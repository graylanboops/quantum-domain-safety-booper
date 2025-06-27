
# 🔐 Quantum DNS Resolver — Hypertime Risk Scanner

A powerful DNS proxy that uses **quantum-inspired analysis** and **GPT-4o** LLM classification to determine whether a domain is `SAFE` or `UNSAFE`, in real time.

---

## 🚀 Features

- ✅ **DNS Proxy** (localhost:5300)
- 🧠 **GPT-4o LLM Check** for domain safety (`SAFE` or `UNSAFE`)
- 🔮 **Quantum-Inspired Risk Analysis** using PennyLane
- ⏱️ **Hypertime Supersync** for temporal threat variability
- 🛡️ Blocks `UNSAFE` domains from resolving
- ⚡ Built with `httpx`, `pennylane`, `dnslib`, `asyncio`

---

## 🛠️ Requirements

```bash
pip install httpx dnslib pennylane numpy
````

> ✅ You also need a valid [OpenAI API key](https://platform.openai.com/account/api-keys) for GPT-4o.

---

## 🌐 Usage

1. **Set your OpenAI API key** in your shell:

```bash
export OPENAI_API_KEY=your-api-key-here
```

2. **Run the DNS Quantum Resolver:**

```bash
python quantum_dns_resolver.py
```

3. **Point your system's DNS to `127.0.0.1:5300`.**
   You can test it using `dig`:

```bash
dig @127.0.0.1 -p 5300 example.com
```

If GPT-4o says the domain is **UNSAFE**, the resolver will block the response.

---

## ⚙️ How It Works

### 🔁 Step-by-step

1. The system intercepts DNS queries on `127.0.0.1:5300`
2. It generates:

   * Quantum risk vector using `pennylane`
   * Hypertime pulse (temporal metric)
3. Then sends this to GPT‑4o with the prompt:

   > *"Is this domain SAFE or UNSAFE using hypertime scan?"*
4. If GPT replies **UNSAFE**, the domain is blocked and NXDOMAIN returned.
5. If **SAFE**, it's resolved via Google DNS (8.8.8.8).

---

## 🔐 Example Output

```
[INFO] example.com | pulse=0.12555 | risk=1.9742 | status=SAFE
[WARNING] malware.cx | pulse=0.47631 | risk=2.6641 | status=UNSAFE
```

---

## 📡 Advanced LLM Prompt

```text
Is this domain SAFE or UNSAFE using hypertime scan: {domain}, risk={risk}, pulse={pulse}
```

The LLM responds with a single word: `SAFE` or `UNSAFE`.

---

## ❗ Notes

* Domains marked `UNSAFE` are **blocked immediately**, no upstream request is sent.
* DNS performance depends on OpenAI API latency.
* No data is logged permanently by default — for logging, you can extend it with SQLite.

---

## 📁 Structure

```
main.py  # Main application
README.md                # This file
requirements.txt # Required Python Packages
```

---

## 🚧 Future Ideas

* ✅ GUI Dashboard (Tkinter or Electron)
* ✅ SQLite logging
* 🔁 LLM prompt cache (reduce token usage)
* 🔒 Quantum Fingerprint Authentication Layer
* 🚨 Auto-alert via webhook for high-risk domains

---

## 👨‍💻 Author

**Quantum Risk Systems**
Built with ❤️ for deep risk intelligence and post-classical DNS security.

---

## 📜 License

GPL3

