import curses
from curses import initscr, wrapper
import time
from fillers import beta, dirtybot
from menus import print_menu, submenu1, submenu2
from utils import bot_setup

def main(stdscr):

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    RED_BLACK = curses.color_pair(1)
    GREEN_BLACK = curses.color_pair(2)
    YELLOW_BLACK = curses.color_pair(3)
    Menu_1 = ["Wallet Features", "Minting", "Setup", "Quit"]
    # initscr()

    stdscr.clear()
    stdscr.addstr(
        0,
        95,
        dirtybot,
        curses.color_pair(1),
    )

    stdscr.addstr("Press any key to make it happen...", YELLOW_BLACK)
    stdscr.getch()
    stdscr.clear()
    stdscr.refresh()

    current_row_idx = 0
    curses.curs_set(0)

    print_menu(stdscr, current_row_idx)

    while True:
        key = stdscr.getch()
        stdscr.clear()

        # escape key to exit the program and return to the terminal
        if key == 27:
            break

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(Menu_1) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            time.sleep(0.2)
            # stdscr.getch()
            stdscr.refresh()
            # this is where if you select the last menu item it will break out of the loop
            if current_row_idx == len(Menu_1) - 1:
                break
            if current_row_idx == 0:
                submenu1(stdscr)
                # wallet_create(stdscr)
                # break
            if current_row_idx == 1:
                submenu2(stdscr)
            if current_row_idx == 2:
                bot_setup()
                stdscr.clear()
                stdscr.refresh()
                stdscr.addstr(
                    0,
                    0,
                    "Setup Complete - The main.json file either already exists or it has \nbeen created in this directory\n..... \nPress any key to continue",
                    RED_BLACK,
                )
                stdscr.getch()
        print_menu(stdscr, current_row_idx)
        stdscr.refresh()


if __name__ == "__main__":
    wrapper(main)
