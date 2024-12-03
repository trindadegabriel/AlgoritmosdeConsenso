import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def log_event(node_id, message):
    logging.info(f"[Node {node_id}] {message}")
