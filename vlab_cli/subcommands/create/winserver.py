# -*- coding: UTF-8 -*-
"""Defines the CLI for creating a Microsoft Server instance"""
import click

from vlab_cli.lib.widgets import Spinner
from vlab_cli.lib.api import consume_task
from vlab_cli.lib.widgets import typewriter
from vlab_cli.lib.click_extras import MandatoryOption
from vlab_cli.lib.portmap_helpers import get_ipv4_addrs
from vlab_cli.lib.ascii_output import format_machine_info


@click.command()
@click.option('-i', '--image', default='2012R2', show_default=True,
              help='The version of Microsoft Server to create')
@click.option('-n', '--name', cls=MandatoryOption,
              help='The name of the Microsoft Server in your lab')
@click.option('-e', '--external-network', default='frontend', show_default=True,
              help='The public network to connect the new Microsoft Server to')
@click.pass_context
def winserver(ctx, name, image, external_network):
    """Create a new Microsoft Server instance"""
    body = {'network': "{}_{}".format(ctx.obj.username, external_network),
            'name': name,
            'image': image.upper()} # upper in case they supply 2012r2
    resp = consume_task(ctx.obj.vlab_api,
                        endpoint='/api/1/inf/winserver',
                        message='Creating a new instance of Microsoft Server {}'.format(image),
                        body=body,
                        timeout=900,
                        pause=5)
    data = resp.json()['content'][name]
    ipv4_addrs = get_ipv4_addrs(data['ips'])
    if ipv4_addrs:
        vm_type = data['meta']['component']
        with Spinner('Creating an RDP port mapping rule'):
            for ipv4 in ipv4_addrs:
                ctx.obj.vlab_api.map_port(target_addr=ipv4, target_port=3389,
                                          target_name=name, target_component=vm_type)
    output = format_machine_info(ctx.obj.vlab_api, info=data)
    click.echo(output)
    if ipv4_addrs:
        typewriter("\nUse 'vlab connect winserver --name {}' to access your new Microsoft Server".format(name))
