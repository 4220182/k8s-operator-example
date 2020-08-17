# k8s-operator-example

利用 python operator 框架 创建k8s operator，本项目使用 kopf框架。
kopf文档：https://kopf.readthedocs.io/en/latest/
kopf项目：https://github.com/zalando-incubator/kopf

可以实时监控k8s中的事件，并做出相应的操作，下面是一些例子：
1. 你可以监控service的创建，并把service的name和ip送到route53中创建相应的域名。参考：https://github.com/email2liyang/kubernetes-service-dns-exporter
2. 你可以使用自定义一些资源创建新的pod。

下面例子，是使用自定义一些资源创建新的pod。

## kopf部署方式
有两种部署方式：
1. 在k8s集群中部署.
2. 在k8s集群外部署。

### 一、部署到k8s中：

1.1 打包，并推送到DockerHub中：
```shell
$ docker build -t koza/k8s-operator-example:latest .
$ docker push koza/k8s-operator-example:latest
```

1.3.部署：

先创建一个sa（此opera的任务是创建一个PO，所以需要一个具备创建pod权限的sa，这里简单直接赋予cluster-admin），此sa配置在部署文件（py-kopf-deployment.yaml）中。
(你也可以利用：rbac-example.yaml创建)
```shell
$ kubectl create sa admin-sa
$ kubectl create clusterrolebinding test-admin-sa \
  --clusterrole=cluster-admin \
  --serviceaccount=default:admin-sa \
  --namespace=default

$ kubectl apply -f ./py-kopf-deployment.yaml

$ kubectl get po
NAME                                                              READY   STATUS    RESTARTS   AGE
py-kopf-operator-854b666b4f-52sbz                                 1/1     Running   0          29m
```


1.4 创建自定义资源：
```shell
kubectl apply -f ./task-crd.yaml

$ kubectl get tasks
No resources found in default namespace.
```

1.5 使用自定义资源，创建一个任务：
```shell
kubectl apply -f ./task_1.yaml

$ kubectl get tasks
NAME     AGE
task-1   5s
```
该任务是触发创建一个POD：
```shell
$ kubectl  get po
NAME                                                              READY   STATUS    RESTARTS   AGE
task-1-8cff75566-jb4f5                                            1/1     Running   0          37s

```

### 二、在k8s集群外部署：
2.1 安装Kopf：
```shell
pip3 install kopf
```

2.2 安装本项目依赖的包：
```shell
pip3 install urllib3
pip3 install yaml
pip3 install kubernetes
```

2.3 创建kopf需要的资源：
```shell
#k8s <= 1.5
kubectl apply -f peering-v1beta1.yaml

#k8s >= 1.6
kubectl apply -f peering-v1beta1.yaml
```

2.4 启动operator
```shell
$ kopf run ./py-kopf.py --verbose
```

2.5 使用自定义资源，创建一个任务：
```shell
kubectl apply -f ./task_1.yaml

$ kubectl get tasks
NAME     AGE
task-1   5s
```
该任务是触发创建一个POD：
```shell
$ kubectl  get po
NAME                                                              READY   STATUS    RESTARTS   AGE
task-1-8cff75566-jb4f5                                            1/1     Running   0          37s

```



