import json


class Finder:
    def read_json(self, jsonfile=None):
        jdata = None
        with open(jsonfile) as file:
            jdata = json.load(file)
        return jdata

    def json_iterator(self, data=None, path=None, delimiter=None):
        if not data:
            return data
        if path:
            path_contents = path.strip().split(delimiter)
            first_path = path_contents[0]
            remaining_path = f'{delimiter}'.join(path_contents[1:])

            if isinstance(data, dict):
                if first_path in data:
                    return self.json_iterator(data.get(first_path, None), remaining_path, delimiter)
                else:
                    print(
                        f'Oh!O! {first_path} is not found in given path, please correct the path!'
                    )
            elif isinstance(data, list):
                for index, element_data in enumerate(data):
                    if isinstance(element_data, dict):
                        if 'id' in element_data and str(element_data['id']) == first_path:
                            return self.json_iterator(element_data, remaining_path, delimiter)
                    elif isinstance(element_data, list):
                        if first_path in element_data:
                            return self.json_iterator(
                                element_data[index], remaining_path, delimiter
                            )
        else:
            return data

    def find(self, path=None, json_file=None, delimiter='/'):
        jdata = self.read_json(json_file)
        return self.json_iterator(jdata, path=path, delimiter=delimiter)
