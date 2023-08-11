import json

big_key = []


def remove_non_variant_key(key):
    global big_key
    reversed_bk = big_key[::-1]
    reversed_bk.remove(key)
    big_key = reversed_bk[::-1]


def _is_data_type_dict(pre, post):
    global big_key
    for pre_key in pre:
        if pre_key in post:
            key = pre_key
            compare_all_pres_with_posts(pre[key], post[key], unique_key=key)
        else:
            print(f"Key is not found in post_data: {pre_key}")


def _is_data_type_list(pre, post, unique_key=''):
    global big_key
    for pre_entity in pre:
        if not pre_entity:
            continue
        if type(pre_entity) is dict:
            for post_entity in post:
                if not post_entity:
                    continue
                if 'id' in pre_entity:
                    if pre_entity['id'] == post_entity['id']:
                        compare_all_pres_with_posts(pre_entity, post_entity, unique_key=pre_entity['id'])
                else:
                    key = list(pre_entity.keys())[0]
                    if pre_entity[key] == post_entity[key]:
                        compare_all_pres_with_posts(pre_entity[key], post_entity[key], unique_key=pre_entity[key])
        else:
            if pre_entity not in post:
                print("Key: " + '-'.join(big_key) + " Pre List: " + str(pre) + " changed in Post: " + str(post))
    else:
        remove_non_variant_key(unique_key)


def compare_all_pres_with_posts(pre_data, post_data, unique_key=''):
    global big_key
    big_key.append(str(unique_key))
    if type(pre_data) is dict:
        _is_data_type_dict(pre_data, post_data)
    elif type(pre_data) is list:
        _is_data_type_list(pre_data, post_data, unique_key=unique_key)
    else:
        if pre_data != post_data:
            print("Key: " + '-'.join(big_key) + " Pre: " + str(pre_data) + " Post: " + str(post_data))
        else:
            remove_non_variant_key(unique_key)


def compare_json():
    pre_data = post_Data = None

    with open("data/pre_entities.json", "r") as fpre:
        pre_data = json.load(fpre)

    with open("data/post_entities.json", "r") as fpost:
        post_data = json.load(fpost)

    compare_all_pres_with_posts(pre_data, post_data)
