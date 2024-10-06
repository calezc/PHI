import os
import sys
import time
import datetime
import zmq
import json

# CONSTANTS

HEADER_MAIN = " /$$$$$$$  /$$   /$$ /$$$$$$\n| $$__  $$| $$  | $$|_  $$_/\n" \
                  "| $$  \\ $$| $$  | $$  | $$\n| $$$$$$$/| $$$$$$$$  | $$\n" \
                  "| $$____/ | $$__  $$  | $$\n| $$      | $$  | $$  | $$\n" \
                  "| $$      | $$  | $$ /$$$$$$\n|__/      |__/  |__/|______/\n\n\n"

# GLOBAL VARIABLES

user_data = {
    "user_name": "Current",
    "initial assets": 0,
    "initial assets date": "2000-01-01",
    "income": [],
    "expense": []
}

state_history = []

unsaved_state = False

# SOCKETS SETUP

# Create context
context = zmq.Context()

# Connect to "Help" microservice socket (5000)
socket_help = context.socket(zmq.REQ)
socket_help.connect("tcp://localhost:5000")

# Connect to "Forecast" microservice socket (5001)
socket_forecast = context.socket(zmq.REQ)
socket_forecast.connect("tcp://localhost:5001")

# Connect to "Save/Load" microservice socket (5002)
socket_saveload = context.socket(zmq.REQ)
socket_saveload.connect("tcp://localhost:5002")

# Connect to "CSV" microservice socket (5003)
socket_CSV = context.socket(zmq.REQ)
socket_CSV.connect("tcp://localhost:5003")

# Connect to "Negative Balance Warning" microservice socket (5004)
socket_Neg = context.socket(zmq.REQ)
socket_Neg.connect("tcp://localhost:5004")

# Connect to "Forecast Visualizer" microservice socket (5005)
socket_forecast_vis = context.socket(zmq.REQ)
socket_forecast_vis.connect("tcp://localhost:5005")

# GLOBAL FUNCTIONS

def PrintHeaderSlow():
    for char in HEADER_MAIN:
        #print(char,end='')
        #time.sleep(.01)
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.015)

def PrintPageStrings(string_list):
    for string in string_list:
        print(string)
        time.sleep(.1)

def ReturnToPage(page):
    if page == "welcome":
        WelcomePage()
    elif page == "new":
        NewProfile1()
    elif page == "home":
        HomePage()
    elif page == "income_home":
        IncomeLandingPage()
    elif page == "income_add_home":
        IncomeAddHome()
    elif page == "income_add_manual":
        IncomeAddManual()
    elif page == "income_add_manual_one":
        IncomeAddManualOne()
    elif page == "income_add_manual_rec":
        IncomeAddManualRec()
    elif page == "income_edit_home":
        IncomeEditHome()
    elif page == "income_edit_manual":
        IncomeEditManual()
    elif page == "income_delete":
        IncomeDelete()
    elif page == "expense_home":
        ExpenseLandingPage()
    elif page == "expense_add_home":
        ExpenseAddHome()
    elif page == "expense_add_manual":
        ExpenseAddManual()
    elif page == "expense_add_manual_one":
        ExpenseAddManualOne()
    elif page == "expense_add_manual_rec":
        ExpenseAddManualRec()
    elif page == "expense_edit_home":
        ExpenseEditHome()
    elif page == "expense_edit_manual":
        ExpenseEditManual()
    elif page == "expense_delete":
        ExpenseDelete()
    elif page == "forecast":
        Forecast()
    elif page == "exit_warning":
        ExitWarning()

def ExecuteStandardInputOptions(input, input_options, page=None):
    global unsaved_state
    global user_data

    if input in input_options:
        if input == "Back":
            prior_state = state_history.pop()
            user_data = prior_state["data"]
            page = prior_state["page"]
            if page == "welcome":
                WelcomePage()
            elif page == "new":
                NewProfile()
            elif page == "home":
                HomePage()
            elif page == "income_home":
                IncomeLandingPage()
            elif page == "income_add_home":
                IncomeAddHome()
            elif page == "income_add_manual":
                IncomeAddManual()
            elif page == "income_add_manual_one":
                IncomeAddManualOne()
            elif page == "income_add_manual_rec":
                IncomeAddManualRec()
            elif page == "income_edit_home":
                IncomeEditHome()
            elif page == "income_edit_manual":
                IncomeEditManual()
            elif page == "income_delete":
                IncomeDelete()
            elif page == "expense_home":
                ExpenseLandingPage()
            elif page == "expense_add_home":
                ExpenseAddHome()
            elif page == "expense_add_manual":
                ExpenseAddManual()
            elif page == "expense_add_manual_one":
                ExpenseAddManualOne()
            elif page == "expense_add_manual_rec":
                ExpenseAddManualRec()
            elif page == "expense_edit_home":
                ExpenseEditHome()
            elif page == "expense_edit_manual":
                ExpenseEditManual()
            elif page == "expense_delete":
                ExpenseDelete()
            elif page == "forecast":
                Forecast()
        elif input == "Help":
            socket_help.send(page.encode())
            socket_help.recv()
            ReturnToPage(page)
        elif input == "Save":
            socket_saveload.send_json(["save", user_data])
            load_attempt = socket_saveload.recv_json()
            if load_attempt != "":
                user_data = load_attempt
                os.system('cls')
                print(HEADER_MAIN)
                time.sleep(.5)
                print("Profile saved!")
                unsaved_state = False
                time.sleep(1.5)
                HomePage()
            else:
                os.system('cls')
                print(HEADER_MAIN)
                time.sleep(.5)
                print("Failed to save profile...")
                time.sleep(1.5)
                HomePage()


        elif input == "Exit":
            if unsaved_state:
                ExitWarning()
            else:
                os.system('cls')
                print(HEADER_MAIN)
                print("See you next time!!!")
                time.sleep(1.5)
                os.system('cls')
                sys.exit()

