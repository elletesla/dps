import socket 
import ssl

host = "127.0.0.1"
port = 5000

context =ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_cert_chain(certfile="client.crt",keyfile="client.key")
context.check_hostname = False
context.load_verify_locations("ca.crt")
context.set_ciphers("ECDHE-RSA-AES256-SHA384")

with socket.create_connection((host,port)) as sock:
    print("Connected to Server")
    with context.wrap_socket(sock,server_hostname=host) as ssock:
        while True:
            num_contestants = int(input("Enter Number of Cntestants"))
            voters = int(input("Enter Number of Voters"))
            ssock.send(f"{num_contestants},{voters}".encode("utf-8"))
            for i in range(voters):
                while True:
                    try:
                        vote = int(input("Enter Vote "))
                        if 1<=vote<=num_contestants:
                            ssock.send(str(vote).encode("utf-8"))
                            break
                        else:
                            print("Valid Integer")
                    except ValueError:
                        print("Invalid")
            result = ssock.recv(1024).decode("utf-8")
            print(result)
            

            
            