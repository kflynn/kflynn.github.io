+++
date = 2024-02-08
title = "On Scaling Nodes and Startup Races"

[taxonomies]
categories = ["craft of computing"]
tags = ["kubernetes", "linkerd"]
+++

_What really happens when all your nodes die?_

<!-- more -->
----

I've been working with Kubernetes for awhile, and in that time I've
largely managed to avoid doing things with nodes -- if you embrace the
"whole clusters are cattle" philosophy, you don't need to worry about
individual nodes, right? Just toss the entire cluster and get a new one
if things are weird.

But then a bug came over the transom that made me actually go take a
closer look at nodes again: a Linkerd user using a GKE cluster was
scaling the cluster's node pool down to 0 every night to save money, and
when they scaled back up, their application pods were no longer meshed.

Not gonna lie: my first thought was "just toss the whole cluster every
night and get a new one", but it's true that there's a certain amount of
automation that needs to happen for that to be really seamless. For
example, tossing the cluster means that the IP address of any
externally-facing services will be different when you spin it back up,
which means you need to be worrying about DNS -- and as we all know, a
day you have to think about DNS is not a great day. 😂

Long story short, the whole thing piqued my interest, because the more I
thought about it, the more it _should_ work. I ended up reproducing it
with `k3d` because that let me see the details of what was happening.

## Setting Up

To set everything up, we'll start with some scripting -- this should work
for `bash` or `zsh`, but you'll need to check it if you use something
else.

```sh
# Cluster management: create and delete a cluster
create_cluster () {
    # Three agent nodes, one server node
    k3d cluster create ffs \
        --agents 3 \
        --servers 1 \
        -p 80:80@loadbalancer -p 443:443@loadbalancer \
        --k3s-arg --disable=local-storage,traefik@server:0

    # Don't run application pods on the server node
    kubectl taint nodes k3d-ffs-server-0 node-role.kubernetes.io/master=:NoSchedule
}

delete_cluster () {
    k3d cluster delete ffs
}

# Node management: drop all agent nodes
drop_nodes () {
    nodes=$(
        kubectl get node \
          | grep -v control-plane | grep -v NAME \
          | awk ' { print $1 }'
    )
    echo $nodes | xargs kubectl delete node
    echo $nodes | xargs k3d node delete
}

# Node management: re-add agent nodes
add_nodes () {
    k3d node create new0 --cluster ffs --role agent
    k3d node create new1 --cluster ffs --role agent
    k3d node create new2 --cluster ffs --role agent
}

# Install Linkerd
install_linkerd () {
    if [ \( "$1" != "" \) -a \( "$1" != "--ha" \) ]; then
        echo "Usage: install_linkerd [--ha]" >&2
    else
        linkerd install --crds | kubectl apply -f -
        linkerd install $1 | kubectl apply -f -
        linkerd check
    fi
}

# Install Faces to play the role of our application
install_faces () {
    kubectl create ns faces
    kubectl annotate ns faces linkerd.io/inject=enabled

    helm install -n faces \
        --version 0.8.0 faces oci://registry-1.docker.io/dwflynn/faces-chart
}

# See what's running (include on which node)
check_pods () {
    kubectl get pods -n linkerd -o wide
    kubectl get pods -n faces -o wide
}

# Watch new pods come up
watch_pods () {
    watch 'sh -c "kubectl get pods -n linkerd -o wide; kubectl get pods -n faces -o wide"'
}
```

Paste the functions above, then run this sequence to get started:

```bash
create_cluster
install_linkerd
install_faces
watch_pods
```

This will create our `k3d` cluster, install Linkerd, install our
application (meshed), then start watching pods. Wait until all the pods
are running (all the Faces pods should show two containers).

This is the state of our user when they first get their GKE cluster
running: everything is working correctly and they're happy.

## Breaking the World

Since everything is working, it's clearly time to break things! 😂

To do that, let's mimic scaling the node pool to zero by deleting all the
`agent` nodes where our pods are actually running.

```bash
drop_nodes
watch_pods
```

Wait for the pods to go to `Pending` state, meaning that Kubernetes would
like to schedule them, but has no running nodes onto which to schedule
them. (This may take a bit.)

At that point we can mimic scaling the node pool back up, by re-adding
some `agent` nodes:

```bash
add_nodes
watch_pods
```

and you'll see that when the Faces pods come back, they'll have only one
container, meaning that they're not actually meshed. 🤔

## What's Going On?

Poke around looking at logs enough, and you'll see that the root cause
here is a startup race.

At the moment the nodes restart, _all_ of our `Pending` pods become
available for scheduling. Since three nodes quickly become available,
that gives us enough CPU and memory for all the pods to in fact be
scheduled, and when that happens there's a race: if the Linkerd proxy
injector (which is a mutating webhook) isn't running at the moment an
application Pod is created, that application Pod won't be brought into
the mesh.

Unfortunately for us, since the Pods are getting creating all at about
the same time, the Linkerd proxy injector has effectively zero chance of
starting in time to see the application Pods getting created. By the time
the proxy injector does start running, it's missed its chance. The end
result is that the Faces app starts running, but isn't meshed.

## Fixing the Problem

The fix is simple: turn on Linkerd high availability (HA) mode, which
will block pods from starting if the proxy injector isn't running. First
we'll delete and recreate the cluster:

```bash
delete_cluster
create_cluster
```

Then, we'll reinstall everything using Linkerd HA mode.

```bash
install_linkerd --ha    # <= note this difference!
install_faces
watch_pods
```

Again, wait for all pods to be running. You'll note there there are a lot
more Linkerd pods running, and that they're scattered evenly across the
three `agent` nodes.

After that, we can repeat our experiment of scaling down and back up.
Scale down by deleting the `agent` nodes:

```bash
drop_nodes
watch_pods
```

Wait for `Pending` (or missing -- in my setup, the Faces pods are often
gone entirely), then

```bash
add_nodes
watch_pods
```

and _this_ time you'll see all the Linkerd pods start running before any
of the Faces pods start, which guarantees that the proxy injector is
running like it should be before the Faces pods start, which is what we
need. When the Faces pods come up, they'll have two containers again,
like they should.

This is because one of the things that Linkerd's HA mode does is to force
pod startup to wait for the proxy injector to be running, which is
exactly what you want here.

## A Webhook Problem

It's important to be clear that we're using Linkerd to illustrate a
problem with admission webhooks here, not a problem with meshes or
sidecars. If you're using admission webhooks, you absolutely must have a
way to _guarantee_ that the things that rely on your webhook can't start
running before the webhook processor has started.

Kubernetes gives us a tool for this: you can configure admission webhooks
with `failurePolicy: Fail` so that if the webhook provider doesn't
respond when the API server is trying to admit a new resource, the API
server will reject the request and the new resource won't be created.
Linkerd does a couple of other things, as well, but `failurePolicy: Fail`
is the big one: it takes advantage of Kubernetes to absolutely prevent
new Pods from being created before the proxy injector is running.

Interesting enough, treating your clusters as cattle might well fix this,
too (we'll assume you have DNS wrangled). This isn't because
clusters-as-cattle is really _better_ at handling startup than scaling
the node pool down and back up, it's that treating the clusters as cattle
all but requires you to automate installing your application onto a new
cluster in a way that handles dependencies. But, as noted before, this
can be pricy too (as much as I kinda like the idea 😂).

So the best way forward here is probably to realize that sure, scaling
nodes to zero can be a great money-saving tool! Just pay attention to
what your application and its infrastructure needs -- including webhooks.