import aiohttp

from candore.config import settings
from functools import cached_property
import asyncio

class Extractor:
    def __init__(self, apilister=None):
        """Extract and save data using API lister endpoints

        :param apilister: APILister object
        """
        self.username = settings.candore.username
        self._passwd = settings.candore.password
        self.base = settings.candore.base_url
        self.verify_ssl = False
        self.auth = aiohttp.BasicAuth(self.username, self._passwd)
        self.connector = aiohttp.TCPConnector(ssl=self.verify_ssl)
        self.client = None
        self.apilister = apilister

    @cached_property
    def dependent_components(self):
        return settings.components.dependencies

    @cached_property
    def ignore_components(self):
        return settings.components.ignore

    @cached_property
    def api_endpoints(self):
        return self.apilister.lister_endpoints()

    async def _start_session(self):
        if not self.client:
            self.client = aiohttp.ClientSession(auth=self.auth, connector=self.connector)
        return self.client

    async def _end_session(self):
        await self.client.close()

    async def __aenter__(self):
        await self._start_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._end_session()

    async def fetch_component_entities(self, **comp_params):
        endpoint = comp_params.get('endpoint', None)
        data = comp_params.get('data', None)
        dependency = comp_params.get('dependency', None)
        get_params = {'url': self.base+'/'+endpoint, 'params': data}
        if data:
            data = {f'{dependency}_id': data}
            get_params['params'] = data
        async with self.client.get(**get_params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                # response_text = await response.text()
                return None

    async def dependency_ids(self, dependency):
        # All the Ids of a specific dependency
        # e.g Organization IDs 1, 2, 3, 4
        endpoint = self.api_endpoints[f'{dependency}s'][0]
        depe_lists = await self.fetch_component_entities(endpoint=endpoint)
        depen_ids = [dep_dict['id'] for dep_dict in depe_lists['results']]
        return depen_ids


    async def component_params(self, component_endpoint):
        """
        component_endpoints = ['katello/api/activationkeys']
        endpoints = ['activationkeys']
        :param component_endpoints:
        :return:
        """
        data = None
        dependency = None
        # remove ignored endpoints
        _last = component_endpoint.rsplit('/')[-1]
        # Ignorable endpoint
        if _last in self.ignore_components:
            return
        # Return results for components those has dependencies
        if _last in self.dependent_components.keys():
            dependency = self.dependent_components[_last]
            data = await self.dependency_ids(dependency)
        return {'endpoint': component_endpoint, 'data': data, 'dependency': dependency}


    async def process_entities(self, endpoints):
        """
        endpoints = ['katello/api/actiovationkeys']
        """
        comp_data = []
        entities = None
        for endpoint in endpoints:
            comp_params = await self.component_params(component_endpoint=endpoint)
            if comp_params:
                entities = []
                if isinstance(comp_params.get('data'), list):
                    for data_point in comp_params.get('data'):
                        depen_data = await self.fetch_component_entities(
                            endpoint=comp_params['endpoint'], dependency=comp_params['dependency'], data=data_point)
                        if not depen_data:
                            continue
                        depen_data = depen_data.get('results', None)
                        if depen_data:
                            entities.extend(depen_data)
                else:
                    data = await self.fetch_component_entities(**comp_params)
                    if data:
                        entities = data.get('results', None)
            if entities:
                comp_data.extend(entities)
        return comp_data

    async def extract_all_entities(self):
        """
        component, endpoints = `activation_key`, ['katello/api/activationkeys']
        :return:
        """
        all_data = {}
        for component, endpoints in self.api_endpoints.items():
            if endpoints:
                comp_entities = await self.process_entities(endpoints=endpoints)
                all_data[component] = comp_entities
        return all_data

