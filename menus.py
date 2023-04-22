import os
import curses
import utils
from fillers import *
from utils import *



def submenu1(stdscr):
    h, w = stdscr.getmaxyx()
    GREEN_BLACK = curses.color_pair(2)
    RED_BLACK = curses.color_pair(1)

    # calculate top position of ASCII art
    art_height = len(wallet_art)
    art_width = len(wallet_art[0])
    center_x = w // 2
    top_y = 0

    options = [
        "Setup Main Wallet",
        "Create Wallets",
        "Disperse",
        "Collect",
        "Check Balance",
        "Main Menu",
    ]
    current_row_idx = 0

    while True:
        stdscr.clear()
        # Print ASCII art
        for i, line in enumerate(wallet_art):
            stdscr.addstr(top_y + i, center_x - (art_width // 2), line, RED_BLACK)

        for idx, option in enumerate(options):
            x = w // 2 - len(option) // 2
            y = h // 2 - len(options) // 2 + idx
            # x = 2
            # y = idx + 2
            if idx == current_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option)

        stdscr.refresh()

        key = stdscr.getch()
        if key == 27:
            break
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(options) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if options[current_row_idx] == "Setup Main Wallet":
                bot_setup()
                stdscr.clear()
                stdscr.refresh()
                stdscr.addstr(
                    0,
                    0,
                    "Setup Function Complete - The main.json file either already exists or it has \nbeen created in the app folder find it 'main.json' \n..... Press any key to continue",
                    RED_BLACK,
                )
                stdscr.getch()
            elif options[current_row_idx] == "Create Wallets":
                wallet_create(stdscr)
            elif options[current_row_idx] == "Collect":
                collect_eth(stdscr)
                # stdscr.clear()
                # stdscr.refresh()
                # stdscr.addstr(
                #     0,
                #     0,
                #     "Collect Function - This function is not yet implemented",
                #     RED_BLACK,
                # )
                # stdscr.getch()
            elif options[current_row_idx] == "Check Balance":
                check_balance(stdscr)
            elif options[current_row_idx] == "Disperse":
                disperse(stdscr)

            elif options[current_row_idx] == "Main Menu":
                break


def submenu2(stdscr):
    options = ["Bulk Mint", "Walk Mint", "Import tx", "Cancel tx", "Main Menu"]
    current_row_idx = 0
    h, w = stdscr.getmaxyx()
    GREEN_BLACK = curses.color_pair(2)
    RED_BLACK = curses.color_pair(1)

    # ASCII art

    # calculate top position of ASCII art
    art_height = len(minting_art)
    art_width = len(minting_art[0])
    center_x = w // 2
    top_y = 0

    while True:
        stdscr.clear()

        # Print ASCII art
        for i, line in enumerate(minting_art):
            stdscr.addstr(top_y + i, center_x - (art_width // 2), line, RED_BLACK)

        for idx, option in enumerate(options):
            x = w // 2 - len(option) // 2
            y = h // 2 - len(options) // 2 + idx
            if idx == current_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option)
        stdscr.refresh()
        key = stdscr.getch()
        if key == 27:
            break
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(options) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # return options[current_row_idx]
            if options[current_row_idx] == "Bulk Mint":
                bulk_mint(stdscr)
            elif options[current_row_idx] == "Walk Mint":
                walk_mint(stdscr)
            elif options[current_row_idx] == "Import tx":
                imp_tx(stdscr)
            elif options[current_row_idx] == "Cancel tx":
                cancel_pending_transactions(stdscr)
                stdscr.refresh()
                stdscr.getch()
            elif options[current_row_idx] == "Main Menu":
                break


def print_menu(stdscr, selected_row_idx):
    Menu_1 = ["Wallet Features", "Minting", "Setup", "Quit"]
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    RED_BLACK = curses.color_pair(1)
    stdscr.clear()
    stdscr.refresh()
    current_row_idx = 0
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    art_height = len(beta)
    art_width = len(beta[0])
    center_x = w // 2
    top_y = 0
    for i, line in enumerate(beta):
        stdscr.addstr(top_y + i, center_x - (art_width // 2), line, RED_BLACK)
    for idx, row in enumerate(
        Menu_1,
    ):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(Menu_1) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()
