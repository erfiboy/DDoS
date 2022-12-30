import csv
from scapy.all import *
from subprocess import Popen, PIPE
from scapy.layers.http import HTTPRequest

def get_packet_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1


def extract_features(pcap_path):
    packets = PcapReader(pcap_path)
    TCP_Packets = []
    for pkt in packets:
        if not pkt.haslayer(IP):
            continue    
        if pkt.haslayer(TCP):
            five_tuple = [
                pkt[IP].src,
                pkt[IP].dst,
                pkt[TCP].sport,
                pkt[TCP].dport,
                'HTTPRequest',
                pkt.time
            ]
            TCP_Packets.append(five_tuple)

    return TCP_Packets
    
def save_csv(TCP_Packets, out_path):
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([' IP Source', ' IP Destination', ' Port Source', ' Port Destination', ' Protocol', ' Timestamp'])
        for pkt in TCP_Packets:
            writer.writerow(pkt)


def get_pcap_size(file_path):

    file_stats = os.stat(file_path)
    return int(file_stats.st_size/(1024*1024))

def split_pcap_files(file_path, part_size_MB = 5):
    if get_pcap_size(file_path) < part_size_MB:
        return f"file:{file_path} is less that part size"

    cap_dir = os.path.join(os.getcwd(), "capture_dir")
    
    if not os.path.exists(cap_dir):
        os.mkdir(cap_dir)
    
    file_path_name = os.path.join(cap_dir, file_path)
    
    try:
        p = Popen(['mergecap', file_path, "-w", file_path_name, '-F', 'pcap'])
        stdout, stderr = p.communicate()
    except:
        print("not need to use mergecap.")

    out_path = file_path_name + "-split"
    
    try:
        p = Popen(['tcpdump', '-r', file_path_name, '-w', out_path, '-C', str(part_size_MB)])
        stdout, stderr = p.communicate()
        p = Popen(['rm', file_path_name])
        p.communicate()
        return stdout
    
    except Exception as e:
        print(f"sth goes wrong in tcpdump: {e}")
        return


if __name__ == '__main__':
    # path = '/home/erfiboy/Pictures/Capture/amp.TCP.reflection.SYNACK.pcap'
    # print(split_pcap_files('maccdc2010_00000_20100310205651.pcap.gz'))
    packets = []
    
    for index, file in enumerate(os.listdir('./capture_dir')):
        path = os.path.join(os.getcwd(), 'capture_dir', file)
        file_pkt = extract_features(path)
        if file_pkt == []:
            continue
        packets.extend(file_pkt)
        if index == 2:
            break
    save_csv(packets, 'out.csv')