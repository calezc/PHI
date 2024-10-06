
from tkinter import messagebox
import zmq

help_titles = {
    "welcome": "Welcome",
    "new": "New Profile",
    "home": "Home Page",
    "income_home": "Income",
    "income_add_home": "Income (Add)",
    "income_add_manual": "Income (Add) (Manual)",
    "income_add_manual_one": "Income (Add) (Manual) (One-Off)",
    "income_add_manual_rec": "Income (Add) (Manual) (Recurring)",
    "income_edit_home": "Income (Edit)",
    "income_edit_manual": "Income (Edit) (Manual)",
    "income_delete": "Income (Delete)",
    "expense_home": "Expense",
    "expense_add_home": "Expense (Add)",
    "expense_add_manual": "Expense (Add) (Manual)",
    "expense_add_manual_one": "Expense (Add) (Manual) (One-Off)",
    "expense_add_manual_rec": "Expense (Add) (Manual) (Recurring)",
    "expense_edit_home": "Expense (Edit)",
    "expense_edit_manual": "Expense (Edit) (Manual)",
    "expense_delete": "Expense (Delete)",
    "forecast": "Financial Forecast",
    "exit_warning": "Exit Warning"
}
help_messages = {
    "welcome":
        "AVAILABLE COMMANDS:\n"
        "- 'New' - Loads interface to create new profile.\n"
        "- 'Load' - Loads interface to load existing profile.\n"
        "- 'More' - Loads interface with additional software information.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Exit' - Exits the program.",
    "new":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Username - Enter the name associated with this profile.\n"
        "- Current Assets - Enter the amount of your current assets (in USD).",
    "home":
        "AVAILABLE COMMANDS:\n"
        "- 'Income' - Loads interface to add/edit income events.\n"
        "- 'Expense' - Loads interface to add/edit expense events.\n"
        "- 'Forecast' - Loads interface to view financial forecast.\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.",
    "income_home":
        "AVAILABLE COMMANDS:\n"
        "- 'Add' - Loads interface to add income events.\n"
        "- 'Edit' - Loads interface to edit income events.\n"
        "- 'Delete' - Loads interface to delete income events.\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.",
    "income_add_home":
        "AVAILABLE COMMANDS:\n"
        "- 'Manual' - Loads interface to add income events manually.\n"
        "- 'CSV' - Loads interface to add income events via CSV (comma delimited).\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.",
    "income_add_manual":
        "AVAILABLE COMMANDS:\n"
        "- 'One-Off' - Loads interface to add one-off income events.\n"
        "- 'Recurring' - Loads interface to add recurring income events.\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.",
    "income_add_manual_one":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Date - Enter the date of the income event. (Format: YYYY-MM-DD)\n"
        "- Amount - Enter the amount of the income event (in USD).",
    "income_add_manual_rec":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Start Date - Enter the start date of the recurring income. (Format: YYYY-MM-DD)\n"
        "- Amount - Enter the amount of the income event (in USD).\n"
        "- Frequency - Enter the frequency of the income event (in days).\n"
        "- End Date - Enter the end date of the recurring income (if any). (Format: YYYY-MM-DD). "
        "If no end date, type '0'.",
    "income_edit_home":
        "AVAILABLE COMMANDS:\n"
        "- 'Manual' - Loads interface to edit income events manually.\n"
        "- 'CSV' - Loads interface to edit income events via CSV.\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.",
    "income_edit_manual":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Income Event - Enter the number of the income event you would like to edit.\n"
        "- Start Date - Enter the start date of the income. (Format: YYYY-MM-DD)\n"
        "- Amount - Enter the amount of the income event (in USD).\n"
        "- Frequency - Enter the frequency of the income event (in days)."
        "If non-recurring, type '0'.\n"
        "- End Date - Enter the end date of the recurring income (if any). (Format: YYYY-MM-DD). "
        "If no end date, type '0'.",
    "income_delete":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Income Event - Enter the number of the income event you would like to delete.",
    "expense_home":
        "AVAILABLE COMMANDS:\n"
        "- 'Add' - Loads interface to add expense events.\n"
        "- 'Edit' - Loads interface to edit expense events.\n"
        "- 'Delete' - Loads interface to delete expense events.\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.",
    "expense_add_home":
        "AVAILABLE COMMANDS:\n"
        "- 'Manual' - Loads interface to add expense events manually.\n"
        "- 'CSV' - Loads interface to add expense events via CSV (comma delimited).\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.",
    "expense_add_manual":
        "AVAILABLE COMMANDS:\n"
        "- 'One-Off' - Loads interface to add one-off expense events.\n"
        "- 'Recurring' - Loads interface to add recurring expense events.\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.",
    "expense_add_manual_one":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Date - Enter the date of the expense event. (Format: YYYY-MM-DD)\n"
        "- Amount - Enter the amount of the expense event (in USD).",
    "expense_add_manual_rec":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Start Date - Enter the start date of the recurring expense. (Format: YYYY-MM-DD)\n"
        "- Amount - Enter the amount of the expense event (in USD).\n"
        "- Frequency - Enter the frequency of the expense event (in days).\n"
        "- End Date - Enter the end date of the recurring expense (if any). (Format: YYYY-MM-DD). "
        "If no end date, type '0'.",
    "expense_edit_home":
        "AVAILABLE COMMANDS:\n"
        "- 'Manual' - Loads interface to edit expense events manually.\n"
        "- 'CSV' - Loads interface to edit expense events via CSV.\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.",
    "expense_edit_manual":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Expense Event - Enter the number of the expense event you would like to edit.\n"
        "- Start Date - Enter the start date of the expense. (Format: YYYY-MM-DD)\n"
        "- Amount - Enter the amount of the expense event (in USD).\n"
        "- Frequency - Enter the frequency of the expense event (in days)."
        "If non-recurring, type '0'.\n"
        "- End Date - Enter the end date of the recurring expense (if any). (Format: YYYY-MM-DD). "
        "If no end date, type '0'.",
    "expense_delete":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Expense Event - Enter the number of the expense event you would like to delete.",
    "forecast":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program.\n\n"
        "INPUT FIELDS:\n"
        "- Start Date - Enter the start date for which you would like to calculate your financial forecast. (Format: YYYY-MM-DD)\n"
        "- End Date - Enter the end date for which you would like to calculate your financial forecast. (Format: YYYY-MM-DD)\n"
        "If only start date, type '0'.",
    "exit_warning":
        "AVAILABLE COMMANDS:\n"
        "- 'Back' - Returns to the prior page.\n"
        "- 'Help' - Triggers this help pop-up.\n"
        "- 'Save' - Loads interface to save current profile.\n"
        "- 'Exit' - Exits the program."
}

def HelpMessageInit(page):
    help_title = f"PHI - Help - {help_titles[page]}"
    help_message = help_messages[page]

    return help_title, help_message

# SOCKET SETUP

# Create context
context = zmq.Context()

#  Connect to "UI" microservice socket (5000)
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5000")

while True:
    page = socket.recv().decode()

    help_title, help_message = HelpMessageInit(page)
    print(f"Generating the following help dialogue: {help_title}")
    messagebox.showinfo(title=help_title, message=help_message)

    socket.send("Complete".encode())