def SaveState(page, data):
    state = {
        "page": page,
        "data": user_data
    }
    state_history.append(state)

def PrintNewManualEntryConfirm(type, data, action="recorded"):

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    start_date = data["start date"]
    amount = "{:,.2f}".format(data["amount"])
    if data["frequency"] is not None:
        frequency = data["frequency"]
    else:
        frequency = "N/A"
    if data["end date"] is not None and data["end date"] != "0":
        end_date = data["end date"]
    else:
        end_date = "N/A"

    page_strings = [
        f"Thank you!\n",
        f"We have {action} the following {type}:\n",
        f"START DATE: {start_date}\n",
        f"AMOUNT: ${amount} (USD)\n",
        f"FREQUENCY: {frequency} days\n",
        f"END DATE: {end_date}\n",
        "Press ENTER to continue..."
    ]

    PrintPageStrings(page_strings)

    input("")

def PrintCSVConfirm(type, action="added"):

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"Thank you!\n",
        f"We have successfully {action} your {type}.\n",
        "Press ENTER to continue..."
    ]

    PrintPageStrings(page_strings)

    input("")

def PrintIncomeExpenseList(type):
    global user_data

    type_str = type.upper()

    print(f"CURRENT {type_str}:")

    if type == "income":
        data = user_data["income"]
    else:
        data = user_data["expense"]
    if len(data) > 0:
        for index, event in enumerate(data):
            print(f"({index+1})")
            PrintIncomeExpenseItem(event)
            print("\n")
        return 1
    else:
        return 0

def PrintIncomeExpenseItem(event):
    start_date = event["start date"]
    amount = "{:,.2f}".format(event["amount"])
    frequency = event["frequency"]
    end_date = event["end date"]
    print(f"START DATE: {start_date}")
    print(f"AMOUNT: ${amount}")
    print(f"FREQUENCY: {frequency}")
    print(f"END DATE: {end_date}")

def CheckNegativeAsssets(forecast):
    for day, amount in enumerate(forecast):
        if amount < 0:
            return day, -amount
    return None

def NegativeAssetsWarning():
    today = datetime.date.today()
    end = today + datetime.timedelta(days=365)
    socket_forecast.send_json([user_data, today.isoformat(), end.isoformat()])
    response = socket_forecast.recv_json()
    negative_balance = CheckNegativeAsssets(response[1])
    if negative_balance is not None:
        neg_date = today + datetime.timedelta(days=negative_balance[0])
        neg_date = neg_date.isoformat()
        amount = negative_balance[1]
        socket_Neg.send_json([neg_date, amount])
        socket_Neg.recv_string()

# PAGE FUNCTIONS

def WelcomePage():

    os.system('cls')

    page_strings = [
        "Welcome to Phi!\n\n",
        "Your path to personal financial empowerment awaits!\n\n",
        "Phi is an easy-to-use (but powerful) command-line program designed to provide\n"
        "you with a forecast of your financial condition, based on your current assets\n"
        "and future income and expenses.\n\n",
        "What would you like to do?",
        "- To get started with a new profile, type 'New'",
        "- To load an existing profile, type 'Load'",
        "- To learn more, type 'More'",
        "- For help, type 'Help'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "New",
        "Load",
        "More",
        "Help",
        "Exit"
    ]

    PrintHeaderSlow()

    time.sleep(0.25)

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "welcome")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    global user_data
    SaveState("welcome", dict(user_data))

    global unsaved_state
    if user_input == "New":
        NewProfile()
    elif user_input == "Load":
        socket_saveload.send_json(["load", user_data])
        load_attempt = socket_saveload.recv_json()
        if load_attempt != "":
            user_data = load_attempt
            os.system('cls')
            print(HEADER_MAIN)
            time.sleep(.5)
            user = user_data["user_name"]
            print(f"Welcome back, {user}!")
            unsaved_state = False
            time.sleep(1.5)
            HomePage()
        else:
            os.system('cls')
            print(HEADER_MAIN)
            time.sleep(.5)
            print("Failed to load profile...")
            time.sleep(1.5)
            WelcomePage()
    elif user_input == "More":
        MorePage()

