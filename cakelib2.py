import html.parser
import random
import re
import select
import socket
import threading
import sys
import time
import urllib.request
import urllib.parse

w12 = 75
sv2 = 95
sv4 = 110
sv6 = 104
sv8 = 101
sv10 = 110
sv12 = 116

tagserver_weights = [["5", w12], ["6", w12], ["7", w12], ["8", w12], ["16", w12], ["17", w12], ["18", w12], ["9", sv2], ["11", sv2], ["12", sv2], ["13", sv2], ["14", sv2], ["15", sv2], ["19", sv4], ["23", sv4], ["24", sv4], ["25", sv4], ["26", sv4], ["28", sv6], ["29", sv6], ["30", sv6], ["31", sv6], ["32", sv6], ["33", sv6], ["35", sv8], ["36", sv8], ["37", sv8], ["38", sv8], ["39", sv8], ["40", sv8], ["41", sv8], ["42", sv8], ["43", sv8], ["44", sv8], ["45", sv8], ["46", sv8], ["47", sv8], ["48", sv8], ["49", sv8], ["50", sv8], ["52", sv10], ["53", sv10], ["55", sv10], ["57", sv10], ["58", sv10], ["59", sv10], ["60", sv10], ["61", sv10], ["62", sv10], ["63", sv10], ["64", sv10], ["65", sv10], ["66", sv10], ["68", sv2], ["71", sv12], ["72", sv12], ["73", sv12], ["74", sv12], ["75", sv12], ["76", sv12], ["77", sv12], ["78", sv12], ["79", sv12], ["80", sv12], ["81", sv12], ["82", sv12], ["83", sv12], ["84", sv12]]
specials = {'mitvcanal': 56, 'magicc666': 22, 'livenfree': 18, 'eplsiite': 56, 'soccerjumbo2': 21, 'bguk': 22, 'animachat20': 34, 'pokemonepisodeorg': 55, 'sport24lt': 56, 'mywowpinoy': 5, 'phnoytalk': 21, 'flowhot-chat-online': 12, 'watchanimeonn': 26, 'cricvid-hitcric-': 51, 'fullsportshd2': 18, 'chia-anime': 12, 'narutochatt': 52, 'ttvsports': 56, 'futboldirectochat': 22, 'portalsports': 18, 'stream2watch3': 56, 'proudlypinoychat': 51, 'ver-anime': 34, 'iluvpinas': 53, 'vipstand': 21, 'eafangames': 56, 'worldfootballusch2': 18, 'soccerjumbo': 21, 'myfoxdfw': 22, 'animelinkz': 20, 'rgsmotrisport': 51, 'bateriafina-8': 8, 'as-chatroom': 10, 'dbzepisodeorg': 12, 'tvanimefreak': 54, 'watch-dragonball': 19, 'narutowire': 10, 'leeplarp': 27}

####
# cakelib2
####

'''
(C) Copyright 2014 Riyoken:

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

version: Sexy (INCOMPLETE)
'''

####
# constants
####

uids = dict()
lastmsg = dict()

def regex(pattern, x, default): return re.search(pattern, x).group(1) if re.search(pattern, x) else default
def unescape(text): return html.parser.HTMLParser().unescape(text)
def escape(text): return ''.join(['&#%s;' % ord(x) for x in text])

def call(classname, function, *values):
    if hasattr(classname, function):
        getattr(classname, function) (*values)

def server(group):
    try:  sn = str(specials[group])
    except KeyError:
        group = re.sub('[-_]', 'q', group)
        lcv8 = max(int(group[6:9], 36), 1000) if len(group) > 6  else 1000
        num = (int(group[:5], 36) % lcv8) / lcv8
        cake, s_number = 0, 0
        for x in tagserver_weights:
          cake += float(x[1]) / sum(a[1] for a in tagserver_weights)
          if(num <= cake) and s_number == 0:
            s_number += int(x[0])
        sn = s_number
    return "s{}.chatango.com".format(sn)

def Auth(user, password): 
    data = urllib.parse.urlencode({"user_id": user, "password": password, "storecookie": "on", "checkerrors": "yes"}).encode()
    return regex('auth.chatango.com=(.*?);', urllib.request.urlopen("http://chatango.com/login", data).getheader('Set-Cookie'), None)

def anon_id(_id, uid):
    return ''.join([str((
        int(uid[4:][i][-1]) + int((_id if (_id != None and len(_id) == 4) else '3452')[i][-1])
        )% 10) for i in range(4)])

def gUser(user, alias, uid, _id):
    if user == '': user = 'None'
    if user == 'None':
        if alias == 'None':
            user = '@anon'+anon_id(_id, uid)        
        else: user = '$'+alias
    return User(**{'name': user.lower(), 'uid': uid})

