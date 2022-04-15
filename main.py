






from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from serial_comunication import Comunication
import collections
import time


class Graph(Frame):
    def __init__(self, master, *args):
        super().__init__(master,*args)
        self.Font = ('Arial',12,'bold')
        self.data_arduino = Comunication()
        self.update_port()

        self.sample = 100
        self.data = 0.0

        self.fig, ax = plt.subplots(facecolor='#000000',dpi=100,figsize=(4,2))
        plt.title('Gaficar Datos de Arduino',color='white',size=12,family='Arial')
        ax.tick_params(direction='out',length=5,width=2,
            colors='white',
            grid_color='r',grid_alpha=0.5)

        self.line, = ax.plot([],[],color='m',marker='o',
            linewidth=2, markersize=1, markeredgecolor='m')
        
        self.line2, = ax.plot([],[],color='g',marker='o',
            linewidth=2, markersize=1, markeredgecolor='g')

        plt.xlim([0,self.sample])
        plt.ylim([-5,6])

        ax.set_facecolor('#6E6D7000')
        ax.spines['bottom'].set_color('blue')
        ax.spines['left'].set_color('blue')
        ax.spines['top'].set_color('blue')
        ax.spines['right'].set_color('blue')

        self.data_sign_one = collections.deque([0]*self.sample,maxlen=self.sample)
        self.data_sign_two = collections.deque([0]*self.sample,maxlen=self.sample)

        
        

        self.widgets()
        
    def on_closing(self):
        
        self.data_arduino.desconec()
        time.sleep(1.5)
        quit()
        
        

    def animate(self, i):
        #self.data_arduino.read_datas()
        
        self.datas = (self.data_arduino.data_received.get())
        data = self.datas.split(',')
        data1= float(data[0])
        data2= float(data[1])

        self.data_sign_one.append(data1)
        self.data_sign_two.append(data2)
        self.line.set_data(range(self.sample),self.data_sign_one)
        self.line2.set_data(range(self.sample),self.data_sign_two)
        #return self.line, self.line2

    def start(self,):
        self.ani = animation.FuncAnimation(self.fig, self.animate,
            interval=100, blit=False)
        self.bt_graph.config(state ='disable')
        self.bt_pause.config(state = 'normal')
        self.canvas.draw()

    def pause(self):
        self.ani.event_source.stop()
        self.bt_restart.config(state = 'normal')
    
    def restart(self):
        self.ani.event_source.start()
        self.bt_restart.config(state = 'disabled')

    def widgets(self):
        frame = Frame(self.master, bg='gray50', bd=2)
        frame.grid(column=0, columnspan=2, row=0, sticky='nsew')
        frame1= Frame(self.master, bg='black')
        frame1.grid(column=2,row=0,sticky='nsew')
        frame4= Frame(self.master, bg='black')
        frame4.grid(column=0,row=1,sticky='nsew')
        frame2= Frame(self.master, bg='black')
        frame2.grid(column=1,row=1,sticky='nsew')
        frame3= Frame(self.master, bg='black')
        frame3.grid(column=2,row=1,sticky='nsew')

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.rowconfigure(0, weight=5)
        self.master.rowconfigure(1, weight=1)

        self.canvas = FigureCanvasTkAgg(self.fig, master = frame)
        self.canvas.get_tk_widget().pack(padx=0,pady=0, expand=True, fill='both')

        self.bt_graph = Button(frame4, text='Graficar Datos',font=('Arial',12,'bold'),
            width=12, bg='purple4', fg='white', command=self.start)
        self.bt_graph.pack(pady=5, expand=1)
        self.bt_pause = Button(frame4, state='disabled', text='Pausar',font=('Arial',12,'bold'),
            width=12, bg='salmon', fg='white', command=self.pause)
        self.bt_pause.pack(pady=5, expand=1)
        self.bt_restart = Button(frame4, state='disabled', text='Reanudar',font=('Arial',12,'bold'),
            width=12, bg='green', fg='white', command=self.restart)
        self.bt_restart.pack(pady=5, expand=1)

        self.logo = PhotoImage(file='logo1.png')
        Label(frame2, text='Control Analogico', font=('Arial',15), bg='black', fg='white').pack(padx=5,expand=1)
        style = ttk.Style()
        style.configure('Horizontal.TScale',background='black')
        self.slider_one = ttk.Scale(frame2,command= self.data_slider_one, state='disabled', to = 255,
            from_=0, orient='horizontal', length=280, style='TScale')
        self.slider_one.pack(pady=5, expand=1)
        self.slider_two = ttk.Scale(frame2,command= self.data_slider_two, state='disabled', to = 255,
            from_=0, orient='horizontal', length=280, style='TScale')
        self.slider_two.pack(pady=5, expand=1)


        port = self.data_arduino.ports
        baud = self.data_arduino.baud_rates
        if len(port)==0:
            port=['ERRO']

        Label(frame1, text='Puerto COM',bg='black', fg='white', font=('Arial',12,'bold')).pack(pady=5, expand=1)
        self.combobox_port = ttk.Combobox(frame1, values=port, justify='center', width=12, font='Arial')
        self.combobox_port.pack(padx=0, expand=1)
        self.combobox_port.current(0)

        Label(frame1, text='Baudrates',bg='black', fg='white', font=('Arial',12,'bold')).pack(pady=0, expand=1)
        self.combobox_baud = ttk.Combobox(frame1, values=baud, justify='center', width=12, font='Arial')
        self.combobox_baud.pack(padx=20, expand=1)
        self.combobox_baud.current(3)

        self.bt_connect = Button(frame1, text='Conectar',font= self.Font,width=12, bg='green2',
            command= self.connect_serial)
        self.bt_connect.pack(pady=5, expand=1)

        self.bt_update = Button(frame1, text='Actualizar',font= self.Font,width=12, bg='magenta',
            command= self.update_port)
        self.bt_update.pack(pady=5, expand=1)

        self.bt_disconnect = Button(frame1, state='disabled', text='Desconectar',font= self.Font,width=12, bg='red2',
            command= self.disconnect_serial)
        self.bt_disconnect.pack(pady=5, expand=1)

        Label(frame3, image=self.logo, bg='black').pack(pady=5, expand=1)

    def update_port(self):
        self.data_arduino.available_ports()

    def connect_serial(self):
        
        self.bt_connect.config(state='disabled')
        self.bt_disconnect.config(state='normal')
        self.slider_one.config(state='normal')
        self.slider_two.config(state='normal')
        self.bt_graph.config(state='normal')
        self.bt_restart.config(state='disable')

        self.data_arduino.arduino.port = self.combobox_port.get()
        self.data_arduino.arduino.baudrate = self.combobox_baud.get()
        self.data_arduino.serial_conexion()

    def disconnect_serial(self):
        
        self.data_arduino.desconec()
        self.bt_connect.config(state='normal')
        self.bt_disconnect.config(state='disabled')
        self.bt_pause.config(state='disabled')
        self.slider_one.config(state='disabled')
        self.slider_two.config(state='disabled')
        
        try:
            self.ani.event_source.stop()
        except AttributeError:
            pass
        

    def data_slider_one(self, *args):
        data = '1,'+str(int(self.slider_one.get()))
        self.data_arduino.sent_data(data)
    
    def data_slider_two(self, *args):
        data = '2,'+str(int(self.slider_one.get()))
        self.data_arduino.sent_data(data)

#if __name__ == "__name__":
window = Tk()
window.geometry('742x535')
window.config(bg='gray30',bd=4)
window.wm_title('Grafica Arduino')
window.minsize(width=700,height=400)
window.call('wm','iconphoto',window._w,PhotoImage(file='logo.png'))
window.protocol("WM_DELETE_WINDOW", lambda:app.on_closing())
app= Graph(window)
app.mainloop()





      #app.on_closing()  







