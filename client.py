import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import hashlib

import SPN

spn = SPN.spnSifreleme()

# reklendirme
init()

# renkler rastgele olarak bu renkler arasından seçiliyor.
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

client_color = random.choice(colors)

# serverın IP adresi
SERVER_HOST = "10.39.168.187"
SERVER_PORT = 4545 # serverın port numarası
separator_token = "<SEP>" 

s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

name = input("Enter your name: ")

def listen_for_messages():
	while True:

		SONUC="SPN" #Gönderilecek mesaj en başta spn olarak atanır.
		message = s.recv(1024).decode()
		message_reverse = message[::-1]
		message_to_list = [x for x in message_reverse[5:21]] #Mesajın içinden tarih isim gibi #ayıklanıp 16 bit kontrol ediliyor
		list_to_message= ""                                  #ayıklanıp 16 bit kontrol ediliyor
		for x in message_to_list:							 #eğer bu 16 bit içinde 0 ve 1 den başka değer varsa şifreleme
			if x!='0' and x!='1':                            #türü sha256 olarak ayarlanıyor.
				SONUC="not SPN"
				break
		if SONUC == "SPN":									#liste halinde incelediğimiz
			for x in message_to_list:
				list_to_message+=x
				
		if SONUC=="SPN":
			sifre_cozum = spn.SPN_DESIFRE(list_to_message[::-1]) #Mesajın içeriğini tesstten kontol etmek daha kolay geldiğinden
			print("\n" + message +" Sifrenin cozumlenmis hali: "+ sifre_cozum)#son olarak mesaj ters çevrilip yollanıyor.
		else:
			print("\n" + message)

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
	to_send =  input()
	text=""
	print(len(to_send))
	if len(to_send) == 16:
		text = spn.SPN(to_send)
	else:
		text = hashlib.sha256(to_send.encode()).hexdigest()

	if to_send.lower() == 'q':
		break

	date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	to_send = f"{client_color}[{date_now}] {name}{separator_token}{text}{Fore.RESET}"
	s.send(to_send.encode())

s.close()