def NewProfile1():

    os.system('cls')

    page_strings1 = [
        "NEW PROFILE\n\n",
        "To create your new profile, please enter your name and current assets below.\n\n",
        "NOTE: All user information is strictly confidential and is only saved on your\n"
        "local machine.  We will use your current assets as a baseline for your financial\n"
        "forecast.\n\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Exit"
    ]

    print(HEADER_MAIN)

    time.sleep(.5)

    PrintPageStrings(page_strings1)

    user_name = str(input("Username: "))

    ExecuteStandardInputOptions(user_name, input_options, "new")

    print("\n")
    user_assets_initial = None
    while type(user_assets_initial) != float:
        try:
            user_assets_initial = input("Current Assets (in USD): $")
            ExecuteStandardInputOptions(user_assets_initial, input_options, "new")
            user_assets_initial = float(user_assets_initial)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive dollar amount in USD ($)\n")
            time.sleep(.5)

    global unsaved_state
    unsaved_state = True

    return user_name, user_assets_initial

def NewProfile2(user_name, user_assets_initial):

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    current_assets = "{:,.2f}".format(user_assets_initial)

    page_strings2 = [
        f"Welcome, {user_name}!\n",
        f"We have recorded your current assets as ${current_assets} (USD).\n",
        "Now, let's get to the fun stuff!  To enhance your financial forecast, let's add some of\n"
        "your income and expenses.  Income and expense entries may be one-off or recurring events.\n"
        "Once you have added your income and expenses, you will then be ready to review your\n"
        "financial forecast!\n\n"
        "Press ENTER to continue..."
    ]

    PrintPageStrings(page_strings2)

    input("")

def NewProfile():

    user_name, user_assets_initial = NewProfile1()

    NewProfile2(user_name, user_assets_initial)

    # Update global user data
    user_data["user_name"] = user_name
    user_data["initial assets"] = user_assets_initial
    user_data["initial assets date"] = datetime.date.today().isoformat()

    # Save state_history
    SaveState("new", dict(user_data))

    HomePage()

def HomePage():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"HOMEPAGE\n",
        "What would you like to do?",
        "- To add/edit income, type 'Income'",
        "- To add/edit expenses, type 'Expense'",
        "- To view your financial forecast, type 'Forecast'\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Income",
        "Expense",
        "Forecast",
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "home")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    SaveState("home", dict(user_data))

    if user_input == "Income":
        IncomeLandingPage()
    elif user_input == "Expense":
        ExpenseLandingPage()
    elif user_input == "Forecast":
        Forecast()

def IncomeLandingPage():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"INCOME\n",
        "What would you like to do?",
        "- To add income, type 'Add'",
        "- To edit income, type 'Edit'",
        "- To delete income, type 'Delete'\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Add",
        "Edit",
        "Delete",
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "income_home")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    SaveState("income_home", dict(user_data))

    if user_input == "Add":
        IncomeAddHome()
    elif user_input == "Edit":
        IncomeEditHome()
    elif user_input == "Delete":
        IncomeDelete()

def IncomeAddHome():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"INCOME (ADD)\n",
        "Would you like to enter your income manually, or upload a CSV file?",
        "- To enter manually, type 'Manual'",
        "- To upload CSV, type 'CSV'\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Manual",
        "CSV",
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "income_add_home")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    SaveState("income_add_home", dict(user_data))

    if user_input == "Manual":
        IncomeAddManual()
    elif user_input == "CSV":
        socket_CSV.send_string("")
        event_list = socket_CSV.recv_json()
        if event_list is not None:
            global unsaved_state
            unsaved_state = True

            PrintCSVConfirm("income", "added")

            # Update global user data
            user_data["income"] += event_list

            # Check Negative Balance
            NegativeAssetsWarning()

            # Save state_history
            SaveState("income_add_home", dict(user_data))

        HomePage()

def IncomeAddManual():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"INCOME (ADD)\n",
        "Would you like to add one-off or recurring income?",
        "- For one-off, type 'One-off'",
        "- For recurring, type 'Recurring'\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "One-off",
        "Recurring",
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "income_add_manual")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    SaveState("income_add_manual", dict(user_data))

    if user_input == "One-off":
        IncomeAddManualOne()
    elif user_input == "Recurring":
        IncomeAddManualRec()

def IncomeAddManualOne():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"INCOME (ADD) (One-Off)\n",
        "To schedule the one-off income event, please respond to the prompts below.\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    income_date_start = None
    valid_date = False
    while not valid_date:
        try:
            income_date_start = str(input("Date (YYYY-MM-DD): "))
            ExecuteStandardInputOptions(income_date_start, input_options, "income_add_manual_one")
            income_date_start = datetime.date.fromisoformat(income_date_start)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    print("\n")
    income_amount = None
    while type(income_amount) != float:
        try:
            income_amount = input("Amount (in USD): $")
            ExecuteStandardInputOptions(income_amount, input_options, "income_add_manual_one")
            income_amount = float(income_amount)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive dollar amount in USD ($).\n")
            time.sleep(.5)

    income = {
        "start date": income_date_start.isoformat(),
        "amount": income_amount,
        "frequency": None,
        "end date": None
    }

    global unsaved_state
    unsaved_state = True

    PrintNewManualEntryConfirm("income", income, "recorded")

    # Update global user data
    user_data["income"].append(income)

    # Check Negative Balance
    NegativeAssetsWarning()

    # Save state_history
    SaveState("income_add_manual_one", dict(user_data))

    HomePage()

