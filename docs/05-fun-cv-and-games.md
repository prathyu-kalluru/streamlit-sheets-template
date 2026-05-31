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
| Face detection (snapshot) | `fun/cv-face/app.py` | OpenCV (already in `requirements.txt`) |
| Live face tracking | `fun/cv-live/app.py` | OpenCV + `streamlit-webrtc` + `av` |

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

## Live face tracking — `fun/cv-live/app.py`

The same Haar cascade, but run on **every frame of a live webcam stream** instead
of one snapshot, so the box follows your face in real time. It uses
`streamlit-webrtc`, which opens a **WebRTC** video connection between the browser
and the app.

**This one is more fragile than the snapshot app — by design, because of the
network.** WebRTC has to find a path between the browser and the Cloud container:

- On an **open network**, the free public **STUN** server (already configured) is
  enough, and it just works.
- On a **firewalled / locked-down network** (many classrooms and offices), STUN
  isn't enough and you need a **TURN** relay. Community Cloud doesn't give you
  one. If **START** spins forever and the video never appears, that's almost
  always this.

If you have TURN credentials (e.g. a free [Twilio](https://www.twilio.com/docs/stun-turn)
key), add them in the app's **Secrets** and the app picks them up automatically:

```toml
# .streamlit/secrets.toml  (paste into Advanced settings → Secrets on Cloud)
[turn]
urls = ["turn:your-turn-host:3478"]
username = "your-username"
credential = "your-credential"
```

**No TURN, locked-down network? Use the snapshot app (`cv-face`) instead.** It
teaches exactly the same computer-vision idea and works on any network, because
it's a plain image upload — no live connection to negotiate.

> Heads-up: `streamlit-webrtc` + `av` are heavy. Adding them to `requirements.txt`
> makes the **first build of every app** in this repo slower. That's the price of
> keeping one shared requirements file.

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
  (and, since `cv-live` was added, `streamlit-webrtc` + `av`), so cold builds
  take a few extra minutes. That's expected; watch **Manage app → Logs**.
- **Live app: START spins forever, no video** — WebRTC can't reach across the
  network. You're on a firewalled network with no TURN relay. Add TURN
  credentials in Secrets (above), or just use the snapshot app `cv-face`.
