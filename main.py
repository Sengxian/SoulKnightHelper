import socket

PORT = 23333

def startRelayServer(players):
    hostRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostRecv.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST or socket.SO_REUSEADDR, 1)
    
    try:
        hostRecv.bind(("", PORT))
    except Exception as e:
        print("Port has been occupied, please run the script before hosting the game.")
        return
    
    players = [player for player in players if player != ""]
    socks = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for i in players]
    print("Relay server started, now host your game.")

    while True:
        for i in range(len(players)):
            hostData, hostAddr = hostRecv.recvfrom(1024)
            if len(hostData) > 0 and hostAddr[0] not in players:
                socks[i].sendto(hostData, (players[i], PORT))
                print(f"Broadcast package received, sending to {players[i]}.")

if __name__ == "__main__":
    players = ["10.8.0.3", "10.8.0.4", ""] # 不足三个则留空
    startRelayServer(players)
    
