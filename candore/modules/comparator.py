import json
import yaml
from pathlib import Path
from candore.config import settings, CURRENT_DIRECTORY
from functools import cached_property, lru_cache


class Comparator:

    def __init__(self):
        self.big_key = []
        self.big_compare = {}
        self.record_evs = False

    @cached_property
    def variations(self):
        templates_path = Path(CURRENT_DIRECTORY, settings.candore.var_file)
        if not templates_path.exists():
            print(f"The file {templates_path} does not exist.")
        with templates_path.open() as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
        return yaml_data

    def get_paths(self, variations, prefix='', separator='/'):
        paths = []
        if isinstance(variations, dict):
            for key, value in variations.items():
                paths.extend(self.get_paths(value, f"{prefix}{key}{separator}"))
        elif isinstance(variations, list):
            for item in variations:
                paths.extend(self.get_paths(item, prefix, separator))
        else:
            paths.append(f'{prefix}{variations}')

        return paths

    def remove_non_variant_key(self, key):
        reversed_bk = self.big_key[::-1]
        reversed_bk.remove(key)
        self.big_key = reversed_bk[::-1]

    def last_index_of_element(self, arr, element):
        for i in range(len(arr) - 1, -1, -1):
            if arr[i] == element:
                return i
        return -1

    def remove_path(self, identy):
        id_index = self.last_index_of_element(self.big_key, identy)
        if id_index == -1:
            return
        self.big_key = self.big_key[:id_index]

    def record_variation(self, pre, post, var_details=None):
        big_key = [str(itm) for itm in self.big_key]
        full_path = '/'.join(big_key)
        var_full_path = '/'.join([itm for itm in self.big_key if not isinstance(itm, int)])
        expected_variations = self.get_paths(variations=self.variations.get('expected_variations'))
        skipped_variations = self.get_paths(variations=self.variations.get('skipped_variations'))
        if var_full_path in expected_variations or var_full_path in skipped_variations:
            if self.record_evs:
                variation = {'pre': pre, 'post': post, 'variation': var_details or 'Expected(A)'}
                self.big_compare.update({full_path: variation})
        elif var_full_path not in expected_variations and var_full_path not in skipped_variations:
            variation = {'pre': pre, 'post': post, 'variation': var_details or ''}
            self.big_compare.update({full_path: variation})

    def _is_data_type_dict(self, pre, post):
        for pre_key in pre:
            if pre_key in post:
                key = pre_key
                self.compare_all_pres_with_posts(pre[key], post[key], unique_key=key)
            else:
                self.compare_all_pres_with_posts(
                    pre[pre_key], None, unique_key=pre_key, var_details='Post lookup key missing')

    def _is_data_type_list(self, pre, post, unique_key=''):
        for pre_entity in pre:
            if not pre_entity:
                continue
            if type(pre_entity) is dict:
                for post_entity in post:
                    if not post_entity:
                        continue
                    if 'id' in pre_entity:
                        if pre_entity['id'] == post_entity['id']:
                            self.compare_all_pres_with_posts(pre_entity, post_entity, unique_key=pre_entity['id'])
                    else:
                        key = list(pre_entity.keys())[0]
                        if pre_entity[key] == post_entity[key]:
                            self.compare_all_pres_with_posts(pre_entity[key], post_entity[key], unique_key=key)
                if 'id' in pre_entity:
                    self.remove_path(pre_entity['id'])
                else:
                    self.remove_path(pre_entity[list(pre_entity.keys())[0]])
            else:
                if pre_entity not in post:
                    self.record_variation(pre, post)
        self.remove_path(unique_key)

    def compare_all_pres_with_posts(self, pre_data, post_data, unique_key='', var_details=None):
        if unique_key:
            self.big_key.append(unique_key)
        if type(pre_data) is dict:
            self._is_data_type_dict(pre_data, post_data)
        elif type(pre_data) is list:
            self._is_data_type_list(pre_data, post_data, unique_key=unique_key)
        else:
            if pre_data != post_data:
                self.record_variation(pre_data, post_data, var_details)
            self.remove_non_variant_key(unique_key)

    def compare_json(self, pre_file, post_file):
        pre_data = post_Data = None

        with open(pre_file, "r") as fpre:
            pre_data = json.load(fpre)

        with open(post_file, "r") as fpost:
            post_data = json.load(fpost)

        self.compare_all_pres_with_posts(pre_data, post_data)
        return self.big_compare
