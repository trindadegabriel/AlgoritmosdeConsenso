import time
import threading
from cluster import Cluster

def simulate_node_failure(cluster, node_id, duration):
    """
    Simula a falha de um nó por um período definido.
    """
    print(f"[Test] Simulating failure for Node {node_id}")
    failed_node = cluster.nodes[node_id]
    failed_node.state = "failed"

    # Desativar o nó
    def recover():
        time.sleep(duration)
        failed_node.state = "follower"
        failed_node.last_heartbeat = time.time()
        print(f"[Test] Node {node_id} recovered and returned to follower state")

    # Recuperação em uma nova thread
    threading.Thread(target=recover).start()

def simulate_network_partition(cluster, partition_duration):
    """
    Simula uma partição de rede, dividindo o cluster em dois grupos.
    """
    half = len(cluster.nodes) // 2
    group1 = cluster.nodes[:half]
    group2 = cluster.nodes[half:]

    print("[Test] Simulating network partition")
    for node in group1:
        node.partitioned = True
    for node in group2:
        node.partitioned = True

    # Restaurar a rede após o tempo definido
    def restore_network():
        time.sleep(partition_duration)
        for node in group1 + group2:
            node.partitioned = False
        print("[Test] Network partition resolved")

    threading.Thread(target=restore_network).start()

if __name__ == "__main__":
    # Criação do cluster
    cluster = Cluster(num_nodes=5)
    cluster.start()

    # Simular falha em um nó
    simulate_node_failure(cluster, node_id=2, duration=10)

    # Simular partição de rede
    simulate_network_partition(cluster, partition_duration=15)
