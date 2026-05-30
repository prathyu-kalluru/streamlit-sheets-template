"""Fun app 2: how a computer 'sees' — face detection in the browser.

Two ideas hide in this tiny app:

  1. **An image is just numbers.** When you take a photo, OpenCV hands you a big
     grid of numbers (a NumPy array): height × width × 3 colour channels. Drawing
     a box on a face is just changing some of those numbers.

  2. **A 'model' is a file of learned patterns.** We don't write rules for what a
     face looks like. We load a *Haar cascade* — a pattern file that ships inside
     OpenCV, trained long ago on thousands of faces — and ask it: where are the
     faces? It answers with boxes: (x, y, width, height) for each one.

Nothing installs on the shared PC. `st.camera_input` just asks the **browser**
for permission to use the webcam and hands us one snapshot. The detection runs
up in Streamlit Cloud, not on your machine.
"""

import cv2
import numpy as np
import streamlit as st

st.set_page_config(page_title="Face detection", page_icon="📷")
st.title("📷 How a computer sees: face detection")
st.caption("Take a photo. We find faces and draw on the pixels. All in the browser.")

# Load the pattern file once. cv2.data.haarcascades is a folder bundled inside
# OpenCV, so there's no model to download or commit — it's already there.
CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Two tuning knobs — drag them and re-take the photo to feel what they do.
with st.sidebar:
    st.header("Tuning knobs")
    scale_factor = st.slider(
        "scaleFactor", 1.05, 1.5, 1.1, 0.05,
        help="How much the detector zooms out each pass. Smaller = more thorough but slower.",
    )
    min_neighbors = st.slider(
        "minNeighbors", 1, 10, 5, 1,
        help="How many overlapping hits to trust a face. Higher = fewer false alarms.",
    )
    blur_faces = st.checkbox(
        "Blur faces instead of boxing them",
        help="The same detection, used to protect privacy rather than highlight it.",
    )

# Ask the browser for a webcam snapshot. Returns None until a photo is taken.
photo = st.camera_input("Take a photo")

if photo is not None:
    # Decode the uploaded photo into an image (a NumPy array of numbers).
    # OpenCV uses BGR channel order, not RGB — we'll fix that before display.
    buffer = np.frombuffer(photo.getvalue(), np.uint8)
    bgr = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

    # Detection works on a grey version — colour doesn't help find a face shape.
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    faces = CASCADE.detectMultiScale(
        gray, scaleFactor=scale_factor, minNeighbors=min_neighbors,
        minSize=(40, 40),
    )

    # Each face is a box (x, y, w, h). Either blur it or draw a green rectangle.
    for (x, y, w, h) in faces:
        if blur_faces:
            roi = bgr[y:y + h, x:x + w]                  # the rectangle of pixels...
            bgr[y:y + h, x:x + w] = cv2.GaussianBlur(roi, (45, 45), 30)  # ...blurred
        else:
            cv2.rectangle(bgr, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Flip BGR back to RGB so the colours look right in the browser, then show it.
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    st.image(rgb, caption="Detected", width="stretch")
    st.metric("Faces detected", len(faces))

    if len(faces) == 0:
        st.info(
            "No faces found. Try better lighting, face the camera straight on, "
            "or drag **minNeighbors** down in the sidebar and retake."
        )
else:
    st.info("👆 Allow the camera when the browser asks, then take a photo.")
