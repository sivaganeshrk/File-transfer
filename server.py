import socket
import os


class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accept_connections()
    #Convert the given list into string divided by space
    def listtostring(self, s):
        str1 = " "
        return (str1.join(s))
    #Create server and Allow client to connect to the server
    def accept_connections(self):
        ip = socket.gethostbyname("localhost")  # socket.gethostname()
        port = int(input('Enter desired port --> '))

        self.s.bind((ip, port))
        self.s.listen(100)
        self.loop_forever = True
        print('Running on IP: '+ip)
        print('Running on port: '+str(port))
        # print(os.listdir("./Files/"))
        files = self.listtostring(os.listdir("./Files/"))
        print("Available files")
        for i in files.split(" "):
            print("-->"+i)
        while self.loop_forever:
            try:
                c, addr = self.s.accept()
                c.send(files.encode())
                print("Connection made with "+addr[0])
                self.handle_client(c, addr)
            except KeyboardInterrupt:
                self.loop_forever = False
                exit(0)
    #Send the file to the client
    def handle_client(self, c, addr):
        data = c.recv(1024).decode()
        if(data == '[bye]'):
            print("Connection Terminated")
            exit()
        path = "./Files/" + data
        if not os.path.exists(path):
            c.send("nos".encode())

        else:
            c.send("yes".encode())
            print('Sending', path)
            if data != '':
                file = open(path, 'rb')
                data = file.read(2048)
                while data:
                    c.send(data)
                    data = file.read(2048)

                c.shutdown(socket.SHUT_RDWR)
                c.close()

#Main driver 
server = Server()
