#!/usr/bin/python3
import os
from airmash import packets
from airmash.player import Player
from airmash.mob import Mob
from airmash.country import COUNTRY_CODES
from airmash import games
from airmash.client import Client
import random
import websocket
import threading
import time
import names

_mydir = os.path.realpath(os.path.dirname(__file__))

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
FIRE = 'FIRE'
SPECIAL = 'SPECIAL'

client = Client(enable_debug=True)

def rare():
    return random.randrange(0, 10) == 0

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._event = threading.Event()

    def stop(self):
        self._event.set()

    def wait(self, timeout=1):
        return self._event.wait(timeout=timeout)


class ClientUpdate(StoppableThread):
    def __init__(self, *args, **kwargs):
        StoppableThread.__init__(self, *args, **kwargs)
        self.keyProbs = {}
        keys = [None, None, UP, UP, UP, UP, DOWN, LEFT, RIGHT, FIRE, FIRE, FIRE, SPECIAL]
        for i in set(keys):
            self.keyProbs[i] = []
            for j in keys:
                for k in range(random.randrange(0, 3)):
                    self.keyProbs[i].append(j)
        print(self.keyProbs)

    def send_keydown(self, key):
        client.key(key=key, state=True)

    def send_keyup(self, key):
        client.key(key=key, state=False)

    def run(self):
        while not self.wait():
            if client.connected:
                break
        packet = packets.build_player_command('COMMAND', com='respawn', data=str(random.randrange(1, 6)))
        client.send(packet)
        if False:  # rare():
            packet = packets.build_player_command('CHAT', text="All hail the robot overlords!")
            client.send(packet)
        self.wait(2)

        lastKey = None
        pressedKeys = []
        while not self.wait(random.randrange(1, 8) / 4.):
            key = random.choice(self.keyProbs[lastKey])
            #print("sending ", key)
            lastKey = key
            if key is None:
                continue
            if key in pressedKeys:
                self.send_keyup(key)
                pressedKeys.remove(key)
            else:
                self.send_keydown(key)
                pressedKeys.append(key)
            my_status = players[me].status
            #print("Status: {}".format(my_status))
            #print("Position: {}:{}".format(me.posX, me.posY))


@client.on('LOGIN')
def on_login(client, message):
    print("Client has logged in!")

def run(name=None, flag='GB', region='eu', room='ffa1', enable_trace=False):
    if name is None:
        name = names.get_full_name()
    print('name = {}'.format(name))
    _t_update = ClientUpdate()
    _t_update.start()
    
    client.connect(
        name=name,
        flag=flag,
        region=region,
        room=room,
        enable_trace=True
    )
    
    _t_update.stop()
    _t_update.join()

if __name__ == '__main__':
    argh.dispatch_command(run)
