







import serial, serial.tools.list_ports
from threading import Thread , Event
from tkinter import StringVar

class Comunication():
    def __init__(self, *args):
        super().__init__(*args)
        self.data_received = StringVar()
        
        self.arduino = serial.Serial()
        self.arduino.timeout = 0.5

        self.baud_rates = ['1200','2400','4800','9600','19200','38400','115200']
        self.ports = []

        self.sign = Event()
        self.my_thread = None
        self.conect = False
    
    def available_ports(self):
        self.ports = [port.device for port in serial.tools.list_ports.comports()]
    
    def serial_conexion(self):
        try:
            self.arduino.open()
        except:
            pass
        if (self.arduino.is_open):
            self.init_thread()
            self.conect = True
            print('Conet')

    def sent_data(self, data):
        if (self.arduino.is_open):
            self.datas = str(data)+'\n'
            self.arduino.write(self.datas.encode())
        else:
            print('Error')
    
    def read_datas(self):
        
        try:
            
            
            while(self.sign.isSet() and self.arduino.is_open):
                
                
                
                if self.conect:
                    data = self.arduino.readline().decode('utf-8').strip()
                else :
                    data = ''
                if(len(data)>1):
                    self.data_received.set(data)

            
        except TypeError:
            print('erros')
        
    
    def init_thread(self):
        print('thread')
        self.my_thread = Thread(target = self.read_datas,daemon=True)
        self.my_thread.setDaemon(1)
        self.sign.set()
        self.my_thread.start()
    
    def stop_thread(self):
        if(self.my_thread is not None):
            self.sign.clear()
            self.my_thread.join()
            self.my_thread = None
        
    
    def desconec(self):
        print('close')
        self.conect = False
        self.arduino.close()
        self.stop_thread()