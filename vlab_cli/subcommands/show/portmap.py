# -*- coding: UTF-8 -*-
"""Defines the CLI for viewing port mapping rules"""
import click

from tabulate import tabulate

from vlab_cli.lib.api import consume_task
from vlab_cli.lib.widgets import Spinner
from vlab_cli.lib.portmap_helpers import port_to_protocol

@click.command()
@click.pass_context
def portmap(ctx):
    """Display configured port mapping/forwarding rules"""
    table = "No portmap rules exist"
    with Spinner('Looking up port mapping rules'):
        rules = ctx.obj.vlab_api.get('/api/1/ipam/portmap').json()['content']
        header = ['Name', 'Type', 'Port', 'Protocol']
        rows = []
        for conn_port, details in rules.items():
            name = details.get('name', 'Error')
            vm_type = details.get('component', 'Unknown')
            vm_port = details.get('target_port', 0)
            protocol = port_to_protocol(vm_type, vm_port)
            rows.append([name, vm_type, conn_port, protocol])
            table = tabulate(rows, headers=header, tablefmt='presto', numalign="center")
    click.echo('\nGateway IP: {}'.format(ctx.obj.vlab_api.vga_ip()))
    click.echo(table)
