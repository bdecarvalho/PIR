import socket
import sys
import os
from functools import partial

NB_CLIENT  = 10
PORT = 25555
FILE_FOUND = False

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('',PORT))

print("Start of server")

while True:
    try:
        socket.listen(NB_CLIENT)
        client, address = socket.accept()
        print("{} connected".format(address))
        response = client.recv(1024)
        if response != str():
            response = response.decode("utf-8")
            print(response)
            files = os.listdir("../videos/")
            for eachFile in files:
                if response in eachFile:
                    FILE_FOUND = True
                    binary_file = str()
                    print(eachFile.split(".")[0])
                    with open("../videos/"+eachFile, 'rb') as file_in:
                        for byte in iter(partial(file_in.read, 1), b''):
                           binary_file += format(ord(byte), '0>8b')
                    file = "key:" + eachFile.split(".")[0]+"+value:"+binary_file
                    client.send(bytes(file, "utf-8"))
            if not FILE_FOUND:
                client.send(b"File not found")


    except KeyboardInterrupt:
        print("End...")
        socket.close()
        sys.exit()


