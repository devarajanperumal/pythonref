import click

@click.group()
@click.version_option(version='0.1')
def cli():
    pass

@cli.command()
@click.option('-v', '--verbose', 'verbose', count=True)
@click.option('-u', '--usb', 'devicetype', flag_value='usb', help='Select USB devices only.')
@click.option('-p', '--pcie', 'devicetype', flag_value='pcie', help='Select PCIE devices only.')
@click.option('-s', '--serialno')
@click.argument('fip', type=click.File('rb'), required=True)
def flash(verbose, devicetype, serialno, fip):
    # import pdb;pdb.set_trace()
    if verbose > 0:
        print('Verbose ON')
    click.echo('FIP {} checked for structural integrity'.format(fip.name))
    if serialno:
        click.echo('Flashed {}'.format(serialno))
        return
    if devicetype == 'usb':
        click.echo('Only USB devices selected')
    elif devicetype == 'pcie':
        click.echo('Only PCIE devices selected')
    else:
        click.echo('All devices selected')
    click.echo('Flashed devices')

@cli.command()
@click.option('-v', '--verbose', 'verbose', count=True)
@click.option('-u', '--usb', 'devicetype', flag_value='usb', help='Select USB devices only.')
@click.option('-p', '--pcie', 'devicetype', flag_value='pcie', help='Select PCIE devices only.')
def devices(verbose, devicetype):
    if verbose > 0:
        print('Verbose ON')
    if devicetype == 'usb':
        click.echo('Only USB devices selected')
    elif devicetype == 'pcie':
        click.echo('Only PCIE devices selected')
    else:
        click.echo('All devices selected')
    click.echo('Devices Info')

@cli.command()
@click.option('-a', '--all', is_flag=True)
@click.option('-u', '--usb', 'devicetype', flag_value='usb', help='Select USB devices only.')
@click.option('-p', '--pcie', 'devicetype', flag_value='pcie', help='Select PCIE devices only.')
@click.option('-s', '--serialno')
def report(all, devicetype, serialno):
    click.echo('Not Implemented')

if __name__=='__main__':
    cli()