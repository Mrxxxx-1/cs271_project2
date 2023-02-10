import socket
import threading, time
from sys import exit
import json
import random
from token_prob import random_unit

print("client")

usertable = {'A' : 10882, 'B' : 10884, 'C' : 10886, 'D' : 10888, 'E' : 10900} 
user = { ('192.168.0.167', 10882) : 'A', ('192.168.0.167', 10884) : 'B', ('192.168.0.167', 10886) : 'C', ('192.168.0.167', 10888) : 'D', ('192.168.0.167', 10900) : 'E'}
outgoingchannel = {'A' : ['B'], 'B' : ['A', 'D'], 'C' : ['B'], 'D' : ['A', 'B', 'C', 'E'], 'E' : ['B', 'D']}
snapshot = {'A' : {'Token' : False, 'B' : None, 'D' : None}, 'B' : {'Token' : False, 'A' : None, 'C' : None, 'D' : None, 'E' : None}, 'C' : {'Token' : False, 'D' : None}, 'D' : {'Token' : False, 'B' : None,'E' : None}, 'E' : {'Token' : False, 'D' : None}}
# incomingchannel = {'A' : 0, 'B' : 0, 'C' : 0, 'D' : 0, 'E' : 0}
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


g_token = False
g_probability = 0
g_tflag = 0
g_marker = 0

flag = True
channel = outgoingchannel[username]
lstatus = snapshot[username]
channelnum = len(lstatus) - 1

# print(channel)
# print(lstatus)
# print(len(lstatus) - 1)

def RECV():
    global g_token
    global g_probability
    global g_marker
    count = 0
    icount = 0 
    while flag:
      (data, addr) = s.recvfrom(1024)
      time.sleep(3)
      try :
            if isinstance(json.loads(data.decode('utf-8')), dict) :
                rev = {}
                rev = json.loads(data.decode('utf-8'))
                if rev.get('Token') :
                    icount += 1
                    print('Received snapshot from client %s' %(user[addr]))
                    snapshot[user[addr]] = rev
                    if icount == 4 :
                        print('Snapshot finished, show all status below:')
                        print(snapshot)
                        icount = 0
                        g_marker = 0
                        count = 0
                else :
                    if g_marker == 0 :
                        print('Received the first MARKER from client %s' %(user[addr]))
                        lstatus['Token'] = g_token
                        g_marker = 1
                        count += 1
                        for item in channel :
                            print('Send MAKER to client %s' %(item))
                            s.sendto(data, (HOST, usertable[item]))
                        print(count)
                        if count == (len(lstatus)-1) :
                            # lstatus1 = json.dumps(lstatus)
                            print('Send snapshot to initiator %s' %(rev['MAKER']))
                            # s.sendto(lstatus1.encode('utf-8'), (HOST, usertable[rev['MAKER']]))
                    else :
                        print('Received MARKER from client %s' %(user[addr]))
                        count += 1
                        print(count)
                        a = (count == (len(lstatus)-1))
                        print(a)
                        if a :
                            # lstatus1 = json.dumps(lstatus)
                            print('Send snapshot to initiator %s' %(rev['MAKER']))
                            # s.sendto(lstatus1.encode('utf-8'), (HOST, usertable[rev['MAKER']]))

      except :
        if g_marker == 1 :
            if data.decode('utf-8') == "Token" :
                if(random_unit(g_probability/100)) :
                    g_token = True
                    lstatus[user[addr]] = g_token
                    print('received token from client %s' %(user[addr]))
                    time.sleep(1)
                    t = random.randint(0, len(channel)-1)
                    print('Send token to client %s \n' %(channel[t]))
                    data = 'Token'
                    g_token = False
                    s.sendto(data.encode('utf-8'), (HOST, usertable[channel[t]]))
                else :
                    g_token = False
        else :
            if data.decode('utf-8') == "Token" :
                if(random_unit(g_probability/100)) :
                    g_token = True
                    print('received token from client %s' %(user[addr]))
                    time.sleep(1)
                    t = random.randint(0, len(channel)-1)
                    print('Send token to client %s \n' %(channel[t]))
                    data = 'Token'
                    g_token = False
                    s.sendto(data.encode('utf-8'), (HOST, usertable[channel[t]]))
                else :
                    g_token = False

def UI():
    global g_token
    global g_probability
    global g_marker
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
            snapshot[username]['Token'] = g_token
            # print(snapshot)
            data2 = {}
            data2['MARKER'] = username
            data22 = json.dumps(data2)
            g_marker = 1
            for item in channel :
                print('Send MAKER to client %s' %(item))
                s.sendto(data22.encode('utf-8'), (HOST, usertable[item]))


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