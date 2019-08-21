# ................................................IMPORTS..............................................................

import tkinter as tk
import copy
from functools import partial


# .....................................................................................................................

# .............................................Tic Tac Toe Class.......................................................

class TicTacToe(object):

    def __init__(self, top):  # constructor

        self.top = top
        self.top.geometry("490x700+400+50")  # dimensions and offset on screen
        self.top.title('TicTacToe')
        self.top_frame = tk.Frame(self.top, width=490, height=700)
        self.top_frame.pack(fill=tk.BOTH, expand=1)
        self.button_frame = tk.Frame(self.top_frame, width=490, height=245)
        self.button_frame.pack(fill=tk.BOTH, expand=1)
        self.canvas_frame = tk.Frame(self.top_frame, width=490, height=450)
        self.canvas_frame.pack(fill=tk.BOTH, expand=1)

        self.button_dic = {}
        self.moves = 0
        self.board_arr, self.tracker_dict = self.build_board()  # initial empty board and tracker dictionary

        self.canv = self.widgets()  # create widgets and return canvas to show board and other text on

        out_str = ("\nMagic Square generated\n")
        for i in range(len(self.board_arr)):
            out_str += str(self.board_arr[i]) + "\n"

        self.canv.create_text(250, 160, text=out_str + "\n" + str(self.drawboard(self.tracker_dict)),
                              font=("Arial", 12))
        self.res = -1  # tie
        self.p1 = self.get_player1("Who will play first?")
        self.player = self.p1
        self.top.wm_attributes('-topmost', True)
        self.next_player = tk.StringVar()
        self.next_player.set(self.player)
        if self.p1 == "C":  # if computer plays first, occupy middle place
            self.cmp_1move()
        self.top.wait_window()

    def cmp_1move(self):
        print("inside")
        self.button_dic[4][1].config(text="C")
        self.tracker_dict[self.board_arr[int(4 / 3)][4 % 3]] = "C"
        self.button_dic[4][1].config(bg="lightgray")
        self.player = "P"
        self.next_player.set(self.player)
        self.moves += 1

    # .................................................................................................................

    def get_player1(self, msg, title='Player1'):  # to take player 1 input if mode is cp
        tl = tk.Toplevel()
        tl.geometry("400x200+400+200")
        tl.title(title)
        tl.wm_attributes('-topmost', True)  # window to stay above all other windows
        lb = tk.Label(tl, text=msg, font=('Arial', 16))
        lb.grid(row=0, column=0, sticky=tk.W)
        p1 = tk.StringVar()
        p1.set("C")  # default radiobutton selected
        p1_rb1 = tk.Radiobutton(tl, text='Player', variable=p1, value="P")
        p1_rb1.grid(row=1, column=2, sticky=tk.W)
        p1_rb2 = tk.Radiobutton(tl, text='Computer', variable=p1, value="C")
        p1_rb2.grid(row=2, column=2, sticky=tk.W)
        ok = tk.Button(tl, text='Ok', font=('Arial', 15),
                       command=tl.destroy)
        # using partial function to be able to pass argument to driver
        ok.grid(row=3, column=2, columnspan=3, sticky=tk.S, pady=10)
        tl.lift()  # window to stay above all other application windows
        tl.wait_window()  # waits until the given window is destroyed
        return p1.get()

    # .................................................................................................................

    def widgets(self):
        """ create 9 buttons, a 3x3 grid
            create exit button
            create a canvas to draw board, other text and widgets
        """

        b_row = 0
        b_col = 0
        for j in range(0, 9):
            sv = tk.StringVar()
            sv.set(j)
            b = tk.Button(self.button_frame, text=str(j), font=('Arial', 10), command=partial(self.cb_handler, j),
                          bg="lightcyan",
                          activebackground="yellow", width=19, height=5)
            b.grid(row=b_row, column=b_col, pady=2)
            self.button_dic[j] = [sv, b]
            b_col += 1
            if b_col > 2:
                b_col = 0
                b_row += 1

        sv = tk.StringVar()
        sv.set("EXIT")
        exit_b = tk.Button(self.button_frame, textvariable=sv, width=19, height=5, font=('Arial', 10),
                           command=partial(self.display, "Thank you for playing"))
        exit_b.grid(row=3, column=1)

        c = tk.Canvas(self.canvas_frame, width=490, height=300,
                      bg="linen")
        c.pack(fill=tk.BOTH, expand=1)
        c.create_text(200, 20, text="Hello", font=("Arial", 12))
        c.create_bitmap(235, 20, bitmap="warning")
        return c

    # .................................................................................................................

    # Return the appropriate move
    def possibilities(self, ms_arr, ms_arr_dict):
        q = []
        n = len(ms_arr)
        if self.p1 == "C":
            if self.moves == 1:
                q.append((int(n / 2), int(n / 2)))
                return q
            elif self.moves == 3:
                if ms_arr_dict[ms_arr[n - 1][n - 1]] == "empty":
                    q.append((n - 1, n - 1))
                    return q
                elif ms_arr_dict[ms_arr[0][n - 1]] == "empty":
                    q.append((0, n - 1))
                    return q
            elif self.moves == 5:
                for i in range(n):
                    for j in range(n):
                        ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                        if ms_arr_dict2[ms_arr[i][j]] == "empty":
                            ms_arr_dict2[ms_arr[i][j]] = "C"
                            if (self.row_win(ms_arr, "C", ms_arr_dict2) or self.col_win(ms_arr, "C",
                                                                                        ms_arr_dict2) or
                                    self.diag_win(ms_arr, "C", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:
                    for i in range(n):
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "P"
                                if (self.row_win(ms_arr, "P", ms_arr_dict2) or self.col_win(ms_arr, "P",
                                                                                            ms_arr_dict2) or
                                        self.diag_win(ms_arr, "P", ms_arr_dict2)):
                                    q.append((i, j))
                                    return q
                    else:
                        if ms_arr_dict[ms_arr[n - 1][0]] == "empty":
                            q.append((n - 1, 0))
                            return q
                        elif ms_arr_dict[ms_arr[0][n - 1]] == "empty":
                            q.append((0, n - 1))
                            return q
            elif self.moves == 7 or self.moves == 9:
                for i in range(n):
                    for j in range(n):
                        ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                        if ms_arr_dict2[ms_arr[i][j]] == "empty":
                            ms_arr_dict2[ms_arr[i][j]] = "C"
                            if (self.row_win(ms_arr, "C", ms_arr_dict2) or self.col_win(ms_arr, "C",
                                                                                        ms_arr_dict2) or
                                    self.diag_win(ms_arr, "C", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:
                    for i in range(n):
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "P"
                                if (self.row_win(ms_arr, "P", ms_arr_dict2) or self.col_win(ms_arr, "P",
                                                                                            ms_arr_dict2) or
                                        self.diag_win(ms_arr, "P", ms_arr_dict2)):
                                    q.append((i, j))
                                    return q
                    else:
                        for i in range(n):
                            for j in range(n):
                                ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                    q.append((i, j))
                                    return q
        elif self.p1 == "P":
            if self.moves == 2:
                if ms_arr_dict[ms_arr[int(n / 2)][int(n / 2)]] == "empty":
                    q.append((int(n / 2), int(n / 2)))
                else:
                    q.append((0, 0))
                return q
            elif self.moves == 4:
                for i in range(n):  # block where p can win
                    for j in range(n):
                        ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                        if ms_arr_dict2[ms_arr[i][j]] == "empty":
                            ms_arr_dict2[ms_arr[i][j]] = "P"
                            if (self.row_win(ms_arr, "P", ms_arr_dict2) or self.col_win(ms_arr, "P",
                                                                                        ms_arr_dict2) or
                                    self.diag_win(ms_arr, "P", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:  # else make2
                    if ms_arr_dict[ms_arr[int(n / 2)][int(n / 2)]] == "empty":  # middle place
                        q.append((int(n / 2), int(n / 2)))
                        return q
                    else:
                        if ms_arr_dict[ms_arr[0][0]] == "C":  # choose another corner
                            if ms_arr_dict[ms_arr[0][n - 2]] == "empty" and ms_arr_dict[
                                ms_arr[0][n - 1]] == "empty":
                                q.append((0, n - 1))
                                return q
                            elif ms_arr_dict[ms_arr[n - 2][0]] == "empty" and ms_arr_dict[
                                ms_arr[n - 1][0]] == "empty":
                                q.append((n - 1, 0))
                                return q
                        elif ms_arr_dict[ms_arr[int(n / 2)][int(n / 2)]] == "C":  # choose appropriate edge
                            # make corner if opponent has two opposite edges
                            if ((ms_arr_dict[ms_arr[0][int(n / 2)]] == "P" and ms_arr_dict[
                                # top edge and bottom edge
                                ms_arr[n - 1][int(n / 2)]] == "P") or
                                    (ms_arr_dict[ms_arr[int(n / 2)][0]] == "P" and ms_arr_dict[
                                        ms_arr[int(n / 2)][n - 1]] == "P")):
                                q.append((0, 0))
                                return q
                            elif (ms_arr_dict[ms_arr[0][int(n / 2)]] == "P" and ms_arr_dict[
                                # top edge and left edge
                                ms_arr[int(n / 2)][0]] == "P"):
                                q.append((0, 0))
                                return q
                            elif (ms_arr_dict[ms_arr[0][int(n / 2)]] == "P" and ms_arr_dict[
                                # top edge and right edge
                                ms_arr[int(n / 2)][n - 1]] == "P"):
                                q.append((0, n - 1))
                                return q
                            elif (ms_arr_dict[ms_arr[n - 1][int(n / 2)]] == "P" and ms_arr_dict[
                                # bottom edge and left edge
                                ms_arr[int(n / 2)][0]] == "P"):
                                q.append((n - 1, 0))
                                return q
                            elif (ms_arr_dict[ms_arr[n - 1][int(n / 2)]] == "P" and ms_arr_dict[
                                # bottom edge and right edge
                                ms_arr[int(n / 2)][n - 1]] == "P"):
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
            elif self.moves == 6:
                for i in range(n):  # check if c can win
                    for j in range(n):
                        ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                        if ms_arr_dict2[ms_arr[i][j]] == "empty":
                            ms_arr_dict2[ms_arr[i][j]] = "C"
                            if (self.row_win(ms_arr, "C", ms_arr_dict2) or self.col_win(ms_arr, "C",
                                                                                        ms_arr_dict2) or
                                    self.diag_win(ms_arr, "C", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:
                    for i in range(n):  # check and block if p can win
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "P"
                                if (self.row_win(ms_arr, "P", ms_arr_dict2) or self.col_win(ms_arr, "P",
                                                                                            ms_arr_dict2) or
                                        self.diag_win(ms_arr, "P", ms_arr_dict2)):
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
                                        ms_arr_dict2[ms_arr[i][j]] = "C"
                                        for k in range(n):
                                            for l in range(n):
                                                ms_arr_dict22 = copy.deepcopy(ms_arr_dict2)
                                                if ms_arr_dict22[ms_arr[k][l]] == "empty":
                                                    ms_arr_dict2[ms_arr[k][l]] = "C"
                                                    if (self.row_win(ms_arr, "C", ms_arr_dict22) or
                                                            self.col_win(ms_arr, "C", ms_arr_dict22) or
                                                            self.diag_win(ms_arr, "C", ms_arr_dict22)):
                                                        q.append((i, j))
                            if not len(q):
                                for i in range(len(ms_arr)):  # go anywhere
                                    for j in range(len(ms_arr)):
                                        ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                        if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                            q.append((i, j))
                            return q
            elif self.moves == 8:
                for i in range(n):  # check if c can win
                    for j in range(n):
                        ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                        if ms_arr_dict2[ms_arr[i][j]] == "empty":
                            ms_arr_dict2[ms_arr[i][j]] = "C"
                            if (self.row_win(ms_arr, "C", ms_arr_dict2) or self.col_win(ms_arr, "C",
                                                                                        ms_arr_dict2) or
                                    self.diag_win(ms_arr, "C", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:
                    for i in range(n):  # check if p can win
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "P"
                                if (self.row_win(ms_arr, "P", ms_arr_dict2) or self.col_win(ms_arr, "P",
                                                                                            ms_arr_dict2) or
                                        self.diag_win(ms_arr, "P", ms_arr_dict2)):
                                    q.append((i, j))
                                    return q
                    else:
                        for i in range(n):  # go anywhere
                            for j in range(n):
                                ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                    q.append((i, j))
                                    return q

    # .................................................................................................................

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

    # .................................................................................................................

    def cb_handler(self, square_number):  # action to take when a button is pressed

        this_player = self.p1 if self.moves < 1 else self.player
        winner = 0
        if self.legal_move(square_number) and self.moves < 9 and (self.res != 1 or self.res != 2):
            self.button_dic[square_number][1].config(text=self.player)
            self.tracker_dict[self.board_arr[int(square_number / 3)][square_number % 3]] = this_player
            self.button_dic[square_number][1].config(bg="light grey")
            self.player = "C" if self.player == "P" else "P"
            print(self.moves)
            self.canv.delete("all")
            self.canv.create_text(250, 150, text=str(self.drawboard(self.tracker_dict)), font=("Arial", 16))
            self.next_player.set(self.player)
            self.moves += 1
            print(self.moves)
            winner = self.check_for_win(this_player)
            if winner:  # if player wins on his move
                self.display(this_player + " Wins")
                self.res = 1 if self.p1 == "P" else 2
                self.top.destroy()
            else:
                # calculate comp's move and make it
                self.moves += 1
                current_loc = self.possibilities(self.board_arr, self.tracker_dict)
                square_number = current_loc[0][0] * len(self.board_arr) + current_loc[0][1]
                self.button_dic[square_number][1].config(text="C")
                self.tracker_dict[self.board_arr[int(square_number / 3)][square_number % 3]] = "C"
                self.button_dic[square_number][1].config(bg="light grey")
                self.player = "C" if self.player == "P" else "P"
                self.canv.delete("all")
                self.canv.create_text(250, 150, text=str(self.drawboard(self.tracker_dict)), font=("Arial", 16))
                self.next_player.set(self.player)

                winner = self.check_for_win("C")
                if winner:
                    self.display("C" + " Wins")
                    self.res = 1 if self.p1 == "P" else 2

                    self.top.destroy()
                elif self.moves == 9:
                    self.display("Match is a tie")
                    self.res = -1
                    self.top.destroy()
        if self.moves == 8 and winner == 0:
            self.display("Match is a tie")
            self.res = -1
            self.top.destroy()

    def check_for_win(self, player):  # method to check for computer or player's win
        winner = (self.row_win(self.board_arr, player, self.tracker_dict) or self.col_win(self.board_arr, player,
                                                                                          self.tracker_dict) or
                  self.diag_win(self.board_arr, player, self.tracker_dict))
        return winner

    # .................................................................................................................

    def display(self, msg, title='Message'):  # to display any kind of message
        tl = tk.Toplevel()
        tl.geometry("400x200+400+200")
        tl.title(title)
        tl.wm_attributes('-topmost', True)  # window to stay above all other windows
        lb = tk.Label(tl, text=msg, font=('Arial', 16))
        lb.pack(fill='both', expand=True)
        tl.lift()  # window to stay above all other application windows
        tl.wait_window()  # waits until the given window is destroyed

    # .................................................................................................................

    def legal_move(self, square_number):
        return (self.tracker_dict[self.board_arr[int(square_number / 3)][square_number % 3]] == "empty")

    # .................................................................................................................

    def magic(self, ms_arr, n):  # function to create a magic square
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

    # .................................................................................................................

    def build_board(self):  # build tic tac toe board from magic square
        n = 3  # dimension of magic square
        ms_arr = [[0 for q in range(n)] for p in range(n)]
        ms_arr = self.magic(ms_arr, n)
        ms_arr_dict = {}
        for i in range(len(ms_arr)):
            for j in range(len(ms_arr)):
                ms_arr_dict.update({ms_arr[i][j]: "empty"})
        return ms_arr, ms_arr_dict

    # .................................................................................................................

    def drawboard(self, ms_arr_dict):
        # return a string used to display game board along with the lists of both players

        i = 0
        out_str = ""

        for x in ms_arr_dict:
            if i == 3:
                i = 0
                out_str += "\n______\n"
            i += 1
            if ms_arr_dict[x] == "empty":
                out_str += ("_" + "   ")
            else:
                out_str += (str(ms_arr_dict[x]) + "  ")

        out_str += ("\n\nList 1 : ")
        for x in ms_arr_dict:
            if ms_arr_dict[x] == "P":
                out_str += (str(x) + "  ")

        out_str += ("\n\nList 2 : ")
        for x in ms_arr_dict:
            if ms_arr_dict[x] == "C":
                out_str += (str(x) + "  ")

        return out_str


# .....................................................................................................................

# .............................................Start Game by instancing class..........................................

game = TicTacToe(tk.Tk())

# .....................................................................................................................
