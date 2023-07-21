from apix.explore import AsyncExplorer

from candore.config import settings
from candore.config import validate_settings


class APILister:

    def __init__(self):
        self.explorer = AsyncExplorer(name=settings.candore.product_name, version=settings.candore.version, host_url=settings.candore.base_url, base_path=settings.candore.docpath, parser=settings.candore.parser)
        self.list_endpoints = {}

    def _endpoints(self):
        self.explorer.explore()
        self.yaml_data = self.explorer.yaml_data()
        return self.yaml_data

    def lister_endpoints(self):
        list_endpoints = {}

        for component, data in self._endpoints().items():
            methods = data.get('methods', [])
            component_list_apis = [
                path.lstrip('GET ') for method in methods
                for path in method.get('index', {}).get('paths', [])
                if 'id' not in path
            ]
            list_endpoints[component] = component_list_apis

        self.list_endpoints = list_endpoints
        return list_endpoints


apilister = APILister()
