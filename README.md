# k8s-operator-example
## 部署方式
1. 部署到k8s中：

1.1 打包，并推送到DockerHub中：
```shell
docker build -t koza/k8s-operator-example:latest .
docker push koza/k8s-operator-example:latest
```

1.2.部署：
```shell
kubectl apply -f ./py-kopf-deployment.yaml

$ kubectl get po
NAME                                                              READY   STATUS    RESTARTS   AGE
py-kopf-operator-854b666b4f-52sbz                                 1/1     Running   0          29m
```


1.3 创建自定义资源：
```shell
kubectl apply -f ./task-crd.yaml

$ kubectl get tasks
No resources found in default namespace.
```

1.4 使用自定义资源，创建一个任务：
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



