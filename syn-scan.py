import sys
import os
import platform
import subprocess
from openai import OpenAI
import socket
import errno
import time

# ─── API Key Detection (cross-platform) ───────────────────────────────────────
def get_api_key():
    # 1. Check environment variable first (works on all OS)
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    system = platform.system()

    # 2. Try reading from a saved key file (cross-platform fallback)
    if system == "Windows":
        key_file = os.path.join(os.environ.get("USERPROFILE", ""), ".syn_scanner_key")
    else:
        key_file = os.path.expanduser("~/.syn_scanner_key")

    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            api_key = f.read().strip()
        if api_key:
            print("[-] API key loaded from saved key file.")
            return api_key

    # 3. Ask the user to enter it manually
    print("\n[!] OPENAI_API_KEY not found in environment variables.")
    print("[!] You can set it permanently by following these steps:")
    if system == "Windows":
        print("    CMD:        setx OPENAI_API_KEY \"your_key_here\"")
        print("    PowerShell: $env:OPENAI_API_KEY=\"your_key_here\"")
    elif system == "Darwin":
        print("    macOS:  echo 'export OPENAI_API_KEY=\"your_key_here\"' >> ~/.zshrc && source ~/.zshrc")
    else:
        print("    Linux:  echo 'export OPENAI_API_KEY=\"your_key_here\"' >> ~/.bashrc && source ~/.bashrc")

    print()
    api_key = input("[?] Enter your API key now to continue (or press Enter to skip AI): ").strip()

    if api_key:
        save = input("[?] Save key to file for future use? (y/n): ").strip().lower()
        if save == "y":
            with open(key_file, "w") as f:
                f.write(api_key)
            # Restrict file permissions on Linux/macOS
            if system != "Windows":
                os.chmod(key_file, 0o600)
            print(f"[-] Key saved to {key_file}")
        return api_key

    return None

# ─── Initialize API client ────────────────────────────────────────────────────
api_key = get_api_key()
if api_key:
    client = OpenAI(api_key=api_key, base_url="https://models.inference.ai.azure.com")
    ai_enabled = True
else:
    print("[!] No API key provided. AI analysis will be disabled.\n")
    ai_enabled = False

# ─── Functions ────────────────────────────────────────────────────────────────
def port_analyze(port, status):
    if not ai_enabled:
        return "AI analysis disabled (no API key)."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.0,
            messages=[
                {"role": "system",
                "content":(
                    "You are a network security assistant analyzing a port scan result. "
                    "If the port status is 'open', summarize what service runs there and its biggest security risk. "
                    "If the port status is 'Closed' or 'filtered', do NOT list security risks for an active service. "
                    "Instead, explain what the closed/filtered status means for the attacker trying to scan it. "
                    "Keep your response to a maximum of 2 sentences."
                )},
                {"role": "user",
                 "content": f"Port {port} is {status}. Analyze it."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis failed: {e}"

def packet(target_ip, target_port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(0.5)
    result = soc.connect_ex((target_ip, target_port))
    soc.close()
    return result

def is_host_alive(target_ip):
    s_result = packet(target_ip, 80)
    if s_result == 0 or s_result == errno.ECONNREFUSED or s_result == 10061:
        return True
    return False

def hoststatus(target_ip):
    return "true" if is_host_alive(target_ip) else "false"

# ─── Main Program ─────────────────────────────────────────────────────────────
try:
    while True:
        target = input("[-]Enter the Target IP/Hostname: ")
        target_IP = socket.gethostbyname(target)
        hs_result = hoststatus(target_IP)
        if hs_result == "true":
            print("[-]Host is alive.")
        else:
            print("[-]Host is offline.")
            continue

        time.sleep(1.0)
        # Menu
        print("++++++++++++__Menu__+++++++++++++")
        print("[-]1.Single Scan")
        print("[-]2.Sequential Scan")
        print("[-]Type Ctrl+C(for exit)")
        print("+++++++++++++++++++++++++++++++++")

        menu_input = input("[-]Enter choice (1-2): ")
        ports_to_scan = []
        if menu_input == "1":
            target_port = int(input("[-]Enter the Target port: "))
            ports_to_scan = [target_port]
        elif menu_input == "2":
            start_port = int(input("[-]Enter start port: "))
            end_port = int(input("[-]Enter end port: "))
            if end_port < start_port:
                start_port, end_port = end_port, start_port
            ports_to_scan = list(range(start_port, end_port + 1))
        else:
            print("[-]Invalid choice.")
            continue

        # For each port
        for target_port in ports_to_scan:
            result = packet(target_IP, target_port)
            if result == 0:
                print(f"[-]Port {target_port} Open.")
                status = "open"
            elif result == errno.ECONNREFUSED or result == 10061:
                print(f"[-]Port {target_port} Closed.")
                status = "Closed"
            else:
                print(f"[-]Port {target_port} Filtered.")
                status = "filtered"

            if status == "open":
                print("[-] AI Analyzing open port service risks...")
                ai_result = port_analyze(target_port, status)
                print(f"[-] {ai_result}\n")
            else:
                print()

        time.sleep(1.0)

except KeyboardInterrupt:
    print("\n[-]Script stopped by user.")
