import time
import random

class Node:
    def __init__(self, node_id, cluster):
        self.node_id = node_id
        self.cluster = cluster
        self.state = "follower"
        self.current_term = 0
        self.voted_for = None
        self.logs = []
        self.timeout = random.randint(5, 10)
        self.last_heartbeat = time.time()

    def run(self):
        while True:
            if self.state == "follower":
                self.run_follower()
            elif self.state == "candidate":
                self.run_candidate()
            elif self.state == "leader":
                self.run_leader()

    def run_follower(self):
        while self.state == "follower":
            if time.time() - self.last_heartbeat > self.timeout:
                self.state = "candidate"

    def run_candidate(self):
        self.current_term += 1
        self.voted_for = self.node_id
        votes = 1
        print(f"[Node {self.node_id}] Started election for term {self.current_term}")
        self.cluster.broadcast(self.node_id, {"type": "vote_request", "term": self.current_term})

        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if self.state == "follower":
                return
            if votes > len(self.cluster.nodes) // 2:
                self.state = "leader"
                print(f"[Node {self.node_id}] Elected as leader for term {self.current_term}")
                return

    def run_leader(self):
        while self.state == "leader":
            self.cluster.broadcast(self.node_id, {"type": "heartbeat", "term": self.current_term})
            time.sleep(2)

    def receive_message(self, sender_id, message):
        if message["type"] == "vote_request" and message["term"] >= self.current_term:
            self.current_term = message["term"]
            self.state = "follower"
            self.voted_for = sender_id
            print(f"[Node {self.node_id}] Voted for Node {sender_id} in term {self.current_term}")
            self.cluster.send_message(self.node_id, sender_id, {"type": "vote", "term": self.current_term})

        elif message["type"] == "heartbeat" and message["term"] >= self.current_term:
            self.current_term = message["term"]
            self.last_heartbeat = time.time()
            self.state = "follower"
            print(f"[Node {self.node_id}] Received heartbeat from Node {sender_id}")
