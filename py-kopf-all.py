'''
https://blog.baeke.info/2020/01/26/writing-a-kubernetes-operator-with-kopf/
https://github.com/gbaeke/kopf-example
'''
import kopf
import os
import yaml
import random
from kubernetes import client
from kubernetes.client.rest import ApiException
import urllib3

urllib3.disable_warnings()


def _generate_random_str(randomlength=8):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'abcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def _getK8sApiFromToken():
    with open('/Users/test/k8s/test/sa/token-admin', 'r') as file:
        Token = file.read().strip('\n')
    APISERVER = 'https://10.2.2.120:6443'
    configuration = client.Configuration()
    configuration.host = APISERVER
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + Token}
    client.Configuration.set_default(configuration)
    api = client.AppsV1Api(client.ApiClient(configuration))
    return api


def getK8sApi():
    api = client.AppsV1Api()
    return api


def get_yaml(spec, name):
    path = os.path.join(os.path.dirname(__file__), 'task-template.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=name, rule=spec['rule'])
    data = yaml.safe_load(text)
    return data


'''
监控所有services的创建
'''
@kopf.on.create('', 'v1', 'services')
def create_fn(spec, name, namespace, logger, **kwargs):
    logger.info("TEST: namespace,name,clusterIP: %s,%s,%s", namespace,name,spec['clusterIP'])


@kopf.on.update('', 'v1', 'services')
def update_fn(spec, name, logger, **kwargs):
    logger.info(f"TEST Update: name %s", name)

@kopf.on.delete('', 'v1', 'services')
def delete(name, logger, **kwargs):
    logger.info(f"TEST delete: name %s", name)
