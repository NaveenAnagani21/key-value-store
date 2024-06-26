import socket
from store.kvstore import kvstore

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.store = kvstore()  # Create an instance of  data store

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)  # Listen for up to 5 connections

        print("Server started on", self.host, ":", self.port)

        while True:
            conn, addr = server_socket.accept()  # Accept a new connection
            print("Connected by", addr)
            buffer=bytearray()
            with conn:
                while True:
                    data=conn.recv(1024)


                    buffer.extend(data)

                    if b'\n' in buffer:
                        command=buffer.decode('utf-8').rstrip('\n')
                        buffer.clear()
                        print("command=",command)
                        response=self.handle_client_command(command,conn)
                        if command[0]!='q':
                            conn.sendall(response.encode())
              

    def handle_client_command(self, command, conn):
        clist=command.split()
        print("clist[0]=",clist[0])
        if clist[0].lower()=='set':
            if len(clist) != 3:
                return "ERR: Invalid number of arguments for SET\n"
            self.store.set(clist[1], clist[2])
            return "OK\n"
        elif clist[0].lower() == 'get':
            if len(clist) != 2:
                return "ERR: Invalid number of arguments for GET\n"
            if self.store.isin(clist[1]):
                return self.store.get(clist[1])+"\n"
            return f"{clist[1]} is not found in store \n"
        elif clist[0].lower() == "delete":
            if len(clist) !=2:
                return "ERR : Invalid number of arguments for DELETE\n"
            if  self.store.isin(clist[1]):
                self.store.remove(clist[1])
                return f"deleted {clist[1]}\n"
            else:
                return f"{clist[1]} is not found in store\n"
            
        elif clist[0].lower() == "q":
            resp='your session got terminated\n'
            conn.sendall(resp.encode())
            conn.close()
          

        else:
            return "ERR: Unknown command\n"

if __name__ == "__main__":
    server = Server("localhost", 6379) 
    server.start()
