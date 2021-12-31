import socket
from threading import Thread

# Serverın IP ADRESİ
SERVER_HOST = "10.39.168.187"
SERVER_PORT = 4545 # PORT numarası
separator_token = "<SEP>" # client adı ve mesajını ayırmak için kullanılan token

# bağlanan kullanıcıların soket bilgisi tutuluyor
client_sockets = set()
# TCP soketi yaratılıyor
s = socket.socket()
# soketler tekrar kullanılabilir olarak ayarlanıuor
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# belirlediğimiz port ve ip numarası adres olarak ayarlanıyor.
s.bind((SERVER_HOST, SERVER_PORT))
# gelen istekler dinleniyor max 5 bağlantı
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # kullanıcının artık bağlı olmadığını gösterir.
            # setten kaldırılıyor.
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # gelen mesajda belirttiğimiz tokeni : ile değiştiriyoruz  
            # daha iyi görüntü için
            msg = msg.replace(separator_token, ": ")
        # bütün soketler geziliyor
        for client_socket in client_sockets:
            # ve mesaj gönderiliyor.
            client_socket.send(msg.encode())

while True:
    # while true içinde sürekli olarak dinlenmeye devam ediyor.
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # yeni bağlantı soketlere ekleniyor
    client_sockets.add(client_socket)
    # thread yapısında tutulmasının sebebi aynı anda birden çok işlemi yapabilmek
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

# client socketler kapanıyor (eğer döngüden çıkılırsa)
for cs in client_sockets:
    cs.close()
# ve server socket kapanıyor.
s.close()