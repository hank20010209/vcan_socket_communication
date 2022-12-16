import socket
from tkinter.messagebox import showinfo
import can
from time import sleep
import sys
from PIL import ImageTk
from tkinter import *
import tkinter as tk
from tkinter import *

try:
    from PIL import Image
except ImportError:
    import Image

HOST = sys.argv[1]
PORT = 7000
server_addr = (HOST, PORT)
##from sys import exit

class Application:
    def __init__(self, master):
        self.master=master
        master.configure(bg="white")
        master.title("Welcome To HackerSir")
        master.geometry('1300x400')
        master.resizable(False, False)
        buttonstart = tk.Button(master, text = "Start", fg = "white", command = self.start)
        buttonstart.configure(bg='black')
        buttonstart.grid(row = 1, column = 0)

        buttonquit = tk.Button(master, text = "Quit", fg = "white", command=self.quitit)
        buttonquit.configure(bg='black')
        buttonquit.grid(row = 1, column = 2)

        image = ImageTk.PhotoImage(Image.open("./img/P1.png"))
        label = tk.Label(image=image)
        label.photo = image   # assign to class variable to resolve problem with bug in `PhotoImage`
        label.grid(row=100, column = 0, rowspan=20, columnspan=3)

        # self.timertext = tk.DoubleVar()
        # self.timertext.set(0)
        # display = tk.Label(master, textvariable = self.timertext)
        # display.grid(row = 0, column = 0)
##        timertext.set(timertext)  ## Huh!!
        self.timeit=False

    def main_client(self):
        # ctr=int(self.timertext.get())
        # self.timertext.set(ctr+1)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bus = can.Bus(channel='vcan0', interface='socketcan')

        message = bus.recv()
        d=message.data
        data=[]
        while len(d) != 0:
            data.append(d.pop())
        msg = f'{message.arbitration_id}:{message.dlc}:{data[::-1]}'
        print('sendto ' + str(server_addr) + ': ' + msg)
        
        s.sendto(msg.encode(), server_addr)
        # sleep(1)

        # indata, addr = s.recvfrom(1024)
        # print('recvfrom ' + str(addr) + ': ' + indata.decode())
        if self.timeit:
            self.master.after(1, self.main_client)

    def start(self):
        showinfo("Start Hacking", "Start Hacking")
        self.timeit=True
        self.main_client()

    def quitit(self):
        showinfo("Stop Hacking", "Stop Hacking")
        self.timeit=False

root = tk.Tk()

# frame = Frame(root, width=1920, height=1080)
# frame.pack()
# frame.place(anchor='center', relx=0, rely=0)

# # Create an object of tkinter ImageTk
# img = ImageTk.PhotoImage(Image.open("./img/P1.png"))

# # Create a Label Widget to display the text or Image
# label = Label(frame, image = img)
# label.pack(side = "bottom", fill = "both", expand = "yes")
app = Application(root)
root.mainloop()


# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bus = can.Bus(channel='vcan0', interface='socketcan')

# while True:
#     message = bus.recv()
#     d=message.data
#     data=[]
#     while len(d) != 0:
#         data.append(d.pop())
#     msg = f'{message.arbitration_id}:{message.dlc}:{data[::-1]}'
#     print('sendto ' + str(server_addr) + ': ' + msg)
    
#     s.sendto(msg.encode(), server_addr)
#     # sleep(1)

#     # indata, addr = s.recvfrom(1024)
#     # print('recvfrom ' + str(addr) + ': ' + indata.decode())
