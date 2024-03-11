import asyncio
from pprint import pprint

import click

from candore import Candore
from candore.config import candore_settings

# Click Interactive for Cloud Resources Cleanup


@click.group(
    help="A data integrity validation CLI tool for upgradable products",
    invoke_without_command=True,
)
@click.option("--version", is_flag=True, help="Installed version of candore")
@click.option("--settings-file", "-s", default=None, help="Settings file path")
@click.option("--components-file", "-c", default=None, help="Components file path")
@click.pass_context
def candore(ctx, version, settings_file, components_file):
    if version:
        import pkg_resources

        ver = pkg_resources.get_distribution("candore").version
        click.echo(f"Version: {ver}")
    candore_obj = Candore(
        settings=candore_settings(
            option_settings_file=settings_file, option_components_file=components_file
        )
    )
    ctx.__dict__["candore"] = candore_obj


@candore.command(help="List API lister endpoints from Product")
@click.pass_context
def apis(ctx):
    """List API lister endpoints from Product"""
    print("List of API lister endpoints from Product")
    candore_obj = ctx.parent.candore
    pprint(candore_obj.list_endpoints())


@candore.command(help="Extract and save data using API lister endpoints")
@click.option("--mode", type=str, help="The mode must be 'pre' or 'post'")
@click.option("-o", "--output", type=str, help="The output file name")
@click.option("--full", is_flag=True, help="Extract data from all the pages of a component")
@click.pass_context
def extract(ctx, mode, output, full):
    loop = asyncio.get_event_loop()
    candore_obj = ctx.parent.candore
    loop.run_until_complete(candore_obj.save_all_entities(mode=mode, output_file=output, full=full))


@candore.command(help="Compare pre and post upgrade data")
@click.option("--pre", type=str, help="The pre upgrade json file")
@click.option("--post", type=str, help="The post upgrade json file")
@click.option("-o", "--output", type=str, help="The output file name")
@click.option(
    "-t",
    "--report-type",
    type=str,
    default="json",
    help="The type of report GSheet, JSON, or webpage",
)
@click.option("--record-evs", is_flag=True, help="Record Expected Variations in reporting")
@click.pass_context
def compare(ctx, pre, post, output, report_type, record_evs):
    candore_obj = ctx.parent.candore
    candore_obj.compare_entities(
        pre_file=pre,
        post_file=post,
        output=output,
        report_type=report_type,
        record_evs=record_evs,
    )


@candore.command(help="JSON Reader for reading the specific path data from entities data file")
@click.option(
    "--path",
    type=str,
    help="The path to search the data from.\n"
    "Path contents could divided by some delimiter.\n"
    "e.g entity/5/description",
)
@click.option(
    "--data-file", type=str, help="The data file from which to search the data on a given path"
)
@click.option("--delimiter", type=str, default='/', help="Settings file path. Default is '/'")
@click.pass_context
def reader(ctx, path, data_file, delimiter):
    candore_obj = ctx.parent.candore
    candore_obj.find_path(path=path, json_file=data_file, delimiter=delimiter)


if __name__ == "__main__":
    candore()
