from asyncio import Queue
import yaml


class Config:
    def __init__(self,config):
        self.config = config


class Data:
    def __init__(self,data):
        #4 sIO p2b event
        self.__event_dict = {}
        #4 sIO b2P event
        self.__wait_events = {}
        self.__latest_id = 0
        #other data
        self.__sio = None
        self.data = data

    def add_p2b_event(self,event):
        queue = Queue()
        self.__event_dict[event] = queue
        return queue

    def get_p2b_events(self):
        return list(self.__event_dict.keys())

    def get_p2b_event_queue(self,event):
        return self.__event_dict.get(event)

    def add_b2p_event(self):
        self.__latest_id += 1
        queue = Queue()
        self.__wait_events[self.__latest_id] = queue
        return self.__latest_id, queue

    def get_b2p_data_by_id(self,id_):
        return self.__wait_events.pop(id_)

    def is_b2p_id_in(self,id_):
        return id_ in self.__wait_events

    @property
    def sio(self):
        return self.__sio

    @sio.setter
    def set_sio(self,value):
        self.__sio = value


with open('config.yaml')as f:
    raw_config = yaml.safe_load(f)
with open('data/data.yaml')as f:
    raw_data = yaml.safe_load(f)
conig = Config(raw_config)
data = Data(raw_data)
