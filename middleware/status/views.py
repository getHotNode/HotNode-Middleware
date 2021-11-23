from imp import reload

import docker
from django.http import HttpResponse
from django.shortcuts import render
from django.template import context
from django.views.generic.base import TemplateView

from .tasks import getBicoindStatus, getRedisStatus

client = docker.from_env()
# Create your views here.
class Index(TemplateView):
    template_name = "status/home.html"

    def get_context_data(self, **kwargs):
        # getBicoindStatus.delay()
        context = super().get_context_data(**kwargs)
        context["redis"] = getRedisStatus()
        context["bitcoind"] = getBicoindStatus()
        context["lightningd"] = "W.I.P"
        return context


def startRedis(request):
    client.containers.get("redis").start()
    return HttpResponse(
        """<html><script>window.location.replace('/');</script></html>"""
    )


def stopRedis(request):
    client.containers.get("redis").stop()
    return HttpResponse(
        """<html><script>window.location.replace('/');</script></html>"""
    )


def createBitcoind(request):
    client.containers.create(
        image="lncm/bitcoind:v22.0",
        command="",
        detach=1,
        name="bitcoind",
        ports={"8332/tcp": 8332, "8333/tcp": 8333},
        volumes=["/Users/ron/Documents/devops/hotnode/bitcoin:/data/.bitcoin"],
    )
    return HttpResponse(
        """<html><script>window.location.replace('/');</script></html>"""
    )


def startBitcoind(request):
    client.containers.get("bitcoind").start()
    return HttpResponse(
        """<html><script>window.location.replace('/');</script></html>"""
    )


def stopBitcoind(request):
    # client.containers.stop_signal('bitcoind')
    client.containers.get("bitcoind").stop()
    return HttpResponse(
        """<html><script>window.location.replace('/');</script></html>"""
    )


def deleteBitcoind(request):
    client.containers.prune()
    return HttpResponse(
        """<html><script>window.location.replace('/');</script></html>"""
    )
