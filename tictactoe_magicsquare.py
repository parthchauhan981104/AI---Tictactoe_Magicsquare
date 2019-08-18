import random
import copy


def magic(ms_arr, n):
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


def build_board():
    n = 3  # dimension of magic square
    ms_arr = [[0 for q in range(n)] for p in range(n)]
    ms_arr = magic(ms_arr, n)
    ms_arr_dict = {}
    for i in range(len(ms_arr)):
        for j in range(len(ms_arr)):
            ms_arr_dict.update({ms_arr[i][j]: "empty"})
    return ms_arr, ms_arr_dict


# Check for empty places on board
def possibilities(ms_arr, ms_arr_dict, mode, *args):
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
                            if (row_win(ms_arr, "c", ms_arr_dict2) or col_win(ms_arr, "c", ms_arr_dict2) or
                                    diag_win(ms_arr, "c", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:
                    for i in range(n):
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "p"
                                if (row_win(ms_arr, "p", ms_arr_dict2) or col_win(ms_arr, "p", ms_arr_dict2) or
                                        diag_win(ms_arr, "p", ms_arr_dict2)):
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
                            if (row_win(ms_arr, "c", ms_arr_dict2) or col_win(ms_arr, "c", ms_arr_dict2) or
                                    diag_win(ms_arr, "c", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:
                    for i in range(n):
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "p"
                                if (row_win(ms_arr, "p", ms_arr_dict2) or col_win(ms_arr, "p", ms_arr_dict2) or
                                        diag_win(ms_arr, "p", ms_arr_dict2)):
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
                            if (row_win(ms_arr, "p", ms_arr_dict2) or col_win(ms_arr, "p", ms_arr_dict2) or
                                    diag_win(ms_arr, "p", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:  # else make2
                    if ms_arr_dict[ms_arr[int(n / 2)][int(n / 2)]] == "empty":  # middle place
                        q.append((int(n / 2), int(n / 2)))
                        return q
                    else:
                        if ms_arr_dict[ms_arr[0][0]] == "c":  # choose another corner
                            if ms_arr_dict[ms_arr[0][n - 2]] == "empty" and ms_arr_dict[ms_arr[0][n - 1]] == "empty":
                                q.append((0, n - 1))
                                return q
                            elif ms_arr_dict[ms_arr[n - 2][0]] == "empty" and ms_arr_dict[ms_arr[n - 1][0]] == "empty":
                                q.append((n - 1, 0))
                                return q
                        elif ms_arr_dict[ms_arr[int(n / 2)][int(n / 2)]] == "c":  # choose appropriate edge
                            # make corner if opponent has two opposite edges
                            if ((ms_arr_dict[ms_arr[0][int(n / 2)]] == "p" and ms_arr_dict[
                                ms_arr[n - 1][int(n / 2)]] == "p") or
                                    (ms_arr_dict[ms_arr[int(n / 2)][0]] == "p" and ms_arr_dict[
                                        ms_arr[int(n / 2)][n - 1]] == "p")):
                                q.append((0, 0))
                                return q
                            elif (ms_arr_dict[ms_arr[0][int(n / 2)]] == "p" and ms_arr_dict[
                                ms_arr[int(n / 2)][0]] == "p"):
                                q.append((0, 0))
                                return q
                            elif (ms_arr_dict[ms_arr[0][int(n / 2)]] == "p" and ms_arr_dict[
                                ms_arr[int(n / 2)][n - 1]] == "p"):
                                q.append((0, n - 1))
                                return q
                            elif (ms_arr_dict[ms_arr[n - 1][int(n / 2)]] == "p" and ms_arr_dict[
                                ms_arr[int(n / 2)][0]] == "p"):
                                q.append((n - 1, 0))
                                return q
                            elif (ms_arr_dict[ms_arr[n - 1][int(n / 2)]] == "p" and ms_arr_dict[
                                ms_arr[int(n / 2)][n - 1]] == "p"):
                                q.append((0, n - 1))
                                return q
                            elif ms_arr_dict[ms_arr[0][int(n / 2)]] == "empty" and ms_arr_dict[
                                ms_arr[n - 1][int(n / 2)]] == "empty":
                                q.append((0, int(n / 2)))
                                return q
                            elif ms_arr_dict[ms_arr[int(n / 2)][0]] == "empty" and ms_arr_dict[
                                ms_arr[int(n / 2)][n - 1]] == "empty":
                                q.append((int(n / 2), 0))
                                return q
                            elif ms_arr_dict[ms_arr[n - 1][0]] == "empty" and ms_arr_dict[
                                ms_arr[n - 1][n - 1]] == "empty":
                                q.append((n - 1, 0))
                                return q
            elif counter == 6:
                for i in range(n):  # check if c can win
                    for j in range(n):
                        ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                        if ms_arr_dict2[ms_arr[i][j]] == "empty":
                            ms_arr_dict2[ms_arr[i][j]] = "c"
                            if (row_win(ms_arr, "c", ms_arr_dict2) or col_win(ms_arr, "c", ms_arr_dict2) or
                                    diag_win(ms_arr, "c", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:
                    for i in range(n):  # check and block if p can win
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "p"
                                if (row_win(ms_arr, "p", ms_arr_dict2) or col_win(ms_arr, "p", ms_arr_dict2) or
                                        diag_win(ms_arr, "p", ms_arr_dict2)):
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
                                                if (row_win(ms_arr, "c", ms_arr_dict22) or
                                                        col_win(ms_arr, "c", ms_arr_dict22) or
                                                        diag_win(ms_arr, "c", ms_arr_dict22)):
                                                    q.append((i, j))
                                                    return q
            elif counter == 8:
                for i in range(n):  # check if c can win
                    for j in range(n):
                        ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                        if ms_arr_dict2[ms_arr[i][j]] == "empty":
                            ms_arr_dict2[ms_arr[i][j]] = "c"
                            if (row_win(ms_arr, "c", ms_arr_dict2) or col_win(ms_arr, "c", ms_arr_dict2) or
                                    diag_win(ms_arr, "c", ms_arr_dict2)):
                                q.append((i, j))
                                return q
                else:
                    for i in range(n):  # check if p can win
                        for j in range(n):
                            ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                            if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                ms_arr_dict2[ms_arr[i][j]] = "p"
                                if (row_win(ms_arr, "p", ms_arr_dict2) or col_win(ms_arr, "p", ms_arr_dict2) or
                                        diag_win(ms_arr, "p", ms_arr_dict2)):
                                    q.append((i, j))
                                    return q
                    else:
                        for i in range(n):  # go anywhere
                            for j in range(n):
                                ms_arr_dict2 = copy.deepcopy(ms_arr_dict)
                                if ms_arr_dict2[ms_arr[i][j]] == "empty":
                                    q.append((i, j))
                                    return q


# Select a random place for the player
def random_place(ms_arr, player, ms_arr_dict, mode, *args):
    if mode == "c":
        selection = possibilities(ms_arr, ms_arr_dict, mode, "p" if player == "player" else "c")
        current_loc = random.choice(selection)
    elif mode == "p":
        selection = possibilities(ms_arr, ms_arr_dict, mode, "p" if player == "player" else "c")
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
        selection = possibilities(ms_arr, ms_arr_dict, mode, "p" if player == "player" else "c", counter, p1)
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


# Checks whether the player has three
# of their marks in a horizontal row
def row_win(ms_arr, player, ms_arr_dict):
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
def col_win(ms_arr, player, ms_arr_dict):
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
def diag_win(ms_arr, player, ms_arr_dict):
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
def evaluate(ms_arr, ms_arr_dict, mode, *args):
    winner = 0
    if mode == "cp":
        p1 = args[0]
    for player in ["1", "2"]:
        if mode == "cp":
            if p1 == "p":
                if player == "1":
                    if (row_win(ms_arr, "p", ms_arr_dict) or col_win(ms_arr, "p", ms_arr_dict) or
                            diag_win(ms_arr, "p", ms_arr_dict)):
                        winner = int(player)
                        break
                else:
                    if (row_win(ms_arr, "c", ms_arr_dict) or col_win(ms_arr, "c", ms_arr_dict) or
                            diag_win(ms_arr, "c", ms_arr_dict)):
                        winner = int(player)
                        break
            else:
                if player == "1":
                    if (row_win(ms_arr, "c", ms_arr_dict) or col_win(ms_arr, "c", ms_arr_dict) or
                            diag_win(ms_arr, "c", ms_arr_dict)):
                        winner = int(player)
                        break
                else:
                    if (row_win(ms_arr, "p", ms_arr_dict) or col_win(ms_arr, "p", ms_arr_dict) or
                            diag_win(ms_arr, "p", ms_arr_dict)):
                        winner = int(player)
                        break

        else:
            if (row_win(ms_arr, player, ms_arr_dict) or col_win(ms_arr, player, ms_arr_dict)
                    or diag_win(ms_arr, player, ms_arr_dict)):
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


def drawboard(ms_arr_dict):
    i = 0
    for x in ms_arr_dict:
        if i == 3:
            i = 0
            print("\n_________")
        i += 1
        if ms_arr_dict[x] == "empty":
            print("_" + " ", end="  ")
        else:
            print(ms_arr_dict[x] + " ", end="  ")


# Main function to start the game
def play_game(mode):
    board_arr, tracker_dict = build_board()
    winner = 0
    counter = 1
    drawboard(tracker_dict)

    p1 = ""
    if mode == "cp":
        while 1:
            print("\nWho will play first?\t Computer(c) or Player(p) ")
            p1 = str(input().rsplit()[0])
            if p1 not in ("p", "c"):
                print("Invalid Player input. Enter again")
            else:
                break

    while winner == 0:
        for player in ["1", "2"]:
            if mode == "cp":
                if p1 == "p":
                    if player == "1":
                        board_arr, tracker_dict = random_place(board_arr, "player", tracker_dict, mode, counter, p1)
                        print("\nBoard after move number " + str(counter) + " (Player)")

                    else:
                        board_arr, tracker_dict = random_place(board_arr, "comp", tracker_dict, mode, counter, p1)
                        print("\nBoard after move number " + str(counter) + " (Computer)")

                elif p1 == "c":
                    if player == "1":
                        board_arr, tracker_dict = random_place(board_arr, "comp", tracker_dict, mode, counter, p1)
                        print("\nBoard after move number " + str(counter) + " (Computer)")
                    else:
                        board_arr, tracker_dict = random_place(board_arr, "player", tracker_dict, mode, counter, p1)
                        print("\nBoard after move number " + str(counter) + " (Player)")
                drawboard(tracker_dict)
                counter += 1
                winner = evaluate(board_arr, tracker_dict, mode, p1)
                if winner != 0:
                    break
            else:
                board_arr, tracker_dict = random_place(board_arr, player, tracker_dict, mode)
                print("\nBoard after move number " + str(counter))
                drawboard(tracker_dict)
                counter += 1
                winner = evaluate(board_arr, tracker_dict, mode)
                if winner != 0:
                    break

    return winner, p1


# Driver Code
for i in range(5):
    print("Which mode?\tComputer vs Player(cp) or Computer vs Computer (c) or Player vs Player(p)")
    mode = str(input())
    if mode != "c" and mode != "p" and mode != "cp":
        print("Incorrect mode input")
        break
    res, p1 = play_game(mode)
    if res == -1:
        print("\n\nMatch finished in a Tie.\n")
    elif mode == "cp":
        if p1 == "p":
            if res == 1:
                print("\n\nPlayer Wins\n")
            else:
                print("\n\nComputer Wins\n")
        else:
            if res == 1:
                print("\n\nComputer Wins\n")
            else:
                print("\n\nPlayer Wins\n")
    else:
        print("\n\nPlayer " + str(res) + " Wins\n")
