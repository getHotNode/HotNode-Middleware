import docker
from celery import shared_task

client = docker.from_env()


@shared_task
def getBicoindStatus():
    print("checking")
    try:
        client.containers.get("bitcoind").reload()
        bitcoind = client.containers.get("bitcoind").status
        print(bitcoind)
        print(type(bitcoind))
    except:
        bitcoind = ""

    return bitcoind


@shared_task
def getRedisStatus():
    try:
        client.containers.get("redis").reload()
        redis = client.containers.get("redis").status
    except:
        redis = createRedis()

    return redis


@shared_task
def createRedis():
    client.containers.create(
        image="redis", command="", name="redis", ports={"6379/tcp": 6379}, detach=1
    )
    client.containers.get("redis").reload()
    return client.containers.get("redis").status
