import json


class Comparator:

    def __init__(self):
        self.big_key = []

    def remove_non_variant_key(self, key):
        reversed_bk = self.big_key[::-1]
        try:
            reversed_bk.remove(key)
        except ValueError:
            import ipdb; ipdb.set_trace()
        self.big_key = reversed_bk[::-1]

    def last_index_of_element(self, arr, element):
        for i in range(len(arr) - 1, -1, -1):
            if arr[i] == element:
                return i
        return -1

    def remove_path(self, identy):
        #id_index = self.big_key.index(str(identy))
        id_index = self.last_index_of_element(self.big_key, str(identy))
        if id_index == -1:
            return
        self.big_key = self.big_key[:id_index]


    def _is_data_type_dict(self, pre, post):
        for pre_key in pre:
            if pre_key in post:
                key = pre_key
                self.compare_all_pres_with_posts(pre[key], post[key], unique_key=key)
            else:
                print(f"Key is not found in post_data: {pre_key}")

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
                    print("Key: " + '-'.join(self.big_key) + " Pre List: " + str(pre) + " changed in Post: " + str(post))
        self.remove_path(unique_key)

    def compare_all_pres_with_posts(self, pre_data, post_data, unique_key=''):
        if unique_key:
            self.big_key.append(str(unique_key))
        if type(pre_data) is dict:
            self._is_data_type_dict(pre_data, post_data)
        elif type(pre_data) is list:
            self._is_data_type_list(pre_data, post_data, unique_key=unique_key)
        else:
            if pre_data != post_data:
                print("Key: " + '-'.join(self.big_key) + " Pre: " + str(pre_data) + " Post: " + str(post_data))
            self.remove_non_variant_key(unique_key)

    def compare_json(self, pre_file, post_file):
        pre_data = post_Data = None

        with open(pre_file, "r") as fpre:
            pre_data = json.load(fpre)

        with open(post_file, "r") as fpost:
            post_data = json.load(fpost)

        self.compare_all_pres_with_posts(pre_data, post_data)
