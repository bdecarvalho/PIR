import socket as s

HOST ="192.168.43.145" # Must be changed with the real server IP address
PORT=25555
client= s.socket(s.AF_INET,s.SOCK_STREAM)
client.connect((HOST,PORT))
# cache = redis.Redis(host="127.0.0.1", port = 6379, db=0)

while True:
    message = input("Fichier à télecharger : ")
    # if cache.get(message) is not None:
    #     print("Got it in cache")

    client.send(message.encode('utf-8'))
    data=client.recv(4096)

    if(data):
        data = data.decode('utf-8').split("+")
        print(data[0].split(":")[1])
        print(data[1].split(":")[1])
        # cache.set(data[0].split(":")[1], data[1].split(":")[1])
        # print(cache.get(data[0].split(":")[1]))