def IncomeAddManualRec():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"INCOME (ADD) (Recurring)\n",
        "To schedule the recurring income events, please respond to the prompts below.\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    income_date_start = None
    valid_date = False
    while not valid_date:
        try:
            income_date_start = str(input("Start Date (YYYY-MM-DD): "))
            ExecuteStandardInputOptions(income_date_start, input_options, "income_add_manual_rec")
            income_date_start = datetime.date.fromisoformat(income_date_start)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    print("\n")
    income_amount = None
    while type(income_amount) != float:
        try:
            income_amount = input("Amount (in USD): $")
            ExecuteStandardInputOptions(income_amount, input_options, "income_add_manual_rec")
            income_amount = float(income_amount)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive dollar amount in USD ($).\n")
            time.sleep(.5)

    print("\n")
    income_freq = None
    while type(income_freq) != int or income_freq <= 0:
        try:
            income_freq = input("Frequency (# of Days): ")
            ExecuteStandardInputOptions(income_freq, input_options, "income_add_manual_rec")
            income_freq = int(income_freq)
            if income_freq <= 0:
                time.sleep(.5)
                print("\nInvalid entry.  Please enter a positive integer.\n")
                time.sleep(.5)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive integer.\n")
            time.sleep(.5)

    print("\n")
    income_date_end = None
    valid_date = False
    while not valid_date:
        try:
            income_date_end = str(input("End Date (YYYY-MM-DD) OR (No End --> Type '0'): "))
            ExecuteStandardInputOptions(income_date_end, input_options, "income_add_manual_rec")
            if income_date_end != "0":
                income_date_end = datetime.date.fromisoformat(income_date_end)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)

    if income_date_end != "0":
        income_date_end = income_date_end.isoformat()
    else:
        income_date_end = None

    income = {
        "start date": income_date_start.isoformat(),
        "amount": income_amount,
        "frequency": income_freq,
        "end date": income_date_end
    }

    global unsaved_state
    unsaved_state = True

    PrintNewManualEntryConfirm("income", income, "recorded")

    # Update global user data
    user_data["income"].append(income)

    # Check Negative Balance
    NegativeAssetsWarning()

    # Save state_history
    SaveState("income_add_manual_rec", dict(user_data))

    HomePage()

def IncomeEditHome():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"INCOME\n",
        "Would you like to edit your income manually, or upload a CSV file?",
        "- To edit manually, type 'Manual'",
        "- To upload CSV, type 'CSV'\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Manual",
        "CSV",
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "income_edit_home")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    SaveState("income_edit_home", dict(user_data))

    if user_input == "Manual":
        IncomeEditManual()
    elif user_input == "CSV":
        socket_CSV.send_string("")
        event_list = socket_CSV.recv_json()
        if event_list is not None:
            global unsaved_state
            unsaved_state = True

            PrintCSVConfirm("income", "edited")

            # Update global user data
            user_data["income"] = event_list

            # Check Negative Balance
            NegativeAssetsWarning()

            # Save state_history
            SaveState("income_edit_home", dict(user_data))

        HomePage()

def IncomeEditManual():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings1 = [
        f"INCOME (EDIT)\n",
        "See the list below of income events.\n\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    page_strings2 = [
        f"INCOME (EDIT)\n",
        "Follow the prompts below to edit the income event.\n\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings1)

    result = PrintIncomeExpenseList("income")

    if result == 0:
        print("\nNo income events found...")
        time.sleep(2.5)
        HomePage()

    user_selection = ""
    while type(user_selection) != int:
        try:
            print("Enter the number of the event you would like to edit:")
            user_selection = input("> ")
            ExecuteStandardInputOptions(user_selection, input_options, "income_edit_manual")
            user_selection = int(user_selection)
            if user_selection < 0 or user_selection > len(user_data["income"]):
                time.sleep(.5)
                print("\nInvalid entry.  Please enter just the number of income event you would like to edit.\n")
                time.sleep(1.5)
                os.system('cls')
                print(HEADER_MAIN)
                PrintPageStrings(page_strings1)
                PrintIncomeExpenseList("income")
                user_selection = ""
                continue
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter just the number of income event you would like to edit.\n")
            time.sleep(.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings1)
            PrintIncomeExpenseList("income")

    income_event = user_data["income"][user_selection - 1]

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    PrintPageStrings(page_strings2)

    print("CURRENT INCOME DETAILS:")

    PrintIncomeExpenseItem(income_event)

    print("\nUPDATED INCOME DETAILS:")

    income_date_start = None
    valid_date = False
    while not valid_date:
        try:
            income_date_start = str(input("Start Date (YYYY-MM-DD): "))
            ExecuteStandardInputOptions(income_date_start, input_options, "income_edit_manual")
            income_date_start = datetime.date.fromisoformat(income_date_start)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings2)
            print("CURRENT INCOME DETAILS:")
            PrintIncomeExpenseItem(income_event)

    print("\n")
    income_amount = None
    while type(income_amount) != float:
        try:
            income_amount = input("Amount (in USD): $")
            ExecuteStandardInputOptions(income_amount, input_options, "income_edit_manual")
            income_amount = float(income_amount)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive dollar amount in USD ($).\n")
            time.sleep(.5)

    print("\n")
    income_freq = None
    while type(income_freq) != int or income_freq < 0:
        try:
            income_freq = input("Frequency (# of Days) OR (Non-Recurring --> Type '0'): ")
            ExecuteStandardInputOptions(income_freq, input_options, "income_edit_manual")
            income_freq = int(income_freq)
            if income_freq < 0:
                time.sleep(.5)
                print("\nInvalid entry.  Please enter a positive integer or 0.\n")
                time.sleep(.5)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive integer or 0.\n")
            time.sleep(.5)

    print("\n")
    income_date_end = None
    valid_date = False
    while not valid_date:
        try:
            income_date_end = str(input("End Date (YYYY-MM-DD) OR (No End --> Type '0'): "))
            ExecuteStandardInputOptions(income_date_end, input_options, "income_edit_manual")
            if income_date_end != "0":
                income_date_end = datetime.date.fromisoformat(income_date_end)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)

    if income_freq == 0:
        income_freq = None

    if income_date_end != "0":
        income_date_end = income_date_end.isoformat()
    else:
        income_date_end = None

    income = {
        "start date": income_date_start.isoformat(),
        "amount": income_amount,
        "frequency": income_freq,
        "end date": income_date_end
    }

    global unsaved_state
    unsaved_state = True

    PrintNewManualEntryConfirm("income", income, "recorded")

    # Update global user data
    user_data["income"][user_selection - 1] = income

    # Check Negative Balance
    NegativeAssetsWarning()

    # Save state_history
    SaveState("income_edit_manual", dict(user_data))

    HomePage()

