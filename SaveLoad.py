
import zmq
from tkinter import filedialog
import json

# Save Profile
def SaveProfile(user_data):
    file_path = filedialog.asksaveasfilename(title="Save Profile", defaultextension=".phi",
                                         filetypes=[("PHI", "*.phi")])

    if file_path != "":
        with open(file_path, "w") as outfile:
            json.dump(user_data, outfile)
        return user_data
    else:
        return ""


# Load Profile
def LoadProfile():
    file_path = filedialog.askopenfilename(title="Load Profile", filetypes=[("PHI", "*.phi")])
    if file_path != "":
        with open(file_path, "r") as infile:
            return json.load(infile)
    else:
        return ""


# SOCKET SETUP

# Create context
context = zmq.Context()

#  Connect to "UI" microservice socket (5002)
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5002")

while True:
    request = socket.recv_json()

    request_type = request[0]
    user_data = request[1]

    if request_type == "save":
        user_data = SaveProfile(user_data)
    else:
        user_data = LoadProfile()

    socket.send_json(user_data)