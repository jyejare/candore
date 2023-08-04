import json


def compare_all_pres_with_posts(pre_data, post_data, unique_key=''):
    if type(pre_data) is dict:
        for key in pre_data:
            if key in post_data:
                compare_all_pres_with_posts(pre_data[key], post_data[key], unique_key=key)
            else:
                print(f"Key is not found in post_data: {key} ")
    elif type(pre_data) is list:
        for pre_entity in pre_data:
            if not pre_entity:
                continue
            if type(pre_entity) is dict:
                for post_entity in post_data:
                    if not post_entity:
                        continue
                    if 'id' in pre_entity:
                        if pre_entity['id'] == post_entity['id']:
                            compare_all_pres_with_posts(pre_entity, post_entity,  unique_key=pre_entity['id'])
                    else:
                        key = list(pre_entity.keys())[0]
                        compare_all_pres_with_posts(pre_entity[key], post_entity[key],   unique_key=pre_entity[key])
            else:
                if pre_entity not in post_data:
                    print("Key: " + unique_key + " Pre List: " + str(pre_data) + " changed in Post: " + str(post_data))
    else:
        if pre_data != post_data:
            print("Key: " + unique_key + " Pre: " + str(pre_data) + " Post: " + str(post_data))




def compare_json():
    pre_data = post_Data = None

    with open("pre_entities2.json", "r") as fpre:
        pre_data = json.load(fpre)

    with open("pre_entities3.json", "r") as fpost:
        post_data = json.load(fpost)

    compare_all_pres_with_posts(pre_data, post_data)