def IncomeDelete():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings1 = [
        f"INCOME (DELETE)\n",
        "See the list below of income events.\n\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings1)

    result = PrintIncomeExpenseList("income")

    if result == 0:
        print("\nNo income events found...")
        time.sleep(2.5)
        HomePage()

    user_selection = ""
    while type(user_selection) != int:
        try:
            print("Enter the number of the event you would like to delete:")
            user_selection = input("> ")
            ExecuteStandardInputOptions(user_selection, input_options, "income_delete")
            user_selection = int(user_selection)
            if user_selection < 0 or user_selection > len(user_data["income"]):
                time.sleep(.5)
                print("\nInvalid entry.  Please enter just the number of income event you would like to delete.\n")
                time.sleep(1.5)
                os.system('cls')
                print(HEADER_MAIN)
                PrintPageStrings(page_strings1)
                PrintIncomeExpenseList("income")
                user_selection = ""
                continue
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter just the number of income event you would like to delete.\n")
            time.sleep(.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings1)
            PrintIncomeExpenseList("income")

    income_event = user_data["income"][user_selection - 1]

    global unsaved_state
    unsaved_state = True

    PrintNewManualEntryConfirm("income", income_event, "deleted")

    # Update global user data
    user_data["income"].pop(user_selection - 1)

    # Check Negative Balance
    NegativeAssetsWarning()

    # Save state_history
    SaveState("income_delete", dict(user_data))

    HomePage()

def ExpenseLandingPage():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"EXPENSE\n",
        "What would you like to do?",
        "- To add expense, type 'Add'",
        "- To edit expense, type 'Edit'",
        "- To delete expense, type 'Delete'\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Add",
        "Edit",
        "Delete",
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "expense_home")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    SaveState("expense_home", dict(user_data))

    if user_input == "Add":
        ExpenseAddHome()
    elif user_input == "Edit":
        ExpenseEditHome()
    elif user_input == "Delete":
        ExpenseDelete()

def ExpenseAddHome():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"EXPENSE (ADD)\n",
        "Would you like to enter your expense manually, or upload a CSV file?",
        "- To enter manually, type 'Manual'",
        "- To upload CSV, type 'CSV'\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Manual",
        "CSV",
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "expense_add_home")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    SaveState("expense_add_home", dict(user_data))

    if user_input == "Manual":
        ExpenseAddManual()
    elif user_input == "CSV":
        socket_CSV.send_string("")
        event_list = socket_CSV.recv_json()
        if event_list is not None:
            global unsaved_state
            unsaved_state = True

            PrintCSVConfirm("expense", "added")

            # Update global user data
            user_data["expense"] += event_list

            # Check Negative Balance
            NegativeAssetsWarning()

            # Save state_history
            SaveState("expense_add_home", dict(user_data))

        HomePage()

def ExpenseAddManual():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"EXPENSE (ADD)\n",
        "Would you like to add a one-off or recurring expense?",
        "- For one-off, type 'One-off'",
        "- For recurring, type 'Recurring'\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "One-off",
        "Recurring",
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "expense_add_manual")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    SaveState("expense_add_manual", dict(user_data))

    if user_input == "One-off":
        ExpenseAddManualOne()
    elif user_input == "Recurring":
        ExpenseAddManualRec()

