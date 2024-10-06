
# importing libraries

import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
import json
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5005")

while True:
    #  Wait for next request from client
    received = socket.recv()
    received = received.decode("utf-8")
    print("Received reply [ %s ]" % (received))
    try:
        json_received = json.loads(received)
    except json.JSONDecodeError:
        socket.send(b"Error - Invalid JSON.")

    #  Do some 'work'
    time.sleep(1)
    for key in json_received:
        if key == "start":
            start_date = json_received[key]
        if key == "end":
            end_date = json_received[key]
        if key == "assets":
            assets_array = json_received[key]

    # Converting strings to dates
    start_string = start_date
    end_string = end_date
    start_date = datetime.datetime.strptime(start_string, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_string, '%Y-%m-%d').date()

    # Finding all dates between two dates and putting them into an array
    delta = end_date - start_date

    date_array = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        date_array.append(day)

    # Array of dates for x axis
    x = date_array

    # Array of ints for y axis
    y = assets_array

    try:
        plt.plot(x, y, 'b') # Blue line
        plt.title("Net Assets Over Time", fontsize=20, weight="bold")
        plt.xlabel("Dates", fontsize=16, weight="bold")
        plt.ylabel("Net Assets", fontsize=16, weight="bold")
        plt.xticks(x, rotation=30)
        plt.show()
    except ValueError:
        socket.send(b"Error - Graph did not display.")

    #  Send reply back to client
    socket.send(b"Success")