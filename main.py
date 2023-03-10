import os
import time
import pickle
import schedule
from sklearn import svm
from intrusion_detection.pacp_extractor import extract_data_from_pcap_file
from intrusion_detection.ML_model import give_malicious_packets
from Intrusion_prevention.create_flow import create_flows

class Prevent_DDoS_Attack():
    def __init__(self, PCAP_DIR) -> None:
        PCAP_DIR: str = PCAP_DIR
        clf: svm.SVC = pickle.load(open('model', 'rb'))
        Processed_PCAP: list = []
        self.malicious_packets= None
    
    def ddos_detection(self):
        #prepare the data
        for file in enumerate(os.listdir(self.PCAP_DIR)):
            if not file in self.Processed_PCAP:
                extract_data_from_pcap_file(file, pcap_dir=self.PCAP_DIR)
                self.Processed_PCAP.append(file)
        #detect malicious packets
        self.malicious_packets = None
        self.malicious_packets = give_malicious_packets()

    def ddos_prevention(self):
        for packet in self.malicious_packets:
            create_flows(packet["src port"], packet["dst port"], packet["src_ip"], packet["dst_ip"])
        return
    
    def network_watcher(self):
        schedule.every(1).minutes.do(self.ddos_detection)
        schedule.every(1).minutes.do(self.ddos_prevention)
        while True:
            schedule.run_pending()
            time.sleep(2)