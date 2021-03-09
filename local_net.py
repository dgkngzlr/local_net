import time
import os
import socket

"""
    KULLANIM :

    SERVER : (GONDEREN)
    port_1 = local_net.createSerSoc()
    local_net.sendFileName(port_1, 'C:\\Users\\Dogukan\\Desktop\\VsCodePy\\Yeni klasör\\WLAN_wl_sthwfw1218_19.60.0.7g_19.51.0.4_0x9929ac2c.zip')
    local_net.sendFile(port_1)
    
    CLIENT : (ALAN)
    port_2 = local_net.createCliSoc('192.168.1.2')
    alınan_dosya = local_net.getFileName(port_2)
    local_net.getFile(port_2)

"""


def get_host_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return (host_ip, host_name)
    except:
        print("Unable to get Hostname and IP")


def createSerSoc(port=14555):
    host = ''

    ser_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Server socket created...')
    print('Your Local IP ', get_host_IP())

    try:
        ser_soc.bind((host, port))
        ser_soc.listen()
        print('Listening...')
    except:
        print('ERROR[1] Socket is closed')
        ser_soc.close()

    com_soc, adr = ser_soc.accept()

    print('OK-[CON]')
    print('Client Addr: ', adr)

    return (com_soc)


def sendFileName(soc, path):
    global glob_path

    glob_path = path
    path_list = path.split('\\')
    file_name = path_list[-1]

    bin_file_name = file_name.encode()
    soc.send(bin_file_name)
    print('Successful', '   ', file_name)


def sendFile(soc):
    time.sleep(0.1)
    try:
        file_stats = os.stat(glob_path)
        file_size = file_stats.st_size
        file_size_parse = file_size/100

        send_size = 0

        with open(glob_path, "rb") as f:
            print('Started at ', time.ctime(), '\nFile is sending...')
            data = f.read(1024)
            while(data):
                if send_size >= file_size_parse:
                    print('#', end='')
                    send_size = 0
                soc.send(data)
                send_size += 1024
                data = f.read(1024)
            soc.close()
            print('\nSuccessful', time.ctime())
    except FileNotFoundError:
        print('ERROR[2]')
        soc.close()


def createCliSoc(host_ip, port=14555):
    cli_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_soc.connect((host_ip, port))
    return cli_soc


def getFileName(soc):
    global recv_file_name
    try:
        bin_file_name = soc.recv(1024)
        file_name = bin_file_name.decode('ascii')
        print(file_name)
        recv_file_name = file_name
        return file_name
    except:
        print('ERROR[3]')
        soc.close()


def getFile(soc):
    f = open(recv_file_name, 'wb')
    try:

        recv_data = soc.recv(1024)
        print(time.ctime(), 'File is recieving...', sep='\n')
        while (recv_data):
            f.write(recv_data)
            recv_data = soc.recv(1024)
        print('\nSuccessful', time.ctime())
        soc.close()
        f.close()
    except:
        print('ERROR[4]')
        soc.close()
        f.close()
