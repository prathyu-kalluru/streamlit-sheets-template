"""Fun app 1: tic-tac-toe — your first real object.

Everything you've built so far has been functions and a bit of pandas. Today we
meet the other big idea: an **object**. A `Board` below is one — it bundles some
*state* (which cells are filled) with the *behaviour* that acts on that state
(make a move, check for a winner). You don't poke at the cells directly; you ask
the board to do things. That's the whole idea of object-oriented programming.

The Streamlit twist: every click reruns this whole file top to bottom (same
lesson as session 4). So how does the board "remember" the game between clicks?
We park the object in `st.session_state` — the one place that survives a rerun.
"""

import random

import streamlit as st

st.set_page_config(page_title="Tic-tac-toe", page_icon="🎮")

# The eight ways to win: three indices in a row. Cells are numbered 0–8:
#   0 | 1 | 2
#   3 | 4 | 5
#   6 | 7 | 8
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


class Board:
    """The game, as an object: state + the behaviour that changes it.

    You (the human) are always "X". The bot is "O".
    """

    def __init__(self):
        self.cells = [""] * 9   # nine empty strings — this IS the game's memory
        self.turn = "X"         # whose move it is right now

    def move(self, i):
        """Place the current player's mark in cell `i`, then hand over the turn.

        Illegal moves (cell taken, or game already over) are quietly ignored —
        the object protects its own state so the UI can't corrupt it.
        """
        if self.cells[i] == "" and self.winner() is None:
            self.cells[i] = self.turn
            self.turn = "O" if self.turn == "X" else "X"

    def available(self):
        """The indices of every empty cell — the moves that are still legal."""
        return [i for i, c in enumerate(self.cells) if c == ""]

    def winner(self):
        """Return 'X', 'O', 'Draw', or None (game still going)."""
        for a, b, c in WIN_LINES:
            if self.cells[a] != "" and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        if "" not in self.cells:
            return "Draw"
        return None

    def reset(self):
        """Wipe the board back to a fresh game."""
        self.cells = [""] * 9
        self.turn = "X"


def bot_move(board):
    """A small, readable opponent — no machine learning, just four rules.

    Try each rule in order and play the first one that applies:
      1. If the bot can win this turn, take it.
      2. Else if the human could win next turn, block that cell.
      3. Else take the centre (the strongest square).
      4. Else take any free corner, otherwise any free cell at all.

    (Stretch idea for a curious student: replace this with the "minimax"
    algorithm and the bot becomes literally unbeatable. Out of scope today.)
    """
    me, you = "O", "X"

    # Rule 1 & 2: is there a line where placing a mark completes three-in-a-row?
    def winning_cell(mark):
        for i in board.available():
            board.cells[i] = mark          # pretend to play here...
            won = board.winner() == mark
            board.cells[i] = ""            # ...then undo the pretend move
            if won:
                return i
        return None

    spot = winning_cell(me) or winning_cell(you)   # win if you can, else block
    if spot is None and 4 in board.available():     # Rule 3: centre
        spot = 4
    if spot is None:                                # Rule 4: corner, then anything
        corners = [i for i in (0, 2, 6, 8) if i in board.available()]
        spot = random.choice(corners) if corners else random.choice(board.available())

    board.cells[spot] = me
    board.turn = "X"   # back to the human


# --- Streamlit UI -----------------------------------------------------------
# `st.session_state` is the only thing that survives a rerun, so the board (and
# the scoreboard) live there. Create them once, on the very first run.
if "board" not in st.session_state:
    st.session_state.board = Board()
if "score" not in st.session_state:
    st.session_state.score = {"You (X)": 0, "Bot (O)": 0, "Draws": 0}

board = st.session_state.board

st.title("🎮 Tic-tac-toe")
st.caption("You're ❌. The bot is ⭕. Click an empty square to move.")

# Status line: who won, or whose turn it is.
result = board.winner()
if result == "X":
    st.success("You win! 🎉")
elif result == "O":
    st.error("The bot wins. 🤖")
elif result == "Draw":
    st.info("It's a draw. 🤝")
else:
    st.write("**Your move.**")

# Draw the 3×3 grid as a grid of buttons (st.columns from session 5).
MARKS = {"X": "❌", "O": "⭕", "": " "}
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        i = row * 3 + col
        # A button per cell. Disable it once it's taken or the game is over.
        disabled = board.cells[i] != "" or result is not None
        if cols[col].button(MARKS[board.cells[i]], key=f"cell-{i}",
                            width="stretch", disabled=disabled):
            board.move(i)                       # your move
            if board.winner() is None:          # then the bot replies
                bot_move(board)
            st.rerun()                          # redraw with the new state

# When the game just ended, count it once into the scoreboard.
result = board.winner()
if result is not None and not st.session_state.get("counted", False):
    key = {"X": "You (X)", "O": "Bot (O)", "Draw": "Draws"}[result]
    st.session_state.score[key] += 1
    st.session_state.counted = True
if result is None:
    st.session_state.counted = False

# New game button + scoreboard.
if st.button("🔄 New game"):
    board.reset()
    st.session_state.counted = False
    st.rerun()

st.subheader("Scoreboard")
s = st.session_state.score
c1, c2, c3 = st.columns(3)
c1.metric("You (X)", s["You (X)"])
c2.metric("Bot (O)", s["Bot (O)"])
c3.metric("Draws", s["Draws"])
