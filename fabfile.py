from fabric.api import *
from fabdocker import docker
import os
import urllib2
import json
import requests


if os.environ.get("deployment_host"):
    env.hosts = [os.environ.get("deployment_host")]

version = local("git rev-parse --short HEAD", capture=True)

app = "nm_forwarder"
app_image = "thenewmotion/" + app
app_http_port = 8081

registry = "https://index.docker.io/v1/"
registry_agent = "tnmbuildagent"
registry_password = "\"{}\"".format(os.environ.get("tnm_registry_password"))
registry_email = "it@thenewmotion.com"

@task
def build_image():
    with settings(docker_local=True):
        docker.build(app_image, ".", "latest")
        docker.tag(
            source_image=app_image,
            source_tag="latest",
            target_image=app_image,
            target_tag=version,
            force=True
        )
        docker.login(registry, registry_agent, registry_password, registry_email)
        docker.push(app_image + ":latest")
        docker.push(app_image + ":" + version)

@task
def deploy(environment):
    version = os.environ.get("version", "latest")
    env.host_string = os.environ.get("deployment_host")
    vhost = os.environ.get("vhost")
    nm_forwarder_config = os.environ.get("NM_FORWARDER_CONFIG")
    docker.login(registry, registry_agent, registry_password, registry_email)
    docker.pull(app_image, version)

    docker.replace(
        app,
        tag=version,
        new_image=app_image,
        env_vars={
            "ENVIRONMENT": environment,
            "VIRTUAL_HOST": vhost,
            "VIRTUAL_PORT": app_http_port,
            "NM_FORWARDER_CONFIG": nm_forwarder_config
        },
        ports={app_http_port: app_http_port},
        daemon=True
    )
