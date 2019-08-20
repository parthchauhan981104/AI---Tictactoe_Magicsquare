# ................................................IMPORTS..............................................................
import tkinter as tk
from time import sleep
import random
import copy
from functools import partial
# .....................................................................................................................

# .............................................Tic Tac Toe Class.......................................................
class TicTacToe(object):
    winners = ({1, 2, 3}, {4, 5, 6}, {7, 8, 9},
               {1, 4, 7}, {2, 5, 8}, {3, 6, 9},
               {1, 5, 9}, {3, 5, 7})

    def __init__(self, top):

        self.top = top
        self.top.geometry("490x550+400+50")  # dimensions and offset on screen
        # self.X_O_dict = {"X": [], "O": []}  ## list of "X" and "O" moves
        self.top.title('TicTacToe')
        self.top_frame = tk.Frame(self.top, width=490, height=550)
        self.top_frame.pack(fill=tk.BOTH, expand=1)
        self.button_frame = tk.Frame(self.top_frame, width=490, height=245)
        self.button_frame.pack(fill=tk.BOTH, expand=1)
        self.canvas_frame = tk.Frame(self.top_frame, width=490, height=245)
        self.canvas_frame.pack(fill=tk.BOTH, expand=1)
        # self.next_player = tk.BooleanVar()
        self.mode = self.get_mode("Which mode?\n")  # game mode
        # tie if moves finish
        # self.tie = True
        # self.moves = 0
        # self.next_player.set(self.player)

    def driver(self, mode, prev):  # Driver Function

        prev.destroy()  # close previous mode input window
        canv = self.widgets()  # canvas to show board and other text on
        self.top.wm_attributes('-topmost', True)  # make the game window active on top
        res, p1 = self.play_game(mode, canv)
        if res == -1:
            self.display("Match finished in a Tie")
        elif mode == "cp":
            if p1 == "p":
                if res == 1:
                    self.display("Player Wins")
                else:
                    self.display("Computer Wins")
            else:
                if res == 1:
                    self.display("Computer Wins")
                else:
                    self.display("Player Wins")
        else:
            self.display("Player " + str(res) + " Wins")

    def get_mode(self, msg, title='Mode'):  # to take game mode input
        tl = tk.Toplevel()
        tl.geometry("400x200+400+200")
        tl.title(title)
        tl.wm_attributes('-topmost', True)  # window to stay above all other windows
        lb = tk.Label(tl, text=msg, font=('Arial', 16))
        lb.grid(row=0, column=0, sticky=tk.W)
        mode = tk.StringVar()
        mode.set("cp")  # default radiobutton selected
        mode_rb1 = tk.Radiobutton(tl, text='Computer vs Player', variable=mode, value="cp")
        mode_rb1.grid(row=1, column=2, sticky=tk.W)
        mode_rb2 = tk.Radiobutton(tl, text='Computer vs Computer', variable=mode, value="c")
        mode_rb2.grid(row=2, column=2, sticky=tk.W)
        mode_rb3 = tk.Radiobutton(tl, text='Player vs Player', variable=mode, value="p")
        mode_rb3.grid(row=3, column=2, sticky=tk.W)
        ok = tk.Button(tl, text='Ok', font=('Arial', 15),
                       command=partial(self.driver, mode.get(), tl))
        # using partial function to be able to pass argument to driver
        ok.grid(row=4, column=2, columnspan=3, sticky=tk.S, pady=10)
        tl.lift()  # window to stay above all other application windows
        tl.wait_window()  # waits until the given window is destroyed
        return mode.get()

    def get_player1(self, msg, title='Player1'):  # to take player 1 input if mode is cp
        tl = tk.Toplevel()
        tl.geometry("400x200+400+200")
        tl.title(title)
        tl.wm_attributes('-topmost', True)  # window to stay above all other windows
        lb = tk.Label(tl, text=msg, font=('Arial', 16))
        lb.grid(row=0, column=0, sticky=tk.W)
        p1 = tk.StringVar()
        p1.set("p")  # default radiobutton selected
        p1_rb1 = tk.Radiobutton(tl, text='Player', variable=p1, value="p")
        p1_rb1.grid(row=1, column=2, sticky=tk.W)
        p1_rb2 = tk.Radiobutton(tl, text='Computer', variable=p1, value="c")
        p1_rb2.grid(row=2, column=2, sticky=tk.W)
        ok = tk.Button(tl, text='Ok', font=('Arial', 15),
                       command=tl.destroy)
        # using partial function to be able to pass argument to driver
        ok.grid(row=3, column=2, columnspan=3, sticky=tk.S, pady=10)
        tl.lift()  # window to stay above all other application windows
        tl.wait_window()  # waits until the given window is destroyed
        return p1.get()

    def widgets(self):
        """ create 9 buttons, a 3x3 grid
            create exit button
            create a canvas to draw board, other text and widgets
        """
        #X_img = tk.PhotoImage(file="x.png")
        button0 = tk.Button(self.button_frame, text='0', font=('Arial', 10), command=partial(self.cb_handler, 0),
                            bg="lightcyan",
                            activebackground="yellow", width=19, height=5)
        button0.grid(row=0, column=0, pady=2)
        button1 = tk.Button(self.button_frame, text='1', font=('Arial', 10), command=partial(self.cb_handler, 1),
                            bg="lightcyan",
                            activebackground="yellow", width=19, height=5)
        button1.grid(row=0, column=1, pady=2)
        button2 = tk.Button(self.button_frame, text='2', font=('Arial', 10), command=partial(self.cb_handler, 2),
                            bg="lightcyan",
                            activebackground="yellow", width=19, height=5)
        button2.grid(row=0, column=2, pady=2)
        button3 = tk.Button(self.button_frame, text='3', font=('Arial', 10), command=partial(self.cb_handler, 3),
                            bg="lightcyan",
                            activebackground="yellow", width=19, height=5)
        button3.grid(row=1, column=0, pady=2)
        button4 = tk.Button(self.button_frame, text='4', font=('Arial', 10), command=partial(self.cb_handler, 4),
                            bg="lightcyan",
                            activebackground="yellow", width=19, height=5)
        button4.grid(row=1, column=1, pady=2)
        button5 = tk.Button(self.button_frame, text='5', font=('Arial', 10), command=partial(self.cb_handler, 5),
                            bg="lightcyan",
                            activebackground="yellow", width=19, height=5)
        button5.grid(row=1, column=2, pady=2)
        button6 = tk.Button(self.button_frame, text='6', font=('Arial', 10), command=partial(self.cb_handler, 6),
                            bg="lightcyan",
                            activebackground="yellow", width=19, height=5)
        button6.grid(row=2, column=0, pady=2)
        button7 = tk.Button(self.button_frame, text='7', font=('Arial', 10), command=partial(self.cb_handler, 7),
                            bg="lightcyan",
                            activebackground="yellow", width=19, height=5)
        button7.grid(row=2, column=1, pady=2)
        button8 = tk.Button(self.button_frame, text='8', font=('Arial', 10), command=partial(self.cb_handler, 8),
                            bg="lightcyan",
                            activebackground="yellow", width=19, height=5)
        button8.grid(row=2, column=2, pady=2)
        sv = tk.StringVar()
        sv.set("EXIT")
        exit_b = tk.Button(self.button_frame, textvariable=sv, width=19, height=5, font=('Arial', 10),
                           command=partial(self.display, "Goodbye human"))
        exit_b.grid(row=3, column=1)

        c = tk.Canvas(self.canvas_frame, width=490, height=250,
                      bg="linen")
        c.pack(fill=tk.BOTH, expand=1)
        c.create_text(200, 25, text="Hello")
        return c

    def play_game(self, mode, canv):
        board_arr, tracker_dict = self.build_board()  # initial empty board and tracker dictionary
        winner = 0
        counter = 1
        out_str = str(self.drawboard(tracker_dict, mode))
        print(out_str)
        #canv.create_text(10,10,text=out_str)

        p1 = ""
        if mode == "cp":
            p1 = self.get_player1("Who will play first?")

        while winner == 0:
            for player in ["1", "2"]:
                if mode == "cp":
                    if p1 == "p":
                        if player == "1":
                            board_arr, tracker_dict = self.random_place(board_arr, "player", tracker_dict, mode,
                                                                        counter, p1)
                            print("\nBoard after move number " + str(counter) + " (Player)")

                        else:
                            board_arr, tracker_dict = self.random_place(board_arr, "comp", tracker_dict, mode, counter,
                                                                        p1)
                            print("\nBoard after move number " + str(counter) + " (Computer)")

                    elif p1 == "c":
                        if player == "1":
                            board_arr, tracker_dict = self.random_place(board_arr, "comp", tracker_dict, mode, counter,
                                                                        p1)
                            print("\nBoard after move number " + str(counter) + " (Computer)")
                        else:
                            board_arr, tracker_dict = self.random_place(board_arr, "player", tracker_dict, mode,
                                                                        counter, p1)
                            print("\nBoard after move number " + str(counter) + " (Player)")
                    self.drawboard(tracker_dict, mode)
                    counter += 1
                    winner = self.evaluate(board_arr, tracker_dict, mode, p1)
                    if winner != 0:
                        break
                else:
                    board_arr, tracker_dict = self.random_place(board_arr, player, tracker_dict, mode)
                    print("\nBoard after move number " + str(counter))
                    self.drawboard(tracker_dict, mode)
                    counter += 1
                    winner = self.evaluate(board_arr, tracker_dict, mode)
                    if winner != 0:
                        break
        while self.moves < 9 and self.tie:
            self.selection()
        try:
            self.stop()
        except tk.TclError:
            pass

        return winner, p1

    # Suitable places for the current player
    def random_place(self, ms_arr, player, ms_arr_dict, mode, *args):
        if mode == "c":
            selection = self.possibilities(ms_arr, ms_arr_dict, mode, "p" if player == "player" else "c")
            current_loc = random.choice(selection)
        elif mode == "p":
            selection = self.possibilities(ms_arr, ms_arr_dict, mode, "p" if player == "player" else "c")
            while (1):
                print("\n\nSelect location from: " + str(
                    selection) + " for player " + player + " move\t (unspaced, comma separated coordinates)")
                current_loc = list(map(int, input().split(",")))
                if (current_loc[0], current_loc[1]) not in selection:
                    print("Invalid move. Enter again")
                else:
                    break
        elif mode == "cp":
            counter = args[0]
            p1 = args[1]
            selection = self.possibilities(ms_arr, ms_arr_dict, mode, "p" if player == "player" else "c", counter, p1)
            if player == "player":
                while (1):
                    print("\n\nSelect location from: " + str(
                        selection) + " for player " + " move\t (unspaced, comma separated coordinates)")
                    current_loc = list(map(int, input().split(",")))
                    if (current_loc[0], current_loc[1]) not in selection:
                        print("Invalid move. Enter again")
                    else:
                        break
            elif player == "comp":
                current_loc = random.choice(selection)

            ms_arr_dict[ms_arr[current_loc[0]][current_loc[1]]] = "c" if player == "comp" else "p"
            return ms_arr, ms_arr_dict

        ms_arr_dict[ms_arr[current_loc[0]][current_loc[1]]] = player
        return ms_arr, ms_arr_dict

    # Return the appropriate move
    def possibilities(self, ms_arr, ms_arr_dict, mode, *args):
        q = []
        n = len(ms_arr)
        player = args[0]

        if mode == "p" or mode == "c" or (mode == "cp" and player == "p"):
            for i in range(n):
                for j in range(n):
                    if ms_arr_dict[ms_arr[i][j]] == "empty":
                        q.append((i, j))
            return q

        elif mode == "cp" and player == "c":
            counter = args[1]
            p1 = args[2]
            if p1 == "c":
                if counter == 1:
                    q.append((int(n / 2), int(n / 2)))
                    return q
                elif counter == 3:
                    if ms_arr_dict[ms_arr[n - 1][n - 1]] == "empty":
                        q.append((n - 1, n - 1))
                        return q
                    elif ms_arr_dict[ms_arr[0][n - 1]] == "empty":
                        q.append((0, n - 1))
                        return q
                elif counter == 5:
                    for i in range(n):
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "c"
                                if (self.row_win(ms_arr, "c", ms_arr_dict2) or self.col_win(ms_arr, "c",
                                                                                            ms_arr_dict2) or
                                        self.diag_win(ms_arr, "c", ms_arr_dict2)):
                                    q.append((i, j))
                                    return q
                    else:
                        for i in range(n):
                            for j in range(n):
                                ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                    ms_arr_dict2[ms_arr[i][j]] = "p"
                                    if (self.row_win(ms_arr, "p", ms_arr_dict2) or self.col_win(ms_arr, "p",
                                                                                                ms_arr_dict2) or
                                            self.diag_win(ms_arr, "p", ms_arr_dict2)):
                                        q.append((i, j))
                                        return q
                        else:
                            if ms_arr_dict[ms_arr[n - 1][0]] == "empty":
                                q.append((n - 1, 0))
                                return q
                            elif ms_arr_dict[ms_arr[0][n - 1]] == "empty":
                                q.append((0, n - 1))
                                return q
                elif counter == 7 or counter == 9:
                    for i in range(n):
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "c"
                                if (self.row_win(ms_arr, "c", ms_arr_dict2) or self.col_win(ms_arr, "c",
                                                                                            ms_arr_dict2) or
                                        self.diag_win(ms_arr, "c", ms_arr_dict2)):
                                    q.append((i, j))
                                    return q
                    else:
                        for i in range(n):
                            for j in range(n):
                                ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                    ms_arr_dict2[ms_arr[i][j]] = "p"
                                    if (self.row_win(ms_arr, "p", ms_arr_dict2) or self.col_win(ms_arr, "p",
                                                                                                ms_arr_dict2) or
                                            self.diag_win(ms_arr, "p", ms_arr_dict2)):
                                        q.append((i, j))
                                        return q
                        else:
                            for i in range(n):
                                for j in range(n):
                                    ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                    if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                        q.append((i, j))
                                        return q
            elif p1 == "p":
                if counter == 2:
                    if ms_arr_dict[ms_arr[int(n / 2)][int(n / 2)]] == "empty":
                        q.append((int(n / 2), int(n / 2)))
                    else:
                        q.append((0, 0))
                    return q
                elif counter == 4:
                    for i in range(n):  # block where p can win
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "p"
                                if (self.row_win(ms_arr, "p", ms_arr_dict2) or self.col_win(ms_arr, "p",
                                                                                            ms_arr_dict2) or
                                        self.diag_win(ms_arr, "p", ms_arr_dict2)):
                                    q.append((i, j))
                                    return q
                    else:  # else make2
                        if ms_arr_dict[ms_arr[int(n / 2)][int(n / 2)]] == "empty":  # middle place
                            q.append((int(n / 2), int(n / 2)))
                            return q
                        else:
                            if ms_arr_dict[ms_arr[0][0]] == "c":  # choose another corner
                                if ms_arr_dict[ms_arr[0][n - 2]] == "empty" and ms_arr_dict[
                                    ms_arr[0][n - 1]] == "empty":
                                    q.append((0, n - 1))
                                    return q
                                elif ms_arr_dict[ms_arr[n - 2][0]] == "empty" and ms_arr_dict[
                                    ms_arr[n - 1][0]] == "empty":
                                    q.append((n - 1, 0))
                                    return q
                            elif ms_arr_dict[ms_arr[int(n / 2)][int(n / 2)]] == "c":  # choose appropriate edge
                                # make corner if opponent has two opposite edges
                                if ((ms_arr_dict[ms_arr[0][int(n / 2)]] == "p" and ms_arr_dict[
                                    # top edge and bottom edge
                                    ms_arr[n - 1][int(n / 2)]] == "p") or
                                        (ms_arr_dict[ms_arr[int(n / 2)][0]] == "p" and ms_arr_dict[
                                            ms_arr[int(n / 2)][n - 1]] == "p")):
                                    q.append((0, 0))
                                    return q
                                elif (ms_arr_dict[ms_arr[0][int(n / 2)]] == "p" and ms_arr_dict[
                                    # top edge and left edge
                                    ms_arr[int(n / 2)][0]] == "p"):
                                    q.append((0, 0))
                                    return q
                                elif (ms_arr_dict[ms_arr[0][int(n / 2)]] == "p" and ms_arr_dict[
                                    # top edge and right edge
                                    ms_arr[int(n / 2)][n - 1]] == "p"):
                                    q.append((0, n - 1))
                                    return q
                                elif (ms_arr_dict[ms_arr[n - 1][int(n / 2)]] == "p" and ms_arr_dict[
                                    # bottom edge and left edge
                                    ms_arr[int(n / 2)][0]] == "p"):
                                    q.append((n - 1, 0))
                                    return q
                                elif (ms_arr_dict[ms_arr[n - 1][int(n / 2)]] == "p" and ms_arr_dict[
                                    # bottom edge and right edge
                                    ms_arr[int(n / 2)][n - 1]] == "p"):
                                    q.append((0, n - 1))
                                    return q
                                elif ms_arr_dict[ms_arr[0][int(n / 2)]] == "empty" and ms_arr_dict[
                                    # top edge and bottom edge
                                    ms_arr[n - 1][int(n / 2)]] == "empty":
                                    q.append((0, int(n / 2)))
                                    return q
                                elif ms_arr_dict[ms_arr[int(n / 2)][0]] == "empty" and ms_arr_dict[
                                    # left edge and right edge
                                    ms_arr[int(n / 2)][n - 1]] == "empty":
                                    q.append((int(n / 2), 0))
                                    return q
                                elif ms_arr_dict[ms_arr[n - 1][0]] == "empty" and ms_arr_dict[
                                    # bottom left corner and bottom right corner
                                    ms_arr[n - 1][n - 1]] == "empty":
                                    q.append((n - 1, 0))
                                    return q
                elif counter == 6:
                    for i in range(n):  # check if c can win
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "c"
                                if (self.row_win(ms_arr, "c", ms_arr_dict2) or self.col_win(ms_arr, "c",
                                                                                            ms_arr_dict2) or
                                        self.diag_win(ms_arr, "c", ms_arr_dict2)):
                                    q.append((i, j))
                                    return q
                    else:
                        for i in range(n):  # check and block if p can win
                            for j in range(n):
                                ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                    ms_arr_dict2[ms_arr[i][j]] = "p"
                                    if (self.row_win(ms_arr, "p", ms_arr_dict2) or self.col_win(ms_arr, "p",
                                                                                                ms_arr_dict2) or
                                            self.diag_win(ms_arr, "p", ms_arr_dict2)):
                                        q.append((i, j))
                                        return q
                        else:
                            if ms_arr_dict[ms_arr[int(n / 2)][int(n / 2)]] == "empty":  # middle place
                                q.append((int(n / 2), int(n / 2)))
                                return q
                            else:  # choose where c can win on next 2 moves
                                for i in range(n):
                                    for j in range(n):
                                        ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                        if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                            ms_arr_dict2[ms_arr[i][j]] = "c"
                                            for k in range(n):
                                                for l in range(n):
                                                    ms_arr_dict22 = copy.deepcopy(ms_arr_dict2)
                                                    if ms_arr_dict22[ms_arr[k][l]] == "empty":
                                                        ms_arr_dict2[ms_arr[k][l]] = "c"
                                                        if (self.row_win(ms_arr, "c", ms_arr_dict22) or
                                                                self.col_win(ms_arr, "c", ms_arr_dict22) or
                                                                self.diag_win(ms_arr, "c", ms_arr_dict22)):
                                                            q.append((i, j))
                                                            return q
                elif counter == 8:
                    for i in range(n):  # check if c can win
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "c"
                                if (self.row_win(ms_arr, "c", ms_arr_dict2) or self.col_win(ms_arr, "c",
                                                                                            ms_arr_dict2) or
                                        self.diag_win(ms_arr, "c", ms_arr_dict2)):
                                    q.append((i, j))
                                    return q
                    else:
                        for i in range(n):  # check if p can win
                            for j in range(n):
                                ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                    ms_arr_dict2[ms_arr[i][j]] = "p"
                                    if (self.row_win(ms_arr, "p", ms_arr_dict2) or self.col_win(ms_arr, "p",
                                                                                                ms_arr_dict2) or
                                            self.diag_win(ms_arr, "p", ms_arr_dict2)):
                                        q.append((i, j))
                                        return q
                        else:
                            for i in range(n):  # go anywhere
                                for j in range(n):
                                    ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                    if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                        q.append((i, j))
                                        return q

    # Checks whether the player has three
    # of their marks in a horizontal row
    def row_win(self, ms_arr, player, ms_arr_dict):
        win = False
        n = len(ms_arr)
        for x in range(len(ms_arr)):
            sum = 0
            for y in range(len(ms_arr)):
                if ms_arr_dict[ms_arr[x][y]] == player:
                    sum += ms_arr[x][y]
                else:
                    win = False
                    continue
            if sum == n * (n ** 2 + 1) / 2:
                win = True
                return win
        return win

    # Checks whether the player has three
    # of their marks in a vertical row
    def col_win(self, ms_arr, player, ms_arr_dict):
        win = False
        n = len(ms_arr)
        for x in range(len(ms_arr)):
            sum = 0
            for y in range(len(ms_arr)):
                if ms_arr_dict[ms_arr[y][x]] == player:
                    sum += ms_arr[y][x]
                else:
                    win = False
                    continue
            if sum == n * (n ** 2 + 1) / 2:
                win = True
                return win
        return win

    # Checks whether the player has three
    # of their marks in a diagonal row
    def diag_win(self, ms_arr, player, ms_arr_dict):
        win = False
        n = len(ms_arr)
        sum = 0
        for x in range(len(ms_arr)):  # left diagonal
            if ms_arr_dict[ms_arr[x][x]] == player:
                sum += ms_arr[x][x]
            else:
                win = False
                break
        if sum == n * (n ** 2 + 1) / 2:
            win = True
            return win

        sum = 0
        for x in range(len(ms_arr)):  # right diagonal
            if ms_arr_dict[ms_arr[x][len(ms_arr) - 1 - x]] == player:
                sum += ms_arr[x][x]
            else:
                win = False
                break
        if sum == n * (n ** 2 + 1) / 2:
            win = True
            return win
        return win

    # Evaluates whether there is
    # a winner or a tie
    def evaluate(self, ms_arr, ms_arr_dict, mode, *args):
        winner = 0
        if mode == "cp":
            p1 = args[0]
        for player in ["1", "2"]:
            if mode == "cp":
                if p1 == "p":
                    if player == "1":
                        if (self.row_win(ms_arr, "p", ms_arr_dict) or self.col_win(ms_arr, "p", ms_arr_dict) or
                                self.diag_win(ms_arr, "p", ms_arr_dict)):
                            winner = int(player)
                            break
                    else:
                        if (self.row_win(ms_arr, "c", ms_arr_dict) or self.col_win(ms_arr, "c", ms_arr_dict) or
                                self.diag_win(ms_arr, "c", ms_arr_dict)):
                            winner = int(player)
                            break
                else:
                    if player == "1":
                        if (self.row_win(ms_arr, "c", ms_arr_dict) or self.col_win(ms_arr, "c", ms_arr_dict) or
                                self.diag_win(ms_arr, "c", ms_arr_dict)):
                            winner = int(player)
                            break
                    else:
                        if (self.row_win(ms_arr, "p", ms_arr_dict) or self.col_win(ms_arr, "p", ms_arr_dict) or
                                self.diag_win(ms_arr, "p", ms_arr_dict)):
                            winner = int(player)
                            break

            else:
                if (self.row_win(ms_arr, player, ms_arr_dict) or self.col_win(ms_arr, player, ms_arr_dict)
                        or self.diag_win(ms_arr, player, ms_arr_dict)):
                    winner = int(player)
                    break

        if winner == 1 or winner == 2:
            return winner
        for x in ms_arr_dict:  # either match has not finished or it is a tie
            if ms_arr_dict[x] == "empty":
                return winner  # 0 - match not finished
            # if loop falls through without encountering the return statement, it is a tie
        winner = -1
        return winner


    def stop(self):
        if self.moves == 99:
            # second stop ignored
            return

        if not self.tie:
            # self.X_O_dict['X'] = range(10)
            self.display("Winner is O" if self.player else "Winner is X")
        elif self.moves == 9:
            self.display("...It's A TIE.....")
        else:
            self.display("Quitter!")
            self.moves = 99
            self.tie = False
        # unsetting wait events
        self.next_player.set(self.player)
        self.top.destroy()
        # raise SystemExit('Bye, bye')

    def cb_handler(self, square_number):
        this_player = "X" if self.player else "O"
        ##--- square not already occupied
        if self.legal_move(square_number):
            ## change button's text to "X" or "O"
            self.button_dic[square_number][0].set(this_player)
            self.X_O_dict[this_player].append(square_number)
            ## set background to occupied color
            self.button_dic[square_number][1].config(bg="lightgray")
            self.check_for_winner(self.X_O_dict[this_player])
            self.player = not self.player
            self.next_player.set(self.player)
        else:
            print
            "Occupied, pick another", square_number

    def check_for_winner(self, list_in):
        set_in = set(list_in)
        if any(winner.issubset(set_in) for winner in self.winners):
            self.tie = False

    def check_two_in_a_row(self):
        """ check for two, but not three, in a row
              if player="X", move to win
              if player="O", move to block
            one check for either strategy
        """
        ## check to win first and then to block
        for player in ["X", "O"]:
            this = set(self.X_O_dict[player])
            for sub_set in self.winners:
                if len(this & sub_set) == 2:
                    one_to_return = next(iter(sub_set - this))
                    # all one of  them legal, then return
                    if self.legal_move(one_to_return):
                        return one_to_return

    def display(self, msg, title='Message'):  # to display any kind of message
        tl = tk.Toplevel()
        tl.geometry("400x200+400+200")
        tl.title(title)
        tl.wm_attributes('-topmost', True)  # window to stay above all other windows
        lb = tk.Label(tl, text=msg, font=('Arial', 16))
        lb.pack(fill='both', expand=True)
        tl.lift()  # window to stay above all other application windows
        tl.wait_window()  # waits until the given window is destroyed

    def legal_move(self, square_number):
        return (square_number not in self.X_O_dict["X"] and
                square_number not in self.X_O_dict["O"])

    def selection(self):
        ## computer moves
        if self.player:
            ## don't accept button clicks when it is computer's (X) turn
            for but in self.button_dic:
                self.button_dic[but][1].state = tk.DISABLED
            move_to_take = self.check_two_in_a_row()
            if move_to_take is not None:
                self.cb_handler(move_to_take)
            else:
                ## sequence = middle square, and then each corner as the
                ## 2 middle rows are elmininated by the middle square
                for chosen in (5, 1, 3, 7, 9, 2, 4, 6, 8):
                    if self.legal_move(chosen):
                        self.cb_handler(chosen)
                        break
        else:
            ## person moves, set buttons back to normal
            for but in self.button_dic:
                self.button_dic[but][1].state = tk.NORMAL
            # we can wait variable change, because they are BooleanVars
            self.top.wait_variable(self.next_player)
        self.moves += 1

    def magic(self, ms_arr, n):  # create a magic square
        ms_arr[int(n / 2)][n - 1] = 1
        r = int(n / 2) - 1
        c = n - 1 + 1
        for p in range(2, n * n + 1):
            if r == -1 and c == n:
                r = 0
                c = n - 2
            else:
                if r == -1:
                    r = n - 1
                elif c == n:
                    c = 0
                if ms_arr[r][c] != 0:
                    r += 1
                    c -= 2
            ms_arr[r][c] = p
            r = r - 1
            c = c + 1
        return ms_arr

    def build_board(self):  # build tic tac toe board from magic square
        n = 3  # dimension of magic square
        ms_arr = [[0 for q in range(n)] for p in range(n)]
        ms_arr = self.magic(ms_arr, n)
        ms_arr_dict = {}
        for i in range(len(ms_arr)):
            for j in range(len(ms_arr)):
                ms_arr_dict.update({ms_arr[i][j]: "empty"})
        return ms_arr, ms_arr_dict

    def drawboard(self, ms_arr_dict, mode):  # return a string used to display the board

        i = 0
        out_str = ""

        for x in ms_arr_dict:
            if i == 3:
                i = 0
                out_str += "\n_________\n"
            i += 1
            if ms_arr_dict[x] == "empty":
                out_str += ("_" + "   ")
            else:
                out_str += (str(ms_arr_dict[x]) + " \t")

        if mode == "cp":
            out_str += ("\n\nList 1 : ")
            for x in ms_arr_dict:
                if ms_arr_dict[x] == "p":
                    out_str += (str(x) + "\t\t")

            out_str += ("\n\nList 2 : ")
            for x in ms_arr_dict:
                if ms_arr_dict[x] == "c":
                    out_str += (str(x) + "\t\t")

        return out_str

# .....................................................................................................................

# .............................................Start Game by instancing class..........................................

game = TicTacToe(tk.Tk())

# .....................................................................................................................
