from scapy.all import *
import base64

BPF_FILTER = f"udp dst port 60696"
DATA_LEN = 6

global file_data
file_data = []


def get_data_from_dns(pkt: IP):
    global file_data
    data =''.join(pkt[DNSQR].qname.decode('ascii').split('.')[:-3])   
    try:
        data_index = int(data[:DATA_LEN])
    except:
        return
    data = data[DATA_LEN:]
    print(data + " located in " + str(data_index))
    # Save data as file and move to new one if recieved sigterm
    if(data_index == 999999):
        file_name = base64.b16decode(data.encode('ascii')).decode('ascii').replace('\x00','')
        print(file_name)
        with open(file_name, 'wb') as f:
            f.write(base64.b16decode(''.join(file_data)))
    
    if(data_index == 0):
        file_data = []

    # Else continue to save data to file    
    else:
        file_data.insert(data_index, data)


def main():
    sniff(filter=BPF_FILTER, prn=get_data_from_dns)

if "__main__" == __name__:
    main()
