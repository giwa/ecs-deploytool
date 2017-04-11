import os
import json
from configparser import ConfigParser
from pprint import pformat

import click

from .docker import Docker
from .docker_image import DockerImage
from .aws_ecr import AwsEcr
from .aws_ecs import AwsEcs


@click.group()
@click.argument('config', type=click.Path(exists=True))
@click.option('--env', help='Deploy environment',
              default=lambda: os.environ.get('DEPLOY_ENV', 'staging'))
@click.pass_context
def cli(ctx, env, config):
    cp = ConfigParser()
    cp.read(config, encoding='utf-8')
    ctx.obj['docker'] = Docker(
            ecr_url=cp[env]['ecr_url'],
            region=cp[env]['region'])
    ctx.obj['ecr'] = AwsEcr()
    ctx.obj['ecs'] = AwsEcs()
    ctx.obj['env'] = env
    ctx.obj['config'] = cp[env]


@cli.command(help='list repository in ECR')
@click.pass_context
def list_repositories(ctx):
    ecr = ctx.obj['ecr']
    repositories = ecr.list_repositories()
    for r in repositories:
        click.echo(r)


@cli.command()
@click.argument('src_image', required=True)
@click.argument('dst_image', required=True)
@click.pass_context
def push_image(ctx, src_image, dst_image):
    """
    push a docker image to ECR
    """
    docker = ctx.obj['docker']
    src = DockerImage(src_image)
    dst = DockerImage(dst_image)
    docker.push_image(src, dst)


@cli.command()
@click.argument('image', required=True)
@click.pass_context
def fetch_image(ctx, image):
    """
    fetch a docker image from ECR
    """
    docker = ctx.obj['docker']
    docker_img = DockerImage(image)
    docker.fetch_image(docker_img)


@cli.command()
@click.argument('image', type=click.STRING)
@click.argument('task_definition', type=click.File())
@click.option('--family', help='task_definition family')
@click.option('--cluster', help='the name of cluster')
@click.option('--service', help='the name of service')
@click.option('--desired_count', help='desired_count', type=click.INT)
@click.option('--max', help='maximumPercent of service', type=click.INT)
@click.option('--min', help='minimumHealthyPercent of service', type=click.INT)
@click.pass_context
def deploy_service(ctx, image, task_definition,
                   family, cluster, service, desired_count, max, min):
    """
    Deploy ECS service

    deploytool ./path/configfile deploy_service image:tag task_definition
    """
    ecs = ctx.obj['ecs']
    td_family = family or ctx.obj['config']['family']
    cluster = cluster or ctx.obj['config']['cluster']
    service = service or ctx.obj['config']['service']

    if desired_count is None:
        desired_count = ctx.obj['config'].getint('desired_count')

    if max is None:
        max = ctx.obj['config'].getint('max')

    if min is None:
        min = ctx.obj['config'].getint('min')

    docker_img = DockerImage(image)

    cds = json.load(task_definition)
    for cd in cds:
        cd['image'] = "{ecr_url}/{image}".format(
                ecr_url=ctx.obj['config']['ecr_url'],
                image=docker_img.image_with_tag)

    new_task_definition_arn = ecs.update_task_definition(
            family=td_family,
            container_definitions=cds,
            volumes=[])

    service = ecs.update_service(cluster, service, desired_count,
                                 new_task_definition_arn, max, min)
    click.echo(pformat(service))


@cli.command()
@click.argument('family', type=click.STRING)
@click.argument('number', type=click.INT, default=5)
@click.pass_context
def keep_task_definitions(ctx, family, number):
    '''
    keep task definitions (default 5)
    '''
    ecs = ctx.obj['ecs']
    tds = ecs.fetch_task_definitions(family)
    for td in tds[number:]:
        click.echo(td)
        ecs.deregister_task_definition(td)
        click.echo(f"{td} is deleted")


@cli.command()
@click.argument('repository', type=click.STRING)
@click.argument('number', type=click.INT, default=5)
@click.pass_context
def keep_images(ctx, repository, number):
    '''
    keep images in repository (default 5)
    '''
    ecr = ctx.obj['ecr']
    repos = ecr.fetch_images(repository)
    repos = [r for r in repos if r['imageTag'] != 'latest']
    repos.sort(key=lambda x: x['imageTag'], reverse=True)
    r = ecr.delete_images(repository, repos[number-1:])
    if r is None:
        return

    for img in r['imageIds']:
        click.echo(f"{img['imageTag']} is deleted")
