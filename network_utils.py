import sys
from openai import OpenAI
import socket
import errno
import time
#functions
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
    else:
        return False

def hoststatus(target_ip):    
    host_status = is_host_alive(target_ip)
    if host_status == False:
        result = "false"
    else:    
        result = "true"
    return result    

def grab_banner(target_ip, target_port, timeout_value=0.5):
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(timeout_value)
        soc.connect((target_ip, target_port))
        raw_buffer = soc.recv(4096)
        soc.close()
        
        ascii_string = raw_buffer.decode("ascii", errors="ignore").strip()
        
        # Handle the remote host closing the connection cleanly (empty byte check)
        if not ascii_string:
            return "Open (No banner broadcasted)"
        return ascii_string
        
    except socket.timeout:
        return "Open (Passive Service / Timeout)"
    except Exception:
        return "Open (Banner connection rejected)"
    