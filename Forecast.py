
import zmq
import datetime

def TotalOnDate(user_data, date, type):
    total = 0
    for event in user_data[type]:
        date_diff = date - datetime.date.fromisoformat(event["start date"])
        if event["frequency"] is None:
            if date_diff.days == 0:
                if type == "income":
                    total += event["amount"]
                else:
                    total -= event["amount"]
        elif date_diff.days >= 0 and date_diff.days % event["frequency"] == 0 \
                and (event["end date"] is None
                     or date <= datetime.date.fromisoformat(event["end date"])):
            if type == "income":
                total += event["amount"]
            else:
                total -= event["amount"]
    return total


# Calculate assets
def CalculateAssets(user_data, start_date, end_date):

    # Initialize dates and amount
    assets_schedule = []
    assets = user_data["initial assets"]
    date = datetime.date.fromisoformat(user_data["initial assets date"])
    start_date = datetime.date.fromisoformat(start_date)

    range = False
    if end_date is not None:
        range = True
        end_date = datetime.date.fromisoformat(end_date)

    # Calculate assets as of start_date
    while date <= start_date:
        assets += TotalOnDate(user_data, date, "income")
        assets += TotalOnDate(user_data, date, "expense")
        date += datetime.timedelta(days=1)
    assets_on_start_date = assets

    # Calculate schedule of assets between start_date and end_date
    if range:
        assets_schedule.append(assets)
        while date <= end_date:
            assets += TotalOnDate(user_data, date, "income")
            assets += TotalOnDate(user_data, date, "expense")
            assets_schedule.append(assets)
            date += datetime.timedelta(days=1)

    return assets_on_start_date, assets_schedule


# SOCKET SETUP

# Create context
context = zmq.Context()

#  Connect to "UI" microservice socket (5001)
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5001")

while True:
    data = socket.recv_json()

    user_data = data[0]
    start_date = data[1]
    end_date = data[2]

    assets_on_start_date, assets_schedule = CalculateAssets(user_data, start_date, end_date)

    socket.send_json([assets_on_start_date, assets_schedule])