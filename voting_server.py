import socket 
import ssl

host = "127.0.0.1"
port = 5000

context =ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server.crt",keyfile="server.key")
context.verify_mode= ssl.CERT_REQUIRED
context.load_verify_locations("ca.crt")
context.set_ciphers("ECDHE-RSA-AES256-SHA384")
with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
    sock.bind((host,port))
    print("Server Binded to HOST AND PORT")
    sock.listen(5)
    with context.wrap_socket(sock,server_side=True) as ssock:
        while True:
            conn,addr = ssock.accept()
            print("Connection RECVIEVD")
            with conn:
                data = conn.recv(1024).decode("utf-8")
                num_con, num_voters = map(int,data.split(","))
                votes = [0]*num_con
                for i in range(num_voters):
                    vote = int(conn.recv(1024).decode("utf-8"))
                    votes[vote-1]+=1
                max_votes = max(votes) if votes else 0
                winners = [i + 1 for i, v in enumerate(votes) if v == max_votes]
                if len(winners) == 1:
                    result = f"Winner is contestant {winners[0]} with {max_votes} votes."
                elif len(winners) > 1:
                    result = f"Tie between contestants {', '.join(map(str, winners))} with {max_votes} votes each."
                else:
                    result = "No votes cast."
                conn.send(result.encode("utf-8"))


        
                