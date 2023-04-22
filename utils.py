import json
import os
import curses
import time
import requests
from dotenv import load_dotenv

load_dotenv()


api_base_url = os.getenv("API_BASE_URL")


class Prompt:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.red_black = curses.color_pair(1)
        self.green_black = curses.color_pair(2)

    def get_str(self, prompt, x=0, y=0, color_pair=None):
        self.stdscr.clear()
        if color_pair is None:
            color_pair = self.red_black
        self.stdscr.addstr(y, x, prompt, color_pair)
        self.stdscr.refresh()
        curses.echo()
        user_input = self.stdscr.getstr(y + 1, x).decode("utf-8")
        self.stdscr.addstr(y + 1, x, user_input, color_pair)
        curses.noecho()
        self.stdscr.refresh()
        return user_input


def bot_setup(stdscr):
    filename = "main.json"

    try:
        # check if the file already exists
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
        else:
            # populate the file with default information
            data = {
                "main_address": "YourMainAddress",
                "main_private_key": "YourMainPrivateKey",
                "etherscan_api_key": "YourApiKeyToken",
                "node_api_key": "YourApiKeyToken",
                "blocknative_api_key": "YourApiKeyToken",
                "dirty_api_key": "YourApiKeyToken",
                "network": "mainnet",
            }
            with open(filename, "w") as f:
                json.dump(data, f)
    except IOError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, "Error is {e}.", curses.color_pair(1))
        stdscr.refresh()
        stdscr.getch()


# Could replace whole json file system with implementation of secured database system down the line but for now this will do
try:
    if os.path.exists("main.json"):
        with open("main.json", "r") as f:
            data = json.load(f)
    else:
        bot_setup(None)
except IOError as e:
    print(e)

# Access fields in main.json
try:
    main_address = data["main_address"]
    main_private_key = data["main_private_key"]
    etherscan_api_key = data["etherscan_api_key"]
    node_api_key = data["node_api_key"]
    blocknative_api_key = data["blocknative_api_key"]
    dirty_api_key = data["dirty_api_key"]
    network = data["network"]
    disperse_contract_address = "0xD152f549545093347A162Dce210e7293f1452150"
except IOError as e:
    print(e)


def file_selection(stdscr, string, ending=None, downloads=None):
    # Initialize curses
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    RED_BLACK = curses.color_pair(1)
    GREEN_BLACK = curses.color_pair(2)

    # Get the list of files in the current directory
    current_dir = os.getcwd()
    files = [f for f in os.listdir(current_dir) if f.endswith(f"{ending}.json")]

    # Optionally include the downloads folder
    if downloads != None:
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        downloads_files = [
            f for f in os.listdir(downloads_folder) if f.endswith(f"{ending}.json")
        ]
        files.extend(downloads_files)

    # Display the file selection menu
    # Initialize the current selection to the first file in the list
    current_selection = 0
    try:
        # Loop until the user selects a file or cancels
        while True:
            # Clear the screen and print the file list
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            stdscr.addstr(0, (w - len(string)) // 2, string, curses.A_BOLD)
            for i, file in enumerate(files):
                if i == current_selection:
                    stdscr.addstr(
                        h // 2 - len(files) // 2 + i + 1,
                        (w - len(file)) // 2,
                        file,
                        RED_BLACK,
                    )
                else:
                    stdscr.addstr(
                        h // 2 - len(files) // 2 + i + 1, (w - len(file)) // 2, file
                    )

            # Refresh the screen
            stdscr.refresh()

            # Get user input
            key = stdscr.getch()
            if key == 27:
                break

            # Move the selection up or down
            if key == curses.KEY_UP:
                if current_selection > 0:
                    current_selection -= 1
            elif key == curses.KEY_DOWN:
                if current_selection < len(files) - 1:
                    current_selection += 1

            # Select the current file
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_file = files[current_selection]
                return os.path.join(current_dir, selected_file)

            # Cancel the selection
            elif key == 27:
                return None
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(
            0, 0, "Error is {e}. Press any key to continue...", curses.color_pair(1)
        )
        stdscr.refresh()
        stdscr.getch()


def cancel_pending_transactions(stdscr):
    pass
    tx_hashes = []
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    RED_BLACK = curses.color_pair(1)
    GREEN_BLACK = curses.color_pair(2)

    wallets = file_selection(
        stdscr, "Select the wallet file to cancel transactions from:", "_wallets"
    )
    try:
        with open(wallets) as f:
            wallet_data = json.load(f)
            pass
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(
            0,
            0,
            f"Error: {e}. Please make sure you have a wallet file in the current directory\n Press any key to continue...",
            RED_BLACK,
        )
        stdscr.refresh()
        stdscr.getch()
        return


# Done but not tested
def wallet_create(stdscr):
    prompt = Prompt(stdscr)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    RED_BLACK = curses.color_pair(1)
    GREEN_BLACK = curses.color_pair(2)

    # Initialize curses
    curses.curs_set(1)

    num_wallets = prompt.get_str("Enter number of wallets to create:")
    file_name = prompt.get_str(
        "Enter file name and '_wallets' will be appended: ex. 20"
    )

    # Check if file exists
    if os.path.isfile(f"{file_name}_wallets.json"):
        # Load existing data from file
        with open(f"{file_name}.json", "r") as f:
            data = json.load(f)
    else:
        # Create new data dictionary
        data = {"wallets": []}

    # Prep the data to be sent to the api
    payload = {
        "num_wallets": num_wallets,
        "node_api_key": node_api_key,
        "network": "mainnet",
    }

    # Prep the headers for the api call
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {dirty_api_key}",
    }

    # Make the POST request to the API
    response = requests.post(
        f"{api_base_url}/api/wallet/create", json=payload, headers=headers
    )

    # Check if the response is successful
    if response.status_code == 200:
        wallets_data = response.json()

        # Add the new wallets to the data dictionary
        try:
            for wallet in wallets_data["wallets"]:
                data["wallets"].append(
                    {"private_key": wallet["private_key"], "address": wallet["address"]}
                )

            # Save the data to the file
            with open(f"{file_name}_wallets.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            stdscr.addstr(
                5,
                0,
                f"Error: {e} \n \n Press any key to continue",
                RED_BLACK,
            )
            stdscr.getch()
            return

        stdscr.addstr(
            5,
            0,
            f"{num_wallets} wallets generated\n \n Press any key to continue",
            GREEN_BLACK,
        )
        stdscr.getch()
    else:
        stdscr.addstr(
            5,
            0,
            f"Error: {response.status_code} \n \n Press any key to continue",
            RED_BLACK,
        )
        stdscr.getch()


def imp_tx(stdscr):
    pass


def disperse(stdscr):
    pass


def collect_eth(stdscr):
    pass


def check_balance(stdscr):
    pass


def bulk_mint(stdscr):
    pass


def walk_mint(stdscr):
    pass


# You are great and i love you long time. Thank you for all you do.
