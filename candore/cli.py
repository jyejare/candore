import click
from .api_lister import APILister
from pprint import pprint

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
    lister = APILister()
    print('\nList of lister endpoints from product are: \n')
    pprint(lister.lister_endpoints())


@candore.command(help="Extract and save data using API lister endpoints")
@click.pass_context
def extract(ctx):
    pass


@candore.command(help="Compare pre and post upgrade data")
@click.pass_context
def compare(ctx):
    pass


@candore.command(help="Report Variation between upgrades")
@click.pass_context
def report(ctx):
    pass


if __name__ == "__main__":
    candore()
