# 5 Common VPN Protocols
import nmap
import os
import subprocess


# 1. PPTP
# nmap –Pn -sSV -p1723 <IP>
def get_pptp(ip):
    pptp_port = '1723'
    nm = nmap.PortScanner()
    nm.scan(ip, pptp_port, arguments=' -Pn')
    output = ""
    oports = {}

    
    for host in nm.all_hosts():
        host = host
        hostname = nm[host].hostname()
        hoststate = nm[host].state()

        for proto in nm[host].all_protocols():
            lport = sorted(nm[host][proto].keys())
            
            for port in lport:
                oports[port] = nm[host][proto][port]

    return hostname, hoststate, oports

#print(get_pptp(ip, pptp_port))


# 2. L2TP/IPSec
def get_l2tp_ipsec(ip):
    port = '500'
    nm = nmap.PortScanner()
    nm.scan(ip, port, arguments=' -Pn -sU')
    output = ""
    oports = {}

    
    for host in nm.all_hosts():
        host = host
        hostname = nm[host].hostname()
        hoststate = nm[host].state()

        for proto in nm[host].all_protocols():
            lport = sorted(nm[host][proto].keys())
            
            for port in lport:
                oports[port] = nm[host][proto][port]
    print(oports)
    print('hello')
    if(oports[500]['state'] == 'open'):
        print('hello')
        sudoPassword = 'ab4nk4l4rm'
        command = 'sudo ike-scan -M 219.100.37.7'
        result = subprocess.getoutput('echo %s|sudo -S %s' % (sudoPassword, command))
        p = result

    return hostname, hoststate, oports, str(p)

#print(get_l2tp_ipsec('219.100.37.7', l2tp_ipsec_port))

# 3. OpenVPN
def get_openvpn_tcp(ip):

    print('hello')
    command = 'echo "test" | nc -Nnv -w 2 ' + ip + ' 443'
    result = subprocess.getoutput(command)
    p = result
    success_arr = p.split('succeeded')
    line_arr = p.split('\n')
    if len(success_arr)==2:
        if len(line_arr)==1:
            return True

    return False

#print(get_openvpn_tcp('219.100.37.7'))

# 4. SSTP
def get_sstp(ip):

    command = 'nmap --script sstp-discover -p443 -Pn '+ip
    result = subprocess.getoutput(command)
    p = result
    success_arr = p.split('SSTP is supported.')
    if len(success_arr)>=2:
            return True

    return False

#print(get_openvpn_tcp('219.100.37.7'))

# 5. IKEv2
def get_IKEv2(ip):
    print('hello')
    sudoPassword = 'ab4nk4l4rm'
    command = 'sudo ike-scan -M 219.100.37.7'
    result = subprocess.getoutput('echo %s|sudo -S %s' % (sudoPassword, command))
    p = result
    return str(p)

print(get_IKEv2('219.100.37.7'))