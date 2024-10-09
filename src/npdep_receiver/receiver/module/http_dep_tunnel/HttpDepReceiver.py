import socket
from threading import *

from npdep_receiver.receiver.base.Receiver import Receiver
from npdep_receiver.receiver.module.http_dep_tunnel.HttpDepMessageProcessor import HttpDepMessageProcessor

class HttpDepReceiver(Receiver):
    def __init__(self, options, logger):
        super().__init__("HttpDepReceiver", options, logger)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread = Thread(target=self.handle)
        self.systemInfoMessages = []
        self.dataInfoMessages = []
        
    def start(self):
        self.socket.bind((self.options["ip"], self.options["port"]))                  
        self.socket.listen(5)
        self.thread.start()
                
    def handle(self):  
        self.logger.log(self.id + " started listening") 
        while self.isRunning:
            connection, address = self.socket.accept()
            self.logger.log(self.id + " accepted connection from: " + str(address)) 
            processor = HttpDepMessageProcessor(self.options, connection, self)
            processor.start()
            self.logger.log(self.id + " started processing from: " + str(address))