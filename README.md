# Systemd Unit Operator

The Systemd Unit Operator is a Kubernetes operator that allows you to monitor the status of systemd units across nodes in your cluster. This operator consists of a custom controller that watches for SystemdUnit custom resources, a helper pod that communicates with the nodes to query systemd unit statuses, and the CustomResourceDefinition (CRD) that defines the SystemdUnit resource.

### Features

    Monitor the status of systemd units on all nodes in your cluster.
    Automatically update the SystemdUnit resource with the latest status information.

### Prerequisites

    Kubernetes cluster (version 1.18 or later)
    kubectl command-line tool installed and configured to work with your cluster
    Python 3.6 or later

### Installation

1. Clone the repository:

```Shell
    git clone https://github.com/example/systemd-unit-operator.git
    cd systemd-unit-operator
```

2. Create the CustomResourceDefinition:

```Shell
    kubectl apply -f operator/crds/systemdunit_crd.yaml
```

3. Deploy the helper pod:

```Shell
    kubectl apply -f operator/deployments/helper_service.yaml
```

4. Deploy the controller:

```Shell
    kubectl apply -f operator/deployments/controller.yaml
```

## Usage

1. Create a SystemdUnit custom resource:

```yaml
    apiVersion: hacks4snacks/v1
    kind: SystemdUnit
    metadata:
        name: ssh-systemdunit
    spec:
        unitName: ssh.service
```

2. Save this file as ssh-systemdunit.yaml, and create the resource with the following command:

```Shell
    kubectl apply -f ssh-systemdunit.yaml
```

3. Check the status of the SystemdUnit resource:

```Shell
    kubectl get systemdunit ssh-systemdunit -o jsonpath='{.status.nodeStatuses}'
```

### License

The Systemd Unit Operator is licensed under the MIT License
