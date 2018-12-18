#!/usr/bin/env python

import click
import requests
import sys
import json
from zeep import Client, xsd


@click.group()
@click.pass_context
@click.version_option(prog_name="Example of SOAP Client",
                      version="1.0.0")
@click.option("-H", "--host", default="localhost", help="SOAP Web Server")
@click.option("-p", "--port", default="5000", help="Web Server Port")
@click.option("-U", "--username", default="admin", help="Username to login")
@click.option("-P", "--password", default="admin", help="Password to login")
def cli(ctx, host, port, username, password):
    ctx.obj = {
        "baseurl": "http://{0}:{1}/soap/v1".format(host,port),
        "username": username,
        "password": password
    }
    pass

@cli.command()
@click.option('-e', '--endpoint', default="/login", help='URL Endpoint to login to server')
@click.pass_context
def login(ctx, endpoint):
    client = Client("{0}{1}".format(ctx.obj['baseurl'], endpoint))

    r = client.service.login(
        username=ctx.obj['username'],
        password=ctx.obj['password']
    )

    assert r.returnCode == 0
    print("Response code '{0}' with message '{1}'".format(r.returnCode, r.message))

@cli.command()
@click.option('-e', '--endpoint', default="/editBook", help='URL Endpoint to edit a Book')
@click.pass_context
def edit(ctx, endpoint):
    client = Client("{0}{1}".format(ctx.obj['baseurl'], endpoint))

    d = {
        'Credentials': {
                'username': ctx.obj['username'],
                'password': ctx.obj['password']
                },
        'Title': 'This is my book title',
        'Description': 'This is my book description',
        'Author': 'Anthony B'
        }

    r = client.service.editBook(**d)
    assert r.returnCode == 0
    print("Response code '{0}' with message '{1}'".format(r.returnCode, r.message))


@cli.command()
@click.option('-e', '--endpoint', default="/getFile", help='URL Endpoint to download a File from server')
@click.pass_context
def download(ctx, endpoint):
    client = Client("{0}{1}".format(ctx.obj['baseurl'], endpoint))

    d = {
        'Credentials': {
                'username': ctx.obj['username'],
                'password': ctx.obj['password'],
                },
        'id': "3",
        'filename': 'myfilename'
    }

    r = client.service.getFile(**d)
    assert r.returnCode == 0
    print("Response code '{0}' with message '{1}'. Saving file to 'test.png'".format(r.returnCode, r.message))

    with open("test.png", 'w+b') as fh:
        fh.write(bytes(r.file.Data))


if __name__ == '__main__':
    cli()
