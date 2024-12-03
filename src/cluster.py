import threading
import time
from node import Node

class Cluster:
    def __init__(self, num_nodes):
        self.nodes = [Node(node_id=i, cluster=self) for i in range(num_nodes)]

    def start(self):
        for node in self.nodes:
            threading.Thread(target=node.run).start()

    def send_message(self, sender_id, receiver_id, message):
        receiver = self.nodes[receiver_id]
        receiver.receive_message(sender_id, message)

    def broadcast(self, sender_id, message):
        for node in self.nodes:
            if node.node_id != sender_id:
                self.send_message(sender_id, node.node_id, message)

if __name__ == "__main__":
    cluster = Cluster(num_nodes=5)
    cluster.start()
