---
layout: single
title: Nodes, Clusters, and Cattle
categories: [kubernetes, linkerd]
---

_What happens when all your Nodes die?_

# Nodes, Clusters, and Cattle

I've been working with Kubernetes for awhile, and in that time I've largely
managed to avoid doing things with Nodes -- if you embrace the "whole clusters
are cattle" philosophy, you don't need to worry about individual Nodes, right?
Just toss the entire cluster and get a new one if things are weird.

But then a bug came over the transom that made me actually go take a closer
look at Nodes again: a Linkerd user using a GKE cluster was scaling the
cluster's Node pool down to 0 every night to save money, and when they scaled
back up, their application Pods were no longer meshed. Not gonna lie: my first
thought was "just toss the whole cluster every night and get a new one", but
it's true that there's a certain amount of automation that needs to happen for
that to be really seamless. For example, tossing the cluster means that the IP
address of any externally-facing services will be different when you spin it
back up, which means you need to be worrying about DNS -- and as we all know,
a day you have to think about DNS is not a great day.

Long story short, the whole thing piqued my interest, because



For the curious, I actually reproduced it with `k3d` because that let me see the details of what was happening. Scripting for bash or zsh follows:

```bash
create_cluster () {
    k3d cluster create ffs \
        --agents 3 \
        --servers 1 \
        -p 80:80@loadbalancer -p 443:443@loadbalancer \
        --k3s-arg --disable=local-storage,traefik@server:0

    kubectl taint nodes k3d-ffs-server-0 node-role.kubernetes.io/master=:NoSchedule
}

install_linkerd () {
    if [ \( "$1" != "" \) -a \( "$1" != "--ha" \) ]; then
        echo "Usage: install_linkerd [--ha]" >&2
    else
        linkerd install --crds | kubectl apply -f -
        linkerd install $1 | kubectl apply -f -
        linkerd check
    fi
}

install_faces () {
    kubectl create ns faces
    kubectl annotate ns faces linkerd.io/inject=enabled

    helm install -n faces \
        --version 0.8.0 faces oci://registry-1.docker.io/dwflynn/faces-chart
}

delete_cluster () {
    k3d cluster delete ffs
}

check_pods () {
    kubectl get pods -n linkerd -o wide
    kubectl get pods -n faces -o wide
}

watch_pods () {
    watch 'sh -c "kubectl get pods -n linkerd -o wide; kubectl get pods -n faces -o wide"'
}

drop_nodes () {
    nodes=$(
        kubectl get node \
          | grep -v control-plane | grep -v NAME \
          | awk ' { print $1 }'
    )
    echo $nodes | xargs kubectl delete node
    echo $nodes | xargs k3d node delete
}

add_nodes () {
    k3d node create new0 --cluster ffs --role agent
    k3d node create new1 --cluster ffs --role agent
    k3d node create new2 --cluster ffs --role agent
}
```

Paste the functions above, then run this sequence to see the problem:

```bash
create_cluster
install_linkerd
install_faces
watch_pods
```

Wait until all the pods are running (all the Faces pods should show two containers). Then

```bash
drop_nodes
watch_pods
```

Wait for the pods to go to `Pending` state. This will take a bit. Finally

```bash
add_nodes
watch_pods
```

and you'll see that when the Faces pods come back, they'll have only one container. This is because Faces starts _much_ faster than Linkerd, so the proxy injector isn't running, so nothing good happens when Faces comes back up.

Now repeat with Linkerd in HA mode:

```bash
delete_cluster
create_cluster
install_linkerd --ha
install_faces
watch_pods
```

Same thing, wait for all pods to be running (you'll note there there are a lot more Linkerd pods running, and that they're scattered evenly across the three `agent` nodes). Then

```bash
drop_nodes
watch_pods
```

Wait for Pending (or missing -- in my setup, the Faces pods are often gone entirely), then

```bash
add_nodes
watch_pods
```

and _this_ time you'll see all the Linkerd pods start running before any of the Faces pods start -- and the Faces pods will have two containers again, like they should.

This is because one of the things that Linkerd's HA mode does is to force pod startup to wait for the proxy injector to be running, which is exactly what you want here.


