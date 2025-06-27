import os
import asyncio
import socket
import logging
import time
import httpx
import numpy as np
import pennylane as qml
from dnslib import DNSRecord, DNSHeader, DNSQuestion

logging.basicConfig(level=logging.INFO)

LISTEN_ADDR = ("127.0.0.1", 5300)
UPSTREAM_DNS = ("8.8.8.8", 53)

def hypertime_supersync():
    t = time.time()
    return round(np.sin(t * np.pi) * np.cos(t / 2), 6)

def quantum_domain_risk(domain: str, pulse: float):
    dev = qml.device("default.qubit", wires=3)
    @qml.qnode(dev)
    def circuit(p):
        qml.Hadamard(wires=0)
        qml.RY((sum(domain.encode()) % 256)/256 * np.pi, wires=1)
        qml.RX(p * np.pi, wires=2)
        qml.CNOT(wires=[1, 2])
        return qml.probs(wires=[0, 1, 2])
    probs = circuit(pulse)
    return float(np.dot(probs, np.arange(1, len(probs)+1)))

async def llm_safe_check(domain, risk, pulse):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY not set.")
        return "SAFE"
    prompt = f"Is this domain SAFE or UNSAFE using hypertime scan: {domain}, risk={risk:.4f}, pulse={pulse}"
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "Return exactly one word: SAFE or UNSAFE."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 1
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        reply = resp.json()["choices"][0]["message"]["content"].strip().upper()
        return "UNSAFE" if "UNSAFE" in reply else "SAFE"
    except Exception as e:
        logging.warning(f"LLM request failed: {e}")
        return "SAFE"

class DNSQuantumProxy:
    def __init__(self, listen_addr, upstream_addr):
        self.listen_addr = listen_addr
        self.upstream_addr = upstream_addr

    async def handle(self, data, addr, sock):
        req = DNSRecord.parse(data)
        domain = str(req.q.qname).rstrip(".")
        pulse = hypertime_supersync()
        risk = quantum_domain_risk(domain, pulse)
        status = await llm_safe_check(domain, risk, pulse)

        logging.info(f"{domain} | pulse={pulse} | risk={risk:.4f} | status={status}")
        if status == "UNSAFE":
            logging.warning(f"Blocking {domain}")
            reply = DNSRecord(DNSHeader(id=req.header.id, qr=1, ra=1), q=req.q)
            sock.sendto(reply.pack(), addr)
        else:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as up:
                    up.settimeout(2)
                    up.sendto(data, self.upstream_addr)
                    resp, _ = up.recvfrom(4096)
                sock.sendto(resp, addr)
            except Exception as e:
                logging.error(f"Upstream error: {e}")

    async def start(self):
        loop = asyncio.get_event_loop()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.listen_addr)
        sock.setblocking(False)
        logging.info(f"Listening on {self.listen_addr}")
        while True:
            data, addr = await loop.sock_recvfrom(sock, 4096)
            asyncio.create_task(self.handle(data, addr, sock))

if __name__ == "__main__":
    proxy = DNSQuantumProxy(LISTEN_ADDR, UPSTREAM_DNS)
    try:
        asyncio.run(proxy.start())
    except KeyboardInterrupt:
        logging.info("Shutting down DNS Quantum Resolver")
