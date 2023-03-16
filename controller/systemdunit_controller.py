import os
import time
from kubernetes import client, config, watch
from kubernetes.client.exceptions import ApiException
import requests

def systemd_unit_status(unit_name, node_name):
    try:
        helper_pod = None
        core_api = client.CoreV1Api()
        label_selector = "app=systemd-helper"
        field_selector = f"spec.nodeName={node_name}"
        pods = core_api.list_namespaced_pod("default", label_selector=label_selector, field_selector=field_selector)
        if len(pods.items) > 0:
            helper_pod = pods.items[0]
        else:
            raise Exception(f"No helper pod found on node {node_name}")

        helper_pod_ip = helper_pod.status.pod_ip
        response = requests.get(f"http://{helper_pod_ip}:8080/systemd-unit-status?unitName={unit_name}", timeout=10)
        response.raise_for_status()
        data = response.json()
        #print(f"Helper response: {data}")
        return data['unitStatus']
    except Exception as e:
        print(f"Error checking systemd unit status on node {node_name}: {e}")
        return "unknown"

def main():
    #config.load_kube_config()
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()

    api = client.CustomObjectsApi()
    group = "hacks4snacks"
    version = "v1"
    plural = "systemdunits"
    namespace = "default"

    w = watch.Watch()
    while True:
        try:
            for event in w.stream(api.list_cluster_custom_object, group, version, plural, timeout_seconds=60):
                resource = event['object']
                unit_name = resource['spec']['unitName']
                print(f"Processing {event['type']} event for SystemdUnit '{unit_name}'")

                if event['type'] == 'ADDED' or event['type'] == 'MODIFIED' or event['type'] == 'DELETED' or event['type'] == 'ERROR':
                    core_api = client.CoreV1Api()
                    nodes = core_api.list_node().items
                    node_statuses = []

                    for node in nodes:
                        node_name = node.metadata.name
                        unit_status = systemd_unit_status(unit_name, node_name)
                        node_statuses.append({'nodeName': node_name, 'unitName': unit_name, 'unitStatus': unit_status})

                    resource['status'] = {'nodeStatuses': node_statuses}
                    #print(f"Updated nodeStatuses: {node_statuses}")
                    api.replace_cluster_custom_object(group, version, plural, resource['metadata']['name'], resource)


        except ApiException as e:
            print(f"Exception: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()
