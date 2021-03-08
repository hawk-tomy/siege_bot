#!/usr/bin/env python
import socketio
import yaml
from logging import getLogger


from .data import data


logger = getLogger('sIO')
slogger = logger.getChild('sIO')
elogger = logger.getChild('eIO')
sio = socketio.Client(logger=slogger, engineio_logger=elogger)
data.sio = sio

with open('data/login.yaml')as f:
    login_data = yaml.safe_load(f)
with open('data/url')as f:
    url = f.read()
with open('data/event_list.yaml')as f:
    event_dict = yaml.safe_load(f)


def event_receiver(event):
    event_type = event_dict.get(event)
    if event_type == 'p2b':
        queue = data.add_p2b_event(event)

        def handler(json):
            logger.debug(json)
            queue.put_nowait(json)

    elif event_type == 'b2p':

        def handler(json):
            logger.debug(json)
            id_ = json.get('id')
            if data.is_b2p_id_in(id_):
                data.get_b2p_data_by_id(id_).put_nowait(json)

    else:
        raise ValueError(f'this event {event} is not found')
    return handler
[sio.on(e,event_receiver(e)) for e in event_dict]


@sio.event
def login(json):
    logger.info(json)
    sio.sleep(1)
    sio.emit('login',login_data)


@sio.event
def login_result(json):
    logger.info(json)
    if json.pop('status') != 'success':
        logger.info('login is failed')
        sio.disconnect()
    else:
        logger.info('login is success')


@sio.event
def connect():
    logger.info('connected to server')


@sio.event
def disconnect():
    logger.info('disconnected from server')


@sio.event
def message(msg):
    logger.info(msg)


def run():
    sio.connect(url, transports='websocket')
