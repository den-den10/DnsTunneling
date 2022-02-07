from scapy.all import *
import base64

BPF_FILTER = f"udp dst port 60696"

global file_data
file_data = []


def get_data_from_dns(pkt: IP):
    global file_data
    
    
    data =''.join(pkt[DNSQR].qname.decode('ascii').split('.')[:-3])      
    data_index = pkt[DNS].id
    print(data + " located in " + str(data_index))
    
    # Reset the data if its new file
    if(data_index == 0):
        file_data = []

    # Save data as file and move to new one if recieved sigterm
    if(data_index == 0xffff):
        file_name = base64.b16decode(data.encode('ascii')).decode('ascii').replace('\x00','')
        print(file_name)
        with open(file_name, 'wb') as f:
            f.write(base64.b16decode(''.join(file_data))) 

    # Else continue to save data to file    
    else:
        file_data.insert(data_index, data)


def main():
    sniff(filter=BPF_FILTER, prn=get_data_from_dns)

if "__main__" == __name__:
    main()
