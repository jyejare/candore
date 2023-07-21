from candore.modules.api_lister import APILister
from candore.modules.extractor import Extractor
from candore.errors import ModeError
import click
import json
from pathlib import Path
import asyncio


api_lister = APILister()


def list_endpoints():
    return api_lister.lister_endpoints()


async def save_all_entities(mode, api_lister=api_lister):
    """Save all the entities to a json file

    :param mode: Pre or Post
    :param api_lister: The candore.modules.api_lister.APILister object
    :return: None
    """
    if mode not in ['pre', 'post']:
        raise ModeError("Extracting mode must be 'pre' or 'post'")

    async with Extractor(apilister=api_lister) as extractor:
        data = await extractor.extract_all_entities()

    if not data:
        click.echo('Entities data is not data found!')

    file_path = Path(f'{mode}_entities.json')
    with file_path.open(mode='w') as entfile:
        json.dump(data, entfile)
    click.echo(f'Entities data saved to {file_path}')
    if mode not in ['pre', 'post']:
        raise ModeError("Extracting mode must be 'pre' or 'post'")

    async with Extractor(apilister=api_lister) as extractor:
        data = await extractor.extract_all_entities()

    if not data:
        click.echo('Entities data is not data found!')

    file_path = Path(f'{mode}_entities2.json')
    with file_path.open(mode='w') as entfile:
        json.dump(data, entfile)
    click.echo(f'Entities data saved to {file_path}')
