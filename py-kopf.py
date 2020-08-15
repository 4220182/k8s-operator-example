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
group , versions, plural
'''
@kopf.on.create('test.com', 'v1', 'tasks')
def create_fn(spec, name, namespace, logger, **kwargs):

    logger.info("TEST name: %s", name)
    logger.info("TEST: namespace: %s", namespace)
    logger.info(f"TEST: rule %s", spec['rule'])
    data = get_yaml(spec, name)
    api = getK8sApi()
    try:
        obj = api.create_namespaced_deployment(
            namespace='default',
            body=data,
        )
        logger.info(f"TEST Create: uid %s", obj.metadata.uid)
    except ApiException as e:
        logger.error(f"create_namespaced_deployment Exception : %s" % e)


@kopf.on.update('test.com', 'v1', 'tasks')
def update_fn(spec, name, logger, **kwargs):
    logger.info(f"TEST Update: name %s", name)
    logger.info(f"TEST Update: rule %s", spec['rule'])
    data = get_yaml(spec, name)
    api = getK8sApi()
    try:
        obj = api.patch_namespaced_deployment(
            name=name,
            namespace='default',
            body=data,
        )
        logger.info(f"TEST Update: name %s", obj.metadata.uid)
    except ApiException as e:
        logger.error(f"update_namespaced_deployment Exception: %s" % e)


@kopf.on.delete('test.com', 'v1', 'tasks')
def delete(name, logger, **kwargs):
    logger.info(f"TEST delete: name %s", name)
    api = getK8sApi()
    try:
        api.delete_namespaced_deployment(
            name=name,
            namespace="default"
        )
        logger.info(f"TEST delete success.")
    except ApiException as e:
        logger.error(f"delete_namespaced_deployment Exception: %s" % e)