def clean(msg):
    font_tag = regex('<f (.*?)>', msg.content, '000')
    name_tag = regex('<n(.*?)/>', msg.content, '000')
    msg.user.fSize = regex('x(.*?)=', font_tag, '12')[0:2]
    msg.user.fColor = regex('x%s(.*?)=' % msg.user.fSize, font_tag, '000')[0:3]
    msg.user.fFace = regex('="(.*?)"', font_tag, '0')
    msg.user.nColor = name_tag[0:3]
    msg.content = unescape(re.sub('<(.*?)>', '', msg.content))
    return msg

####
# cake
####

class newObject(object):

    def __init__(self, **kw):
        [setattr(self, x, kw[x]) for x in kw]
        self.object_ret()

    def object_ret(self): return self

####
# chat class
####

class Chat:

    def __init__(self, **kw):
        [setattr(self, x, kw[x]) for x in kw]

        self.connect()

    def connect(self):
        self.cumsock = socket.socket()
        self.cumsock.connect((self.server, self.port))
        self.ping = self.main.timer(35, self.main.ping, self)
        self.login()

    def send(self, *x):
        data = ':'.join(x).encode()
        byte = b'\x00' if self.ready else b'\r\n\x00'
        self.wbyte += data+byte

    def login(self):
        self.send('bauth', self.chatname, self.id, self.user, self.password)
        self.ready = False

    def post(self, msg):
        if len(msg) > 2500:
            message, rest = msg[:2500], msg[:2500]
            self.send('bmsg', 'fuck', message)
            self.post(rest)
        else:
            self.send('bmsg', 'fuck', msg)
    
####
# user class
####

class User:

    def __init__(self, **kw):
        [setattr(self, x, kw[x]) for x in kw]

####
# pm class
####

class Pm:
  
    def __init__(self, **kw):
        [setattr(self, x, kw[x]) for x in kw]
        self.connect()

    def connect(self):
        self.cumsock = socket.socket()
        self.cumsock.connect((self.server, self.port))
        self.ping = self.main.timer(35, self.main.ping, self)
        self.login()

    def login(self):
        self.send('tlogin', self.auth, '2')
        self.ready = False

    def send(self, *x):
        data = ':'.join(x).encode()
        byte = b'\x00' if self.ready else b'\r\n\x00'
        self.wbyte += data+byte

    def say(self, user, x):
        self.send('msg', user, x.replace('<', '[').replace('>',']')) 
      

####
# event handler
####

class Interpret:
    
    def __init__(self, main):
        self.main = main

    def lemonize(self, data, net):
        data = [x.split(':') for x in data.decode('utf-8').split('\r\n\x00')]
        [self.event_call(x[0],x[1:], net) for x in data]

    def event_call(self, event, data, net):
        event = '_'+event
        if hasattr(self, event):
            getattr(self, event)(data, net)

    def _ok(self, data, net):
        net.chatInfo = newObject(**{
            'mods': data[6].split(';'),
            'owner': data[0],
            'history': list(),
            'nomore': 1
          })

    def _inited(self, data, net):
        print('connected sucessfully to '+ net.chatname)
        init = [['g_participants', 'start'],
               ['blocklist', 'block', '', 'next', '500'],
               ['blocklist', 'unblock', '', 'next', '500'],
               ['getbannedwords'],
               ['getpremium', '1'],
               ['msgbg', '1']]
        net.gHistory = self.main.timer(0.1, net.send, 'get_more', '35')
        [net.send(x[0], *x[1:]) for x in init]

    def _g_participants(self, data, net):
        data = [x.split("%") for x in "%".join(data).split(";")]
        y = []
        for x in data:
            info = newObject(**{
              'user': gUser(x[3], x[4], x[2], str(x[1]).split('.')[0][-4:]),
              'sid': x[0],
              'joinTime': x[1]
              })
            y.append(info)
        net.chatInfo.pData = y
        net.chatInfo.userlist = [x.user.name for x in net.chatInfo.pData] 

    def _participant(self, data, net):
        ctype = data[0]
        pUser = newObject(**{
            'user': gUser(data[3], data[4], data[2], str(data[6].split('.')[0][-4:])),
            'joinTime': data[6],
            'uid': data[2],
            'sid': data[1]
          })
        y = [x for x in net.chatInfo.pData if x.sid == pUser.sid]
        if ctype == '0': net.chatInfo.pData.remove(y[0])
        elif ctype == '1': net.chatInfo.pData.append(pUser)
        elif ctype == '2':
            net.chatInfo.pData.remove(y[0])
            net.chatInfo.pData.append(pUser)
        net.chatInfo.userlist = [x.user.name for x in net.chatInfo.pData]

    def _mods(self, data, net):
        net.chatInfo.mods = data

    def _n(self, data, net):
        net.chatInfo.userCount = int(data[0], 16)

    def _nomore(self, data, net):
        try:
            net.gHistory.set()
            if hasattr(net, 'gHistory'):
                delattr(net, 'gHistory')
        except: 'cake' == 'cake'        

    def _i(self, data, net):
        _id = re.search("<n(.*?)/>", ':'.join(data[9:]))
        if _id: _id = _id.group(1)
        hist = newObject(**{
            'user': gUser(data[1], data[2], data[3], _id),
            'cid': data[4],
            'uid': data[3],
            'time': data[0],
            'sid': data[5],
            'ip': data[6],
            'content': ':'.join(data[9:]),
            'room': net
          })
        net.chatInfo.history.append(clean(hist))            

    def _b(self, data, net):
        _id = re.search("<n(.*?)/>", ':'.join(data[9:]))
        if _id: _id = _id.group(1)
        msg = newObject(**{
            'user': gUser(data[1], data[2], data[3], _id),
            'room': net,
            'uid': data[3],
            'id': data[4],
            'time': data[0],
            'ip': data[6],
            'content': ':'.join(data[9:]),
            'u_id': None
            })
        net.Message = clean(msg)
        
    def _u(self, data, net):
        net.Message.u_id = data[1]
        lastmsg[net.Message.user.name] = [net.Message.content, net.Message.room.chatname, net.Message.time]
        call(self.main, 'onMessage', net.Message.user, net.Message.room, net.Message)

    def _msg(self, data, net):
        msg = newObject(**{
            'user': data[0],
            'content': unescape(re.sub("<(.*?)>", "", data[5])),
            'time': data[3]
          })
        call(self.main, 'onPm', msg.user, msg, net)
          
          
