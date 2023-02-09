import socket
import threading, time
from sys import exit
import json
import random

print("client")

usertable = {'A' : 10882, 'B' : 10884, 'C' : 10886, 'D' : 10888, 'E' : 10900} 
user = { ('192.168.0.167', 10882) : 'A', ('192.168.0.167', 10884) : 'B', ('192.168.0.167', 10886) : 'C', ('192.168.0.167', 10888) : 'D', ('192.168.0.167', 10900) : 'E'}
outgoingchannel = {'A' : ['B'], 'B' : ['A', 'D'], 'C' : ['B'], 'D' : ['A', 'B', 'C', 'E'], 'E' : ['B', 'D']}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True :
    username = input("Please input your username : ")
    if usertable.get(username) == None :
        print("wrong username!")
        continue
    break

PORT = usertable[username]
HOST = '192.168.0.167'
s.bind((HOST, PORT))

# s.sendto(username.encode('utf-8'), (HOST, 10888))
# time.sleep(3)

g_token = False
g_probability = 1
g_tflag = 0

flag = True
channel = outgoingchannel[username]

def RECV():
    global g_token
    global g_probability
    while flag:
      (data, addr) = s.recvfrom(1024)
      if data.decode('utf-8') == "Token" :
        g_token = True
        print('received token from client %s' %(user[addr]))
        time.sleep(1)
        t = random.randint(0, len(channel)-1)
        print('Send token to client %s \n' %(channel[t]))
        data = 'Token'
        g_token = False
        s.sendto(data.encode('utf-8'), (HOST, usertable[channel[t]]))

    #   try :
    #     if isinstance(json.loads(data.decode('utf-8')), dict) :
    #         rev = {}
    #         rev = json.loads(data.decode('utf-8'))
    #         # del trans['status']
    #         if rev.get('status') :
    #             # if chain == None:
    #                 # chain = BlockChain(1, data.decode('utf-8'))
    #             # else :
    #                 # chain.new_block(None, data.decode('utf-8'))
    #             g_time = max(g_time, int(rev[user[addr]]))
    #             g_time += 1
    #             print("Local Lamport time(%d)\n" %(g_time))
    #         elif rev['info'] == 'Transfer' :
    #             print('User(%s) is requesting a transfer' % (user[addr]))
    #             g_time = max(g_time, int(rev[user[addr]]))
    #             g_time += 1
    #             data2 ={}
    #             data2['info'] = "OK"
    #             data2[username] = g_time
    #             data22 = json.dumps(data2)
    #             s.sendto(data22.encode('utf-8'), addr)
    #             time.sleep(3)
    #         elif rev['info'] == "OK" :
    #             print('User(%s) agreed to the request' % (user[addr]))
    #             g_count += 1
    #             g_time = max(g_time, int(rev[user[addr]]))
    #             g_time += 1
    #             print("Local Lamport time(%d)\n" %(g_time))
    #             time.sleep(3)
    #   except : 
    #     if data.decode('utf-8') == "Denied" :
    #         g_flag = 0
    #     if data.decode('utf-8') == "Approved" :
    #         g_flag = 1
    #     print(data.decode('utf-8'))
    #     time.sleep(3)

def UI():
    global g_token
    global g_probability
    while True :
        print("1. Issue token")
        print("2. Start snapshot")
        print("3. Adjust token loss probability")
        print("0. Exit application")
        a = input("please insert command\n")
        if a == "0" :
            flag = False
            # to server
            break
        elif a == "1" :
            print('Issue token to local client')
            g_tflag = 1
            g_token = True
            time.sleep(1)
            t = random.randint(0, len(channel)-1)
            print('Send token to client %s \n' %(channel[t]))
            data = 'Token'
            g_token = False
            s.sendto(data.encode('utf-8'), (HOST, usertable[channel[t]]))


        elif a == "2" :
            print('Initiating a Snapshot')
            # for item in channel :
            #     print(item)
            print(len(channel))


        elif a == "3" :
            g_probability = input('Please enter token loss probability\n')
            g_probability = float(g_probability)
            print('Now client has a %.1f %% chance of losing the token' %(g_probability))
        time.sleep(1)
# UI()

t1 = threading.Thread(target=RECV)
t2 = threading.Thread(target=UI)

t1.start()
t2.start()
t1.join()
t2.join()