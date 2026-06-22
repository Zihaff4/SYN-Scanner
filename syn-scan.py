from network_utils import packet, is_host_alive, hoststatus, grab_banner
import sys
from openai import OpenAI
import socket
import errno
import time
#For Ai
client = OpenAI(base_url="https://models.inference.ai.azure.com")
#def area
def port_analyze(port, status, banner_info="None"):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=[
            {"role": "system",
            "content":(
                "You are a network security assistant analyzing a port scan result. "
                "If the port status is 'open', summarize what service runs there and its biggest security risk. "
                "Identify the application name and version if visible, and map its highest-severity known CVE or security risk. "
                "If the port status is 'Closed' or 'filtered', do NOT list security risks for an active service. "
                "Instead, explain what the closed/filtered status means for the attacker trying to scan it. "
                "Keep your response to a maximum of 2 sentences."
            ) 
             },
            {"role": "user",
             "content": f"Port {port} is {status}. Banner found: '{banner_info}'. Analyze it."}
        ]
    )
    ai_replay = response.choices[0].message.content
    return ai_replay

#main program
try:
    while True:
        #SYN-Script
        target = input("[-]Enter the Target IP/Hostname: ")
        target_IP = socket.gethostbyname(target)
        hs_result = hoststatus(target_IP)
        if hs_result == "true":
            print("[-]Host is alive.")
        else:
            print("[-]Host is offline.")
            continue  
        
        time.sleep(1.0)
        #Menu
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

        #for each port
        for target_port in ports_to_scan:
            result = packet(target_IP, target_port)
            #Scan logic
            if result == 0:
                print("[-]Port Open.")
                status = "open"                  
            elif result == errno.ECONNREFUSED or result == 10061:
                print("[-]Port Closed.")
                status = "Closed"                  
            else:
                print("[-]Port filtered.")
                status = "filtered"
            #prints Ai's answer only if the port is open.
            if status == "open":
                #Banner analyzing
                print("[-] Grabbing service banner...")
                banner_info = grab_banner(target_IP, target_port)
                print(f"[-] Service Banner: {banner_info}")
                #Ai analyzing
                print("[-] Ai Analyzing open port service risks...")
                ai_result = port_analyze(target_port, status, banner_info)
                print(f"[-] {ai_result}\n")
            else:
                print()
        time.sleep(1.0)      
except KeyboardInterrupt:
    print("\n[-]Script stopped by user.")