####
# main class
####

class Main:

    def __init__(self):
        self.connections = dict()
        self.interpret = Interpret(self)
        self.pm = None
        self.user = None
        self.password = None
        self.ready = True
        self.tasks = list()

    def joinChat(self, x):
        if x not in self.connections.keys():
            self.connections[x] = Chat(**{
                'chatname': x,
                'port': 443,
                'server': server(x),
                'wbyte': b'',
                'id': str(random.randrange(10**15, 10**16)),
                'main': self,
                'ready': True,
                'password': self.password,
                'user': self.user,
                'chatInfo': None
                })
            return True
        else: return False

    def gConnections(self):
        return [x for x in self.connections.values()]

    def gChats(self):
        return [x for x in self.gConnections() if x.cumsock.getpeername()[1] == 443]

    def gChat(self, chat):
        return [x for x in self.gChats if x.chatname == chat.lower()][0]

    def gLastmsg(self):
        time.sleep(10)
        hist = [x.chatInfo.history[::-1] for x in self.gChats()]
        for i in hist:
            for x in i: lastmsg[x.user.name] = [x.content, x.room.chatname, x.time]
        print('loaded chat history to lastmsg')
        return True
    
    def timer(self, seconds, function, *var):
        event = threading.Event()
        def decorator(*var):
            while not event.wait(seconds): function(*var)
        threading.Thread(target = decorator, args = (var), daemon = True).start()
        self.tasks.append(event)
        return event

    def ping(self, var):
            var.send('')

    @classmethod
    def start(bot, user = None, password = None, chats = None, pm = None, debug = False, default = None):
        self = bot()
        chats = default if debug and defalut != None else chats
        if type(chats) == str: chats = chats.split()
        self.user = user
        self.password = password
        [self.joinChat(x) for x in chats]
        if pm == True:
          self.pm = Pm(**{
            'main': self,
            'port': 5222,
            'auth': Auth(self.user, self.password),
            'wbyte': b'',
            'ready': True,
            'server': 'c1.chatango.com'
            })
          self.connections['pm'] = self.pm
          threading.Thread(target=self.gLastmsg, daemon = True).start()
        self.matrix()

    def onInit(self):
        pass

    def matrix(self):
        self.onInit()
        read_byte = b''
        self.cake = True
        while self.cake:
            connections = self.gConnections()
            rsock = [x.cumsock for x in connections]
            wsock = [x.cumsock for x in connections if x.wbyte != b'']
            read_sock, write_sock, errors = select.select(rsock, wsock, [], 0.1)
            for i in read_sock:
                net = [x for x in connections if x.cumsock == i][0]
                while not read_byte.endswith(b'\x00'):
                    read_byte += i.recv(1024)
                self.interpret.lemonize(read_byte, net)
                read_byte = b''
            for i in write_sock:
                net = [x for x in connections if x.cumsock == i][0]
                i.send(net.wbyte)
                net.wbyte = b''            

    def stop(self):
        self.cake = False
        [x.set() for x in self.tasks]