def ExpenseAddManualOne():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"EXPENSE (ADD) (One-Off)\n",
        "To schedule the one-off expense event, please respond to the prompts below.\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    expense_date_start = None
    valid_date = False
    while not valid_date:
        try:
            expense_date_start = str(input("Date (YYYY-MM-DD): "))
            ExecuteStandardInputOptions(expense_date_start, input_options, "expense_add_manual_one")
            expense_date_start = datetime.date.fromisoformat(expense_date_start)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    print("\n")
    expense_amount = None
    while type(expense_amount) != float:
        try:
            expense_amount = input("Amount (in USD): $")
            ExecuteStandardInputOptions(expense_amount, input_options, "expense_add_manual_one")
            expense_amount = float(expense_amount)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive dollar amount in USD ($).\n")
            time.sleep(.5)

    expense = {
        "start date": expense_date_start.isoformat(),
        "amount": expense_amount,
        "frequency": None,
        "end date": None
    }

    global unsaved_state
    unsaved_state = True

    PrintNewManualEntryConfirm("expense", expense, "recorded")

    # Update global user data
    user_data["expense"].append(expense)

    # Check Negative Balance
    NegativeAssetsWarning()

    # Save state_history
    SaveState("expense_add_manual_one", dict(user_data))

    HomePage()

def ExpenseAddManualRec():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"EXPENSE (ADD) (Recurring)\n",
        "To schedule the recurring expense events, please respond to the prompts below.\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    expense_date_start = None
    valid_date = False
    while not valid_date:
        try:
            expense_date_start = str(input("Start Date (YYYY-MM-DD): "))
            ExecuteStandardInputOptions(expense_date_start, input_options, "expense_add_manual_rec")
            expense_date_start = datetime.date.fromisoformat(expense_date_start)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    print("\n")
    expense_amount = None
    while type(expense_amount) != float:
        try:
            expense_amount = input("Amount (in USD): $")
            ExecuteStandardInputOptions(expense_amount, input_options, "expense_add_manual_rec")
            expense_amount = float(expense_amount)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive dollar amount in USD ($).\n")
            time.sleep(.5)

    print("\n")
    expense_freq = None
    while type(expense_freq) != int or expense_freq <= 0:
        try:
            expense_freq = input("Frequency (# of Days): ")
            ExecuteStandardInputOptions(expense_freq, input_options, "expense_add_manual_rec")
            expense_freq = int(expense_freq)
            if expense_freq <= 0:
                time.sleep(.5)
                print("\nInvalid entry.  Please enter a positive integer.\n")
                time.sleep(.5)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive integer.\n")
            time.sleep(.5)

    print("\n")
    expense_date_end = None
    valid_date = False
    while not valid_date:
        try:
            expense_date_end = str(input("End Date (YYYY-MM-DD) OR (No End --> Type '0'): "))
            ExecuteStandardInputOptions(expense_date_end, input_options, "expense_add_manual_rec")
            if expense_date_end != "0":
                expense_date_end = datetime.date.fromisoformat(expense_date_end)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)

    if expense_date_end != "0":
        expense_date_end = expense_date_end.isoformat()
    else:
        expense_date_end = None

    expense = {
        "start date": expense_date_start.isoformat(),
        "amount": expense_amount,
        "frequency": expense_freq,
        "end date": expense_date_end
    }

    global unsaved_state
    unsaved_state = True

    PrintNewManualEntryConfirm("expense", expense, "recorded")

    # Update global user data
    user_data["expense"].append(expense)

    # Check Negative Balance
    NegativeAssetsWarning()

    # Save state_history
    SaveState("expense_add_manual_rec", dict(user_data))

    HomePage()

def ExpenseEditHome():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        f"EXPENSE (EDIT)\n",
        "Would you like to edit your expense manually, or upload a CSV file?",
        "- To edit manually, type 'Manual'",
        "- To upload CSV, type 'CSV'\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Manual",
        "CSV",
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        ExecuteStandardInputOptions(user_input, input_options, "expense_edit_home")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

    # Save state_history
    SaveState("expense_edit_home", dict(user_data))

    if user_input == "Manual":
        ExpenseEditManual()
    elif user_input == "CSV":
        socket_CSV.send_string("")
        event_list = socket_CSV.recv_json()
        if event_list is not None:
            global unsaved_state
            unsaved_state = True

            PrintCSVConfirm("expense", "edited")

            # Update global user data
            user_data["expense"] = event_list

            # Check Negative Balance
            NegativeAssetsWarning()

            # Save state_history
            SaveState("expense_edit_home", dict(user_data))

        HomePage()

