#!/usr/bin/env python3
import threading
import os
import secrets
import argh
from airmash.client import Client

client = Client(enable_debug=True)


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

    def run(self):
        while not self.wait():
            if client.connected:
                client.key('LEFT', True)


def track_position(player, key, old, new):
    new = [int(x) for x in new]
    print("Position: {} {}".format(*new))


def track_rotation(player, key, old, new):
    print("Rotation: {}".format(new))


@client.on('LOGIN')
def on_login(client, message):
    print("Client has logged in!")
    print("Player ID: {}".format(client.player.id))
    client.player.on_change('position', track_position)
    client.player.on_change('rotation', track_rotation)


@client.on('PLAYER_HIT')
def on_hit(client, message):
    for player in message.players:
        if player.id == client.player.id:
            print("Uh oh! I've been hit!")


_mydir = os.path.realpath(os.path.dirname(__file__))
_hashfile = os.path.join(_mydir, '.hashes')
if not os.path.exists(_hashfile):
    print(secrets.token_hex(nbytes=2), file=open(_hashfile, 'w'))
_hash = open(_hashfile).read().strip()


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
        enable_trace=False
    )
    _t_update.stop()
    _t_update.join()


if __name__ == '__main__':
    argh.dispatch_command(run)
