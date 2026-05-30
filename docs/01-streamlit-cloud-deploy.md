# 01 · Deploy to Streamlit Community Cloud

You'll repeat this flow once per step. The only thing that changes between deployments is the **main file path** you point at.

## One-time setup

1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Sign in **with GitHub** — use the same account you forked this template into.
3. Authorize Streamlit Cloud to see your repos.

## Deploy an app

1. On the dashboard, click **Create app** → **Deploy a public app from GitHub**.
2. Fill in:
   - **Repository:** `<your-username>/streamlit-sheets-template`
   - **Branch:** `main`
   - **Main file path:** depends on the step:

     | Step | Main file path |
     |---|---|
     | 1 | `step1-mock/app.py` |
     | 2 | `step2-read-public-sheet/app.py` |
     | 3 — collector | `step3-write-admin-gated/collect/app.py` |
     | 3 — admin | `step3-write-admin-gated/admin/app.py` |
     | Fun — game | `fun/game-tictactoe/app.py` |
     | Fun — face detection (snapshot) | `fun/cv-face/app.py` |
     | Fun — live face tracking | `fun/cv-live/app.py` |

   - **App URL:** pick something like `my-feedback-step1` (must be unique across all of Streamlit Cloud).
3. **(Step 3 only)** Click **Advanced settings** → paste your TOML into the **Secrets** field. See [`03-service-account-setup.md`](03-service-account-setup.md) for what to paste.
4. Click **Deploy**.

The first deploy takes 1–3 minutes (Streamlit installs the libraries from `requirements.txt`). After that, every commit to `main` redeploys in seconds.

## Re-deploy after editing

You don't need to manually re-deploy. As long as the app exists in Streamlit Cloud, every push to `main` of your fork auto-redeploys. Watch the build logs from the app's **Manage app** panel if anything goes wrong.

## One repo, multiple apps

You'll end up with up to four Streamlit Cloud apps all pointing at the same fork — one per step (and two for step 3). That's normal and intentional. Each gets its own URL.

## Common errors and fixes

- **`ModuleNotFoundError`** — check that the library is listed in [`requirements.txt`](../requirements.txt) at the repo root.
- **App stuck on "Your app is in the oven"** — usually a build error. Open **Manage app → Logs**.
- **Step 3 says `KeyError: 'gcp_service_account'`** — secrets aren't pasted yet. Open **App settings → Secrets** and paste the TOML.
- **Step 2 says "Paste a Google Sheet URL" or won't load** — paste a public sheet link into the **Google Sheet URL** box at the top of the app. The sheet must be published-to-web or shared "Anyone with the link". See [`02-publish-sheet-to-web.md`](02-publish-sheet-to-web.md).
