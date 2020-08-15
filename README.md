# k8s-operator-example
## 部署方式
1. 部署到k8s中：

打包，并推送到DockerHub中：
```shell
docker build -t koza/k8s-operator-example:latest .
docker push koza/k8s-operator-example:latest
```

部署：
```shell
kubectl apply -f ./py-kopf-deployment.yaml
```


