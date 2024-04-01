import socket
from tkinter import *
import tkinter
from threading import Thread

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('UTF-8')
            msg_list.insert(tkinter.END, msg)
        except:
            print("Error in receiving a message")
            break

def send():
    msg = my_msg.get()
    my_msg.set("")
    client.send(bytes(msg, 'UTF-8'))
    if (msg == '#quit'):
        client.close()
        window.quit()

def on_closing():
    my_msg.set("#quit")
    send()


window = Tk()
window.title ("Chat Room")
window.configure(bg="Light Grey")
msg_frame = Frame(window, height=100, width=100,bg = "Black")
my_msg = StringVar()
my_msg.set("")
scrollBar = Scrollbar(msg_frame)
msg_list = Listbox(msg_frame,height=50, width=100, bg = "White", yscrollcommand=scrollBar.set)
scrollBar.pack(side = RIGHT, fill = Y)
msg_list.pack(side=LEFT, fill = BOTH)
msg_list.pack()
msg_frame.pack()
button_label = Label(window, text= "Enter your text", fg = 'Light grey',bg = 'grey')
button_label.pack()
entryField = Entry(window, textvariable=my_msg,fg = 'Black',width = 50)
entryField.pack()
send_button = Button(window, text = "Send",bg='Green', font = "Aerial", fg = 'white', command=send)
send_button.pack()
quit_button = Button(window, text="Quit", bg = 'green', font = 'Aerial', fg = 'white', command=on_closing)
quit_button.pack()
window.protocol("WM_DELETE_WINDOW",on_closing)
host = '127.0.0.1'
port = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))
receive_thread = Thread(target=receive)
receive_thread.start()
mainloop()