def ExpenseEditManual():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings1 = [
        f"EXPENSE (EDIT)\n",
        "See the list below of expense events.\n\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    page_strings2 = [
        f"EXPENSE (EDIT)\n",
        "Follow the prompts below to edit the expense event.\n\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings1)

    result = PrintIncomeExpenseList("expense")

    if result == 0:
        print("\nNo expense events found...")
        time.sleep(2.5)
        HomePage()

    user_selection = ""
    while type(user_selection) != int:
        try:
            print("Enter the number of the event you would like to edit:")
            user_selection = input("> ")
            ExecuteStandardInputOptions(user_selection, input_options, "expense_edit_manual")
            user_selection = int(user_selection)
            if user_selection < 0 or user_selection > len(user_data["expense"]):
                time.sleep(.5)
                print("\nInvalid entry.  Please enter just the number of expense event you would like to edit.\n")
                time.sleep(1.5)
                os.system('cls')
                print(HEADER_MAIN)
                PrintPageStrings(page_strings1)
                PrintIncomeExpenseList("expense")
                user_selection = ""
                continue
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter just the number of expense event you would like to edit.\n")
            time.sleep(.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings1)
            PrintIncomeExpenseList("expense")

    expense_event = user_data["expense"][user_selection - 1]

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    PrintPageStrings(page_strings2)

    print("CURRENT EXPENSE DETAILS:")

    PrintIncomeExpenseItem(expense_event)

    print("\nUPDATED EXPENSE DETAILS:")

    expense_date_start = None
    valid_date = False
    while not valid_date:
        try:
            expense_date_start = str(input("Start Date (YYYY-MM-DD): "))
            ExecuteStandardInputOptions(expense_date_start, input_options, "expense_edit_manual")
            expense_date_start = datetime.date.fromisoformat(expense_date_start)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings2)
            print("CURRENT EXPENSE DETAILS:")
            PrintIncomeExpenseItem(expense_event)

    print("\n")
    expense_amount = None
    while type(expense_amount) != float:
        try:
            expense_amount = input("Amount (in USD): $")
            ExecuteStandardInputOptions(expense_amount, input_options, "expense_edit_manual")
            expense_amount = float(expense_amount)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive dollar amount in USD ($).\n")
            time.sleep(.5)

    print("\n")
    expense_freq = None
    while type(expense_freq) != int or expense_freq < 0:
        try:
            expense_freq = input("Frequency (# of Days) OR (Non-Recurring --> Type '0'): ")
            ExecuteStandardInputOptions(expense_freq, input_options, "expense_edit_manual")
            expense_freq = int(expense_freq)
            if expense_freq < 0:
                time.sleep(.5)
                print("\nInvalid entry.  Please enter a positive integer or 0.\n")
                time.sleep(.5)
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter a positive integer or 0.\n")
            time.sleep(.5)

    print("\n")
    expense_date_end = None
    valid_date = False
    while not valid_date:
        try:
            expense_date_end = str(input("End Date (YYYY-MM-DD) OR (No End --> Type '0'): "))
            ExecuteStandardInputOptions(expense_date_end, input_options, "expense_edit_manual")
            if expense_date_end != "0":
                expense_date_end = datetime.date.fromisoformat(expense_date_end)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)

    if expense_freq == 0:
        expense_freq = None

    if expense_date_end != "0":
        expense_date_end = expense_date_end.isoformat()
    else:
        expense_date_end = None

    expense = {
        "start date": expense_date_start.isoformat(),
        "amount": expense_amount,
        "frequency": expense_freq,
        "end date": expense_date_end
    }

    global unsaved_state
    unsaved_state = True

    PrintNewManualEntryConfirm("expense", expense, "recorded")

    # Update global user data
    user_data["expense"][user_selection - 1] = expense

    # Check Negative Balance
    NegativeAssetsWarning()

    # Save state_history
    SaveState("expense_edit_manual", dict(user_data))

    HomePage()

