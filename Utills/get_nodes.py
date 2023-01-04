import requests
import re

def get_nodes() -> list:
    url = "http://localhost:8181/restconf/operational/network-topology:network-topology/topology/flow:1"

    payload={}
    headers = {
    'Authorization': 'Basic YWRtaW46YWRtaW4=',
    'Cookie': 'JSESSIONID=bhgveqfwd4j41n5cqp5pwvx05'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    nodes = []

    try:
        nodes = response["topology"][0]["node"]
    except:
        print("error no running node")

    nodes_id = []
    for node in nodes:
        nodes_id.append(node["node-id"])

    nodes_id.sort()
    regex = re.compile('openflow.*')
    nodes_id = [ node for node in nodes_id if regex.match(node) ]
    return nodes_id


def get_ovs_name_of_nodes(nodes: list) -> dict:
    result = dict()
    for node in nodes:
        url = f"http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/node/{node}"
        payload={}
        headers = {
        'Authorization': 'Basic YWRtaW46YWRtaW4=',
        'Cookie': 'JSESSIONID=bhgveqfwd4j41n5cqp5pwvx05'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        try:
            node_connector = response["node"][0]["node-connector"]
            result[node] = []
            for connector in node_connector:
                if connector["id"] == f"{node}:LOCAL":
                    continue
                else:
                    result[node].append(connector["flow-node-inventory:name"])
        except:
            continue
        
    return result


print(get_ovs_name_of_nodes(get_nodes()))