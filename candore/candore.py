from candore.modules.api_lister import APILister
from candore.modules.extractor import Extractor
from candore.modules.comparator import Comparator
from candore.errors import ModeError
from candore.modules.report import Reporting
import click
import json
from pathlib import Path
import asyncio


api_lister = APILister()


def list_endpoints():
    return api_lister.lister_endpoints()


async def save_all_entities(mode, output_file, full):
    """Save all the entities to a json file

    :param mode: Pre or Post
    :param output_file: Output file name
    :param full: If True, save entities from all pages of the components, else just saves first page
    :return: None
    """
    if mode not in ['pre', 'post']:
        raise ModeError("Extracting mode must be 'pre' or 'post'")

    async with Extractor(apilister=api_lister) as extractor:
        if full:
            extractor.full = True
        data = await extractor.extract_all_entities()

    if not data:
        click.echo('Entities data is not data found!')

    file_path = Path(output_file) if output_file else Path(f'{mode}_entities.json')
    with file_path.open(mode='w') as entfile:
        json.dump(data, entfile)
    click.echo(f'Entities data saved to {file_path}')


def compare_entities(pre_file=None, post_file=None, output=None, report_type=None, record_evs=None):
    comp = Comparator()
    if record_evs:
        comp.record_evs = True
    results = comp.compare_json(pre_file=pre_file, post_file=post_file)
    reporter = Reporting(results=results)
    reporter.generate_report(output_file=output, output_type=report_type)
