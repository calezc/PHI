
import zmq
from tkinter import filedialog
from tkinter import messagebox

def parseCSV(file_path):
    result = []
    with open(file_path, "r") as infile:
        for line in infile:
            if len(line) >= 12:
                event = {
                    "start date": None,
                    "amount": None,
                    "frequency": None,
                    "end date": None
                }
                words = line.split(sep=",")
                if words[-1][-1:] == "\n":
                    words[-1] = words[-1][:-1]
                event["start date"] = words[0]
                event["amount"] = float(words[1])
                if len(words) > 2 and words[2] != "0" and words[2] != "":
                    event["frequency"] = int(words[2])
                if len(words) > 3 and words[3] != "0" and words[3] != "":
                    event["end date"] = words[3]
                result.append(event)

    return result

def LoadCSV():
    file_path = filedialog.askopenfilename(title="Load CSV", filetypes=[("CSV", "*.csv")])
    if file_path != "":
        try:
            event_list = parseCSV(file_path)
        except:
            message = "Error loading CSV.  Please check file format and try again."
            messagebox.showinfo(title="Error", message=message)
            LoadCSV()
        return event_list
    else:
        return None


# SOCKET SETUP

# Create context
context = zmq.Context()

#  Connect to "UI" microservice socket (5003)
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5003")

while True:
    request = socket.recv_string()

    event_list = LoadCSV()

    socket.send_json(event_list)