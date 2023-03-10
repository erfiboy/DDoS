import os
import csv
import time
import pyshark
from threading import Thread
from utils.get_nodes import get_nodes, get_ovs_name_of_nodes

def sniff_packets_from_switch(interface_name: str, informations: list) -> tuple:
    capture = pyshark.LiveCapture(interface = interface_name)
    capture.sniff(packet_count=1)
    for packet in capture:
        try:
            print(packet.highest_layer)
            if "ICMP" == packet.highest_layer:
                informations.append((packet['ip'].dst, packet['ip'].src, -1, -1, "ICMP", packet.sniff_timestamp))
            elif "UDP" == packet.highest_layer:
                informations.append((packet['ip'].src, packet['ip'].dst, packet['udp'].srcport, packet['udp'].dstport, "UDP", packet.sniff_timestamp))
            elif "TCP"  == packet.highest_layer:
                informations.append((packet['ip'].src, packet['ip'].dst, packet['tcp'].srcport, packet['tcp'].dstport, "TCP", packet.sniff_timestamp))
        except Exception as e:
            print(e)
            continue
    return informations

def get_packets_of_all_nodes():
    nodes = get_ovs_name_of_nodes(get_nodes())
    switches = []
    for switch in nodes.keys():
        switches.extend(nodes[switch])

    threads = [None] * len(switches)
    results = [[]] * len(switches)

    packets = []
    for index, switch in enumerate(switches):
        threads[index] = Thread(target=sniff_packets_from_switch, args=(switch, results[index]))
        threads[index].start()

    for index in range(len(switches)):
        threads[index].join()
    
    for result in results:
        if result is not None:
            packets.extend(result)

    path = os.getcwd()
    path = os.path.join(path, "capture_dir", f"mininet_{str(int(time.time()))}")
    save_csv(TCP_Packets= packets,out_path= path)

    return

def save_csv(TCP_Packets, out_path):
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([' IP Source', ' IP Destination', ' Port Source', ' Port Destination', ' Protocol', ' Timestamp'])
        for pkt in TCP_Packets:
            writer.writerow(pkt)


if __name__ == "__main__":
    get_packets_of_all_nodes()