
from tkinter import messagebox
import zmq

# SOCKET SETUP

# Create context
context = zmq.Context()

#  Connect to "UI" microservice socket (5004)
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5004")

while True:
    page = socket.recv_json()

    date, amount = page
    amount = "{:,.2f}".format(amount)
    title = "************* NEGATIVE ASSETS WARNING *************"
    message = f"YOUR PROJECTED ASSETS WILL DROP BELOW $0 ON {date} BY ${amount} (USD)!!!!!"
    messagebox.showinfo(title=title, message=message)

    socket.send_string("Complete")