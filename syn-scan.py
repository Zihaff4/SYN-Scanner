import sys
import os
from openai import OpenAI
import socket
import errno

# For AI - API key is read from the OPENAI_API_KEY environment variable
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("[-] Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)
client = OpenAI(api_key=api_key, base_url="https://models.inference.ai.azure.com")
#def area
def port_analyze(port, status):
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
            ) 
             },
            {"role": "user",
             "content": f"Port {port} is {status}. Analyze it."}
        ]
    )
    ai_replay = response.choices[0].message.content
    return ai_replay

def packet(target_ip, target_port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(0.5)
    result = soc.connect_ex((target_ip, target_port))
    soc.close()
    return result

def is_host_alive(target_ip):
    c_result = packet(target_ip, 80)
    if c_result == 0 or c_result == errno.ECONNREFUSED or c_result == 10061:
        return True
    else:
        return False
#main program
try:
    while True:
        #SYN-Script
        target = input("Enter the Target IP/Hostname: ")        
        target_IP = socket.gethostbyname(target)
        
#chacks if the host alive before scan        
        host_status = is_host_alive(target_IP)
        if host_status == False:
            print("[-] Target host is offline") 
            continue
        print("[-] Target host is online")

        target_port = int(input("Enter the Target port: "))    
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

        #prints Ai's answer.    
        print("[-]Ai Analyzing......")
        ai_result = port_analyze(target_port, status)
        print(f"[-]{ai_result}")

        print()
        print("==========================================")     
except KeyboardInterrupt:
    print("\n[-]Script stopped by user.")
