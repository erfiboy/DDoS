import os 
import json
import shutil
from get_nodes import get_nodes
from send_flows import add_flow, del_all_flows

def clean_directory():
  base = os.path.dirname(os.path.abspath(__file__))
  directory= "switches_flows"
  path = os.path.join(base, directory) 
  if os.path.isdir(path):
    shutil.rmtree(path)

  del_all_flows()

def log_flows(flow, switch_id):
  base = os.path.dirname(os.path.abspath(__file__))
  directory= "switches_flows"
  path = os.path.join(base, directory) 

  if not os.path.isdir(path):
    os.mkdir(path) 

  flow = json.loads(flow)

  f = open(path+"/switch_"+str(switch_id)+"_flow.json", "a")
  json.dump(flow, f, indent=4)
  f.write("\n")
  f.close()


def create_url(config):
  base_url = "http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/"
  node_id = "openflow:"+str(config['node_id'])+"/"
  flow_table = "flow-node-inventory:table/"+str(config['table_id'])+"/"
  flow_id = "flow/"+str(config['flow_id'])
  request_url = base_url + node_id + flow_table + flow_id

  return request_url


def create_payload(config):
  payload = {}
  payload["id"] = config["flow_id"]
  payload["table_id"] = config["table_id"]
  payload["idle-timeout"] = 60
  payload["priority"] = 500

  if "drop" in config.keys() and config["drop"] == True:
    action = {"order": 0, "apply-actions": {"action": [{"order": 0, "drop-action": {}}]}}
    instruction = []
    instruction.append({"order": 0, "apply-actions":{"action": action}})

  payload["instructions"] = {"instruction": instruction}
  payload ={"flow-node-inventory:flow":[payload]} 

  return json.dumps(payload)


def create_flows(src_port, dest_port, src_ip, dst_ip):

  clean_directory()
  
  for node in get_nodes():
          config = {"node_id": node, "table_id": 0, "flow_id": 0, "ipv4-source": f"{src_ip}/32",
                    "ipv4-destination": f"{dst_ip}/32", "tcp-source-port": src_port, "tcp-destination-port":dest_port, "drop": True}
          add_flow(create_url(config), create_payload(config))
          log_flows(create_payload(config), node)
        