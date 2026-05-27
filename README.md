# SYN Port Scanner with AI Analysis

A Python-based TCP port scanner that checks whether a target host's port is **open**, **closed**, or **filtered** — then uses an AI model (GPT-4o-mini via Azure) to analyze the result and explain the security implications.

---

## Features

- **Host liveness check** before scanning
- **TCP connect scan** to determine port status
- **AI-powered analysis** of each scan result (powered by OpenAI / Azure inference)
- Runs in a continuous loop until stopped with `Ctrl+C`

---

## Requirements

- Python 3.7+
- An OpenAI-compatible API key (Azure inference endpoint)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/syn-scanner.git
cd syn-scanner
```

2. **Set your API key as an environment variable:**

```bash
# Linux / macOS
export OPENAI_API_KEY="your_api_key_here"

# Windows (CMD)
set OPENAI_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your_api_key_here"
```

> ⚠️ Never hardcode your API key directly in the script.

3. **Run the scanner:**

```bash
python syn-scan.py
```

---

## Usage

```
Enter the Target IP/Hostname: scanme.nmap.org
[-] Target host is online
Enter the Target port: 80
[-]Port Open.
[-]Ai Analyzing......
[-] Port 80 typically runs HTTP web services, making it a common target for attacks like SQL injection,
    cross-site scripting (XSS), and directory traversal. An open port 80 can expose the server to
    unencrypted traffic interception if HTTPS is not enforced.
```

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational purposes** and **authorized security testing only**.  
Scanning hosts without explicit permission is **illegal** in most jurisdictions.  
The author is not responsible for any misuse of this tool.

---

## License

[MIT](LICENSE)
