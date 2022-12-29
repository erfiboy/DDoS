from re import S
import pyshark
from get_nodes import get_nodes, get_ovs_name_of_nodes
from threading import Thread

def sniff_packets_from_switch(interface_name: str, informations: list) -> tuple:
    capture = pyshark.LiveCapture(interface = interface_name)
    capture.sniff(timeout=1)
    for packet in capture:
        try:
            if packet.highest_layer == 'ICMP':
                informations.append((packet['ip'].dst, packet['ip'].src, -1, -1))
            layers = [layer._layer_name for layer in packet.layers]
            if "udp" in layers:
                informations.append((packet['ip'].dst, packet['ip'].src, packet['udp'].srcport, packet['udp'].dstport))
            elif "tcp"  in layers:
                informations.append((packet['ip'].dst, packet['ip'].src, packet['tcp'].srcport, packet['tcp'].dstport))
        except:
            continue
    return informations

def get_packets_of_all_nodes():
    nodes = get_ovs_name_of_nodes(get_nodes())
    switches = []
    for switch in nodes.keys():
        switches.extend(nodes[switch])
    
    threads = [None] * len(switches)
    results = [None] * len(switches)

    packets = []
    for index, switch in enumerate(switches):
        threads[index] = Thread(target=sniff_packets_from_switch, args=(switch, results[index]))
        threads[index].start()

    for index in range(len(switches)):
        threads[index].join()
    
    for result in results:
        if result is not None:
            packets.extend(result)

    return packets

if __name__ == "__main__":
    print(get_packets_of_all_nodes())