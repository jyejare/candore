import click
from pprint import pprint
from candore.candore import list_endpoints
from candore.candore import save_all_entities
from candore.candore import compare_entities
import asyncio

# Click Interactive for Cloud Resources Cleanup


@click.group(
    help="A data integrity validation CLI tool for upgradable products",
    invoke_without_command=True,
)
@click.option("--version", is_flag=True, help="Installed version of candore")
@click.pass_context
def candore(ctx, version):
    if version:
        import pkg_resources

        ver = pkg_resources.get_distribution("candore").version
        click.echo(f"Version: {ver}")


@candore.command(help="List API lister endpoints from Product")
@click.pass_context
def apis(ctx):
    """List API lister endpoints from Product"""
    print("List of API lister endpoints from Product")
    pprint(list_endpoints())


@candore.command(help="Extract and save data using API lister endpoints")
@click.option("--mode", type=str, help="The mode must be 'pre' or 'post'")
@click.pass_context
def extract(ctx, mode):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_all_entities(mode=mode))


@candore.command(help="Compare pre and post upgrade data")
@click.pass_context
def compare(ctx):
    compare_entities()


@candore.command(help="Report Variation between upgrades")
@click.pass_context
def report(ctx):
    pass


if __name__ == "__main__":
    candore()