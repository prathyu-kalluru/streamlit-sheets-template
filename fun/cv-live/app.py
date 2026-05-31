"""Fun app 2b: LIVE face tracking — the same idea, now on moving video.

The snapshot app (`../cv-face/app.py`) takes ONE photo and finds faces in it.
This one runs the *same* Haar cascade on **every frame of a live webcam stream**,
so the green box follows your face in real time.

How it works (and why it's more fragile than the snapshot version):

  - `streamlit-webrtc` opens a **WebRTC** video connection between the browser
    and this app. Each frame is sent up, we draw boxes on it in Python, and send
    it back — many times a second.
  - WebRTC has to find a network path between the two ends. On an open network a
    public **STUN** server is enough. On a locked-down classroom/office network,
    it may need a **TURN** relay — if so, add credentials in Secrets (see the
    `ice_servers()` helper and docs/05). Without that, the video may never start.

Still browser-only: nothing installs on the PC, the camera is just a browser
permission. If this won't connect on the room's network, fall back to the
snapshot app — it teaches the same thing and always works.
"""

import av
import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

st.set_page_config(page_title="Live face tracking", page_icon="🎥")
st.title("🎥 Live face tracking")
st.caption("The same OpenCV face detector as the snapshot app — now on live video.")


def ice_servers():
    """Network 'how do I reach the other side' config for WebRTC.

    Always offer a free public STUN server. If a TURN relay is configured in
    Secrets (needed on firewalled networks), add it too. The try/except means
    'no secrets set' is fine — we just run with STUN only.
    """
    servers = [{"urls": ["stun:stun.l.google.com:19302"]}]
    try:
        turn = st.secrets["turn"]   # optional; see docs/05 for the TOML shape
        servers.append({
            "urls": turn["urls"],
            "username": turn["username"],
            "credential": turn["credential"],
        })
    except Exception:
        pass
    return servers


class FaceTracker(VideoProcessorBase):
    """Runs once per video frame. Same detect-and-draw as the snapshot app."""

    def __init__(self):
        self.cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        # These get overwritten live from the sidebar sliders below.
        self.min_neighbors = 5
        self.blur = False

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")           # frame -> numbers (BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=self.min_neighbors, minSize=(40, 40)
        )
        for (x, y, w, h) in faces:
            if self.blur:
                roi = img[y:y + h, x:x + w]
                img[y:y + h, x:x + w] = cv2.GaussianBlur(roi, (45, 45), 30)
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        return av.VideoFrame.from_ndarray(img, format="bgr24")   # numbers -> frame


with st.sidebar:
    st.header("Tuning knobs")
    min_neighbors = st.slider("minNeighbors", 1, 10, 5, 1,
                              help="Higher = fewer false detections.")
    blur = st.checkbox("Blur faces instead of boxing them")

# Open the live stream. `recv` above is called for every frame.
ctx = webrtc_streamer(
    key="face-tracker",
    video_processor_factory=FaceTracker,
    rtc_configuration={"iceServers": ice_servers()},
    media_stream_constraints={"video": True, "audio": False},
)

# Push the slider/checkbox values into the running processor each rerun, so the
# knobs change the live video without restarting the stream.
if ctx.video_processor:
    ctx.video_processor.min_neighbors = min_neighbors
    ctx.video_processor.blur = blur

st.info(
    "Click **START** and allow the camera. If the video never connects, you're "
    "probably on a firewalled network that needs a TURN relay — use the snapshot "
    "app (`cv-face`) instead, or add TURN credentials in Secrets (see docs/05)."
)
