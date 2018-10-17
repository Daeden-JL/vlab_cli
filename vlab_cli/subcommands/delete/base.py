# -*- coding: UTF -*-
"""The grouping of the ``delete`` subcommand"""
import click

from vlab_cli.subcommands.delete.onefs import onefs
from vlab_cli.subcommands.delete.gateway import gateway
from vlab_cli.subcommands.delete.iiq import iiq
from vlab_cli.subcommands.delete.network import network
from vlab_cli.subcommands.delete.jumpbox import jumpbox
from vlab_cli.subcommands.delete.esrs import esrs
from vlab_cli.subcommands.delete.cee import cee
from vlab_cli.subcommands.delete.router import router
from vlab_cli.subcommands.delete.windows import windows
from vlab_cli.subcommands.delete.winserver import winserver
from vlab_cli.subcommands.delete.centos import centos
from vlab_cli.subcommands.delete.icap import icap
from vlab_cli.subcommands.delete.claritynow import claritynow
from vlab_cli.subcommands.delete.ecs import ecs


@click.group()
def delete():
    """Remove a component from your lab"""
    pass

delete.add_command(onefs)
delete.add_command(gateway)
delete.add_command(iiq)
delete.add_command(network)
delete.add_command(jumpbox)
delete.add_command(esrs)
delete.add_command(cee)
delete.add_command(router)
delete.add_command(windows)
delete.add_command(winserver)
delete.add_command(centos)
delete.add_command(icap)
delete.add_command(claritynow)
delete.add_command(ecs)
