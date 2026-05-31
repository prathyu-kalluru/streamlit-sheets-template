# streamlit-sheets-template

A browser-only template for building a small web app with **Streamlit** and a **Google Sheet** as the backing store. Designed for learners who know a little Python and `pandas` but have never installed Python locally, used git/GitHub, or deployed a web app.

You build the app in **three progressive steps**. Each step deploys to **Streamlit Community Cloud** as its own URL. No local Python install, no `pip`, no terminal — you edit code in your browser (on github.com or via [github.dev](https://github.dev)) and every commit auto-redeploys.

## The three steps

| Step | Folder | What you learn |
|------|--------|----------------|
| 1 | [`step1-mock/`](step1-mock/) | Streamlit basics: widgets, forms, `st.dataframe`, your first `st.bar_chart`. Data is hardcoded — no external service. |
| 2 | [`step2-read-public-sheet/`](step2-read-public-sheet/) | Read a public Google Sheet as CSV with `pandas.read_csv`. Build a dashboard: KPIs (`st.metric`), bar chart, line chart, filters. |
| 3 | [`step3-write-admin-gated/`](step3-write-admin-gated/) | **Optional / self-study.** Two apps. A public collector writes to a private sheet via a service account; a password-gated admin app views, edits, and visualises the data. The heaviest step — service-account plumbing. Do it on your own time if you want it. |

Each step folder is **self-contained** — you can deploy step 1, then come back later and deploy steps 2 and 3 without touching the earlier apps.

## Fun extras

Two browser-only apps for the last session — pure fun, but each teaches a real idea:

| Folder | What you learn |
|------|--------|
| [`fun/game-tictactoe/`](fun/game-tictactoe/) | Object-oriented programming: a `Board` **class** bundling state + behaviour, kept alive across reruns in `st.session_state`. |
| [`fun/cv-face/`](fun/cv-face/) | Computer vision: a webcam snapshot via `st.camera_input`, face detection with OpenCV. An image is just numbers; a model is a file of learned patterns. |
| [`fun/cv-live/`](fun/cv-live/) | The same detector on **live video** via `streamlit-webrtc`. The wow finale — but needs an open network (or a TURN relay); falls back to `cv-face` if the room's wifi blocks WebRTC. |

See [`docs/05-fun-cv-and-games.md`](docs/05-fun-cv-and-games.md). The webcam is just a browser permission — nothing installs on the PC you're using.

## Where to start

1. **Fork this repo** — click **Fork** at the top right. Your fork is the copy Streamlit Cloud will deploy from.
2. Skim [`docs/00-git-github-basics.md`](docs/00-git-github-basics.md) for the absolute minimum git/GitHub vocabulary.
3. Follow [`docs/01-streamlit-cloud-deploy.md`](docs/01-streamlit-cloud-deploy.md) to deploy `step1-mock/app.py`.
4. Move on to steps 2 and 3 as you're ready.

## Docs

- [`docs/00-git-github-basics.md`](docs/00-git-github-basics.md) — git, GitHub, forks, browser editing
- [`docs/01-streamlit-cloud-deploy.md`](docs/01-streamlit-cloud-deploy.md) — deploy any step to Streamlit Community Cloud
- [`docs/02-publish-sheet-to-web.md`](docs/02-publish-sheet-to-web.md) — make a Google Sheet readable as CSV (step 2)
- [`docs/03-service-account-setup.md`](docs/03-service-account-setup.md) — create a service account so step 3 can read/write a private sheet
- [`docs/04-adapt-to-your-niche.md`](docs/04-adapt-to-your-niche.md) — change the schema and ship your own version
- [`docs/05-fun-cv-and-games.md`](docs/05-fun-cv-and-games.md) — the fun extras: an OOP game and webcam face detection

## What you need

- A **GitHub account** (free)
- A **Google account** (free)
- A **Streamlit Community Cloud account** (free, sign in with GitHub at [share.streamlit.io](https://share.streamlit.io))

Nothing installs on your machine.

## What's in the box

```
.
├── README.md                            # you are here
├── requirements.txt                     # Python libraries Streamlit Cloud installs for you
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example             # the shape of secrets you paste into Streamlit Cloud (step 3)
├── step1-mock/
│   └── app.py
├── step2-read-public-sheet/
│   └── app.py
├── step3-write-admin-gated/
│   ├── collect/app.py
│   └── admin/app.py
├── fun/                                 # last-session extras (session 6)
│   ├── game-tictactoe/app.py            # OOP: a Board class
│   ├── cv-face/app.py                   # computer vision: webcam snapshot
│   └── cv-live/app.py                   # computer vision: live WebRTC tracking
└── docs/
    ├── 00-git-github-basics.md
    ├── 01-streamlit-cloud-deploy.md
    ├── 02-publish-sheet-to-web.md
    ├── 03-service-account-setup.md
    ├── 04-adapt-to-your-niche.md
    └── 05-fun-cv-and-games.md
```
