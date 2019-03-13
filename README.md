
## List Cluster
```
ibmcloud ks clusters
```

## Show Configuration
```
ibmcloud ks cluster-config ssm-dev
```
```
export KUBECONFIG=/home/vinoth/.bluemix/plugins/container-service/clusters/ssm-dev/kube-config-dal12-ssm-dev.yml
```

## List Nodes

```
kubectl get nodes
```

```
NAME            STATUS   ROLES    AGE    VERSION
10.184.94.208   Ready    <none>   7d3h   v1.12.6+IKS
10.184.94.215   Ready    <none>   7d3h   v1.12.6+IKS
```

## Create Deployment Unit

```
kubectl run was9 --port=9043 --port=9080 --image=docker.io/vinoth186/was:latest
```

## List Deployments

```
kubectl get deployments
```

```
NAME                 DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
hello-world-python   1         1         1            1           7d2h
was9                 1         1         1            1           47h
```
## Get POD
```
kubectl get pods
```
```
NAME                                 READY   STATUS    RESTARTS   AGE
hello-world-python-5c7f858f8-pf7wq   1/1     Running   0          7d2h
was9-756977f6fc-977r4                1/1     Running   0          47h
```

## Expose deployment
```
kubectl create -f was9-nodeport-svc.yaml
```
## Get Service

```
kubectl get services
```
```
NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE
hello-world-python   NodePort    172.*.*.*        <none>        80:30918/TCP                    7d2h
kubernetes           ClusterIP   172.*.*.*        <none>        443/TCP                         7d4h
was9                 NodePort    172.*.*.*        <none>        9080:31230/TCP,9043:31240/TCP   47h
```

## Describe Service
```
kubectl describe service was9
```
## Worker Info
```
ibmcloud ks workers --cluster ssm-dev
```
## Delete Service and Deployment
```
kubectl delete deployments/was9 services/was9 
```
## Delete POD

```
kubectl delete pods -l app=was9
```
