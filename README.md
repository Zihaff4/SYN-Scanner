# SYN Port Scanner with AI Analysis

A Python-based TCP port scanner that checks whether a target host's port is **open**, **closed**, or **filtered** — grabs the **service banner**, then uses AI (GPT-4o-mini via Azure) to analyze the result and identify security risks or known CVEs.

---

## Features

- **Host liveness check** before scanning
- **Single port scan** or **sequential port range scan**
- **Service banner grabbing** to identify what's actually running on open ports
- **AI-powered analysis** — identifies app name/version from banner and maps known CVEs
- **Cross-platform API key detection** — works on Windows, Linux, and macOS
- Runs in a continuous loop until stopped with `Ctrl+C`

---

## File Structure

```
SYN-Scanner/
├── syn-scan.py        # Main program — menu, scan logic, AI analysis
├── network_utils.py   # Network helper functions (packet, banner grab, host check)
├── requirements.txt   # Python dependencies
├── .gitignore
└── LICENSE
```

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

The script detects your API key automatically in this order:

1. **Environment variable** `OPENAI_API_KEY` (recommended)
2. **Saved key file** (`~/.syn_scanner_key` on Linux/macOS, `%USERPROFILE%\.syn_scanner_key` on Windows)
3. **Manual input** at runtime — with an option to save it for future use

If no key is provided, the script still runs but AI analysis will be disabled.

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
[-]Enter the Target port: 22
[-]Port 22 Open.
[-] Grabbing service banner...
[-] Service Banner: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6
[-] AI Analyzing open port service risks...
[-] Port 22 runs OpenSSH 8.9p1; CVE-2023-38408 allows remote code execution via ssh-agent forwarding.
```

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational purposes** and **authorized security testing only**.
Scanning hosts without explicit permission is **illegal** in most jurisdictions.
The author is not responsible for any misuse of this tool.

---

## License

[MIT](LICENSE)
