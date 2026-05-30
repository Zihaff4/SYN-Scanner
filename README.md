# SYN Port Scanner with AI Analysis

A Python-based TCP port scanner that checks whether a target host's port is **open**, **closed**, or **filtered** — then uses an AI model (GPT-4o-mini via Azure) to analyze open ports and explain the security implications.

---

## Features

- **Host liveness check** before scanning
- **Single port scan** or **sequential port range scan**
- **AI-powered analysis** of open ports (powered by GPT-4o-mini via Azure)
- **Cross-platform API key detection** — works on Windows, Linux, and macOS
- Runs in a continuous loop until stopped with `Ctrl+C`

---

## Requirements

- Python 3.7+
- An API key for the Azure OpenAI inference endpoint

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup — API Key

The script will automatically detect your API key. It checks in this order:

1. **Environment variable** `OPENAI_API_KEY` (recommended)
2. **Saved key file** (`~/.syn_scanner_key` on Linux/macOS, `%USERPROFILE%\.syn_scanner_key` on Windows)
3. **Manual input** at runtime — with an option to save it for future use

### Set the environment variable permanently

**Linux:**
```bash
echo 'export OPENAI_API_KEY="your_key_here"' >> ~/.bashrc && source ~/.bashrc
```

**macOS:**
```bash
echo 'export OPENAI_API_KEY="your_key_here"' >> ~/.zshrc && source ~/.zshrc
```

**Windows (CMD):**
```cmd
setx OPENAI_API_KEY "your_key_here"
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your_key_here"
```

> If no key is provided, the script still runs but AI analysis will be disabled.

---

## Usage

```bash
python syn-scan.py
```

```
[-]Enter the Target IP/Hostname: scanme.nmap.org
[-]Host is alive.
++++++++++++__Menu__+++++++++++++
[-]1.Single Scan
[-]2.Sequential Scan
[-]Type Ctrl+C(for exit)
+++++++++++++++++++++++++++++++++
[-]Enter choice (1-2): 1
[-]Enter the Target port: 80
[-]Port 80 Open.
[-] AI Analyzing open port service risks...
[-] Port 80 runs HTTP web services and is a common target for attacks like SQL injection and XSS.
```

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational purposes** and **authorized security testing only**.
Scanning hosts without explicit permission is **illegal** in most jurisdictions.
The author is not responsible for any misuse of this tool.

---

## License

[MIT](LICENSE)
