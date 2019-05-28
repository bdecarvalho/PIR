import socket
import sys
import os
import threading
from functools import partial


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def run(self): #cette fonction va gérer ce qu'on envoit et reçoit du client
   
        print("Connexion de %s %s" % (self.ip, self.port, ))

        response = self.clientsocket.recv(4096) #reçoit le message sur un buffer de 4096 bits

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
				eachFile.close()

		if not FILE_FOUND:
			client.send(b"File not found")
			
        
        print("Client déconnecté...")


NB_CLIENT  = 10
PORT = 25555
FILE_FOUND = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',PORT))


try:
	tabClients = {}
	n=0

	while True:
		s.listen(NB_CLIENT)
		print( "En écoute...")

		clientsocket, (ip, port)) = s.accept() #on repere une connexion
		
		tabClients[n] = clientsocket #on rentre dans le dictionnaire des clients

		newClientThread = ClientThread(ip, port, clientsocket) #on lance un thread pour gérer le client
		newClientThread.start()

		n+=1


except KeyboardInterrupt:
        print('Exiting...')
finally:
    for i in range(n):
        tabClients[i].close()
    print('je ferme les connexions')
    sys.exit()
    pass