def ExpenseDelete():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings1 = [
        f"EXPENSE (DELETE)\n",
        "See the list below of expense events.\n\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings1)

    result = PrintIncomeExpenseList("expense")

    if result == 0:
        print("\nNo expense events found...")
        time.sleep(2.5)
        HomePage()

    user_selection = ""
    while type(user_selection) != int:
        try:
            print("Enter the number of the event you would like to delete:")
            user_selection = input("> ")
            ExecuteStandardInputOptions(user_selection, input_options, "expense_delete")
            user_selection = int(user_selection)
            if user_selection < 0 or user_selection > len(user_data["expense"]):
                time.sleep(.5)
                print("\nInvalid entry.  Please enter just the number of expense event you would like to delete.\n")
                time.sleep(1.5)
                os.system('cls')
                print(HEADER_MAIN)
                PrintPageStrings(page_strings1)
                PrintIncomeExpenseList("expense")
                user_selection = ""
                continue
        except ValueError:
            time.sleep(.5)
            print("\nInvalid entry.  Please enter just the number of expense event you would like to delete.\n")
            time.sleep(.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings1)
            PrintIncomeExpenseList("expense")

    expense_event = user_data["expense"][user_selection - 1]

    global unsaved_state
    unsaved_state = True

    PrintNewManualEntryConfirm("expense", expense_event, "deleted")

    # Update global user data
    user_data["expense"].pop(user_selection - 1)

    # Check Negative Balance
    NegativeAssetsWarning()

    # Save state_history
    SaveState("expense_delete", dict(user_data))

    HomePage()

def Forecast():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        "FINANCIAL FORECAST\n",
        "Please provide the date or range of dates below for which you would like to see your projected assets.\n",
        "Options:",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    forecast_date_start = None
    valid_date = False
    while not valid_date:
        try:
            forecast_date_start = str(input("Start Date (YYYY-MM-DD): "))
            ExecuteStandardInputOptions(forecast_date_start, input_options, "forecast")
            forecast_date_start = datetime.date.fromisoformat(forecast_date_start)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)
    forecast_date_start = forecast_date_start.isoformat()

    print("\n")
    forecast_date_end = None
    valid_date = False
    while not valid_date:
        try:
            forecast_date_end = str(input("End Date (YYYY-MM-DD) OR (Only Start Date --> Type '0'): "))
            ExecuteStandardInputOptions(forecast_date_end, input_options, "forecast")
            if forecast_date_end != "0":
                forecast_date_end = datetime.date.fromisoformat(forecast_date_end)
            valid_date = True
        except ValueError:
            time.sleep(.5)
            print("\nIncorrect date format.  Please enter YYYY-MM-DD.\n")
            time.sleep(1.5)

    if forecast_date_end != "0":
        forecast_date_end = forecast_date_end.isoformat()
    else:
        forecast_date_end = None

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    socket_forecast.send_json([user_data, forecast_date_start, forecast_date_end])
    response = socket_forecast.recv_json()
    if forecast_date_end is None:
        assets_forecast_specific = "{:,.2f}".format(response[0])

        page_strings2 = [
            "FINANCIAL FORECAST (Specific Date)\n",
            f"On {forecast_date_start}, your assets are projected to be ${assets_forecast_specific} (USD).\n\n",
            "Press ENTER to continue..."
        ]
    else:
        start_date_assets = response[1][0]
        start_date_assets_formatted = "{:,.2f}".format(start_date_assets)
        end_date_assets = response[1][-1]
        end_date_assets_formatted = "{:,.2f}".format(end_date_assets)
        difference = end_date_assets - start_date_assets
        difference_formatted = "{:,.2f}".format(difference)

        if difference == 0:
            change_str = "a difference"
            change_punc = "."
        elif difference > 0:
            change_str = "an increase"
            change_punc = "!"
        else:
            change_str = "a decrease"
            change_punc = "."

        page_strings2 = [
            "FINANCIAL FORECAST (Date Range)\n",
            f"On {forecast_date_start}, your assets are projected to be ${start_date_assets_formatted} (USD).\n"
            f"On {forecast_date_end}, your assets are projected to be ${end_date_assets_formatted} (USD).\n",
            f"That's {change_str} of ${difference_formatted}{change_punc}\n",
            "See the pop-up window for a graph of your Financial Forecast!\n",
            "Press ENTER to continue..."
        ]

    PrintPageStrings(page_strings2)

    if forecast_date_end is not None:
        # Send request to Forecast Visualizer
        forecast_request = {
            "start": forecast_date_start,
            "end": forecast_date_end,
            "assets": response[1]
        }
        forecast_request = json.dumps(forecast_request)
        socket_forecast_vis.send(forecast_request.encode("utf-8"))
        socket_forecast_vis.recv()

    input("")

    # Save state_history
    SaveState("forecast", dict(user_data))

    HomePage()

def MorePage():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings2 = [
        "AUTHOR: Cale Coffman\n",
        "VERSION: 0.1\n",
        "DESCRIPTION: Phi is an easy-to-use (but powerful) command-line program designed to\n"
        "provide you with a forecast of your financial condition, based on your current assets\n"
        "and future income and expenses.  Once you have uploaded your current assets and at\n"
        "least one income or expense event, Phi prepares a schedule of your income and\n"
        "expense events and calculates adjustments to your assets based on those events.\n"
        "Using that data, you are able to access a forecast of your assets, by either\n"
        "viewing your calculated assets as of a specific date or over a specific future\n"
        "timeframe.  Income and expense events may be input manually on a one-off or recurring\n"
        "basis, or by leveraging Phi's CSV file support, you may upload a pre-assembled\n"
        "schedule of income or expense events all at once--a very powerful tool for unlocking\n"
        "the mysteries of your financial future!",
        "\n\n"
        "Press ENTER to return..."
    ]

    PrintPageStrings(page_strings2)

    input("")

    WelcomePage()

def ExitWarning():

    os.system('cls')

    print(HEADER_MAIN)

    time.sleep(.5)

    page_strings = [
        "WARNING: YOU ARE ABOUT TO EXIT THE PROGRAM WITHOUT SAVING YOUR DATA.\n"
        "IF YOU PROCEED, ALL DATA ENTERED DURING THIS SESSION WILL BE LOST!\n",
        "WOULD YOU LIKE TO PROCEED?",
        "- To return to the previous page, type 'Back'",
        "- For help, type 'Help'",
        "- To save, type 'Save'",
        "- To exit, type 'Exit'\n\n"
    ]

    input_options = [
        "Back",
        "Help",
        "Save",
        "Exit"
    ]

    PrintPageStrings(page_strings)

    user_input = ""
    while user_input not in input_options:
        user_input = str(input("> "))
        if user_input == "Exit":
            global unsaved_state
            unsaved_state = False
        ExecuteStandardInputOptions(user_input, input_options, "exit_warning")
        if user_input not in input_options:
            print("\nInvalid entry. Please try again.\n")
            time.sleep(1.5)
            os.system('cls')
            print(HEADER_MAIN)
            PrintPageStrings(page_strings)

# INITIATE UI

WelcomePage()