import socket
import os
import time
import progressbar


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
    # Connect to server by getting ip and port from user

    def connect_to_server(self):
        self.target_ip = input('Enter ip --> ')
        self.target_port = input('Enter port --> ')

        self.s.connect((self.target_ip, int(self.target_port)))

        self.main()
    # reconnect to the server

    def reconnect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.target_ip, int(self.target_port)))
    # main function servers the files to the client

    def main(self):
        while 1:
            files = (self.s.recv(1024).decode()).split(" ")
            print("Files available in the server")
            for i in files:
                print("-->"+i)
            file_name = input('Enter file name on server --> ')
            if(file_name == "[bye]"):
                self.s.send(file_name.encode())
                print("Terminaing Connection")
                time.sleep(1)
                exit()
            self.s.send(file_name.encode())

            confirmation = self.s.recv(3)
            # print(confirmation)
            if confirmation == b"nos":
                print("File doesn't exist on server.")

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()

            else:
                write_name = 'from_server '+file_name
                if os.path.exists(write_name):
                    os.remove(write_name)

                with open(write_name, 'wb') as file:
                    while 1:
                        data = self.s.recv(2048)
                        # print(data)
                        file.write(data)
                        if not data:
                            print("Completed")
                            break

                print(file_name, 'successfully downloaded.')

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()


# Main driver
client = Client()
