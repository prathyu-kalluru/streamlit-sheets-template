# 05 · Fun extras — an OOP game and computer vision

Two browser-only apps that close the workshop on the fun stuff: a tic-tac-toe
game (your first real **object**) and a webcam **face detector** (a first taste
of computer vision). Same deploy flow as everything else — fork, point Streamlit
Cloud at the file, done. Nothing installs on your machine.

## Deploy them

Same steps as [`01-streamlit-cloud-deploy.md`](01-streamlit-cloud-deploy.md). The only new thing is the **main file path**:

| App | Main file path | New libraries |
|---|---|---|
| Tic-tac-toe | `fun/game-tictactoe/app.py` | none — pure Python + Streamlit |
| Face detection | `fun/cv-face/app.py` | OpenCV (already in `requirements.txt`) |

If you forked this template a while ago, click **Sync fork** on your fork's
GitHub page first, so the `fun/` folder appears in your copy.

## The game — `fun/game-tictactoe/app.py`

The whole point is the `Board` **class**: an object that bundles *state* (which
cells are filled, whose turn it is) with the *behaviour* that changes it
(`move`, `winner`, `reset`). You never touch the cells directly — you ask the
board. That's object-oriented programming in one screen.

The other lesson is one you've met before (session 4): every click reruns the
script top to bottom, so the board has to live in `st.session_state` to survive
between moves. The bot opponent (`bot_move`) is four plain rules — win, block,
centre, corner — no machine learning.

## Computer vision — `fun/cv-face/app.py`

Two ideas:

- **An image is just numbers.** OpenCV hands you the photo as a grid of numbers
  (a NumPy array, height × width × 3 colours). Drawing a box on a face is just
  changing some of those numbers.
- **A "model" is a file of learned patterns.** We load a *Haar cascade* — a
  pattern file that ships inside OpenCV — and ask it where the faces are. It
  answers with boxes: `(x, y, width, height)` per face.

The webcam is reached with `st.camera_input`, which simply asks the **browser**
for permission and hands back one snapshot. The detection runs in Streamlit
Cloud, not on the local PC — **nothing is installed on the machine you're using.**

The sidebar sliders (`scaleFactor`, `minNeighbors`) are live tuning knobs; the
**blur** checkbox flips detection from "highlight the face" to "hide the face" —
the same code, used for privacy instead.

## Common errors and fixes

- **`ModuleNotFoundError: No module named 'cv2'`** — `opencv-python-headless`
  isn't installed. Confirm it's in [`requirements.txt`](../requirements.txt) at
  the repo root (it is, by default). If you ever swap it for plain
  `opencv-python`, the build will fail — it must be the **`-headless`** build,
  because Streamlit Cloud has no GUI libraries.
- **Camera is blank or "permission denied"** — the browser blocked the webcam.
  Click the camera icon in the address bar, choose **Allow**, and reload. On a
  locked-down shared PC, an admin may have pre-blocked it — test before you rely
  on it in front of a class.
- **No faces detected** — Haar cascades are fussy about lighting and angle. Face
  the light, look straight at the camera, get a bit closer, and drag
  **minNeighbors** down in the sidebar before retaking.
- **First deploy is slow** — the first build of any app now installs OpenCV
  (~1–2 extra minutes). That's expected; watch **Manage app → Logs**.
