# Deployment Guide for TrackName

This project is a Flask application that uses the Genius API. To make it accessible online, the easiest way is to use a Platform as a Service (PaaS) like **Railway.app** or **Render.com**.

## 🚀 Step-by-Step Deployment

### 1. Push your code to GitHub
The hosting platforms connect directly to your GitHub repository.
- Create a repository on GitHub.
- Push your local code to that repository.

### 2. Deploy to Railway.app (Recommended) or Render.com
**For Railway:**
1. Log in to [Railway.app](https://railway.app/).
2. Click **"New Project"** $\rightarrow$ **"Deploy from GitHub repo"**.
3. Select your `TrackName` repository.

**For Render:**
1. Log in to [Render.com](https://render.com/).
2. Click **"New"** $\rightarrow$ **"Web Service"**.
3. Connect your GitHub account and select the `TrackName` repository.
4. Select **"Python"** as the runtime and ensure the start command is `gunicorn app:app`.

### 3. Set Environment Variables
The app will not start without your Genius API token.
1. In your project dashboard (Railway or Render), find the **"Variables"** or **"Env Vars"** section.
2. Add a new variable:
   - **Key:** `GENIUS_ACCESS_TOKEN`
   - **Value:** `your_actual_token_here`
3. Save the changes. The app will automatically restart and deploy.

## ⚠️ Important Note on Data Persistence
The current version of TrackName saves search history and favorites to a local JSON file in the home directory (`~/.trackname`). 

**On hosted platforms (Railway, Render, Heroku), the filesystem is ephemeral.** This means:
- Whenever you deploy a new version or the server restarts, **your history and favorites will be deleted**.
- If you need persistent storage, you would need to migrate the `storage.py` logic to use a database (like PostgreSQL or MongoDB) or a persistent volume (available on some paid plans).

## 🛠 Local Testing
If you want to test the "production" setup locally before deploying:
1. Install gunicorn: `pip install gunicorn`
2. Run the app: `gunicorn app:app`
3. Visit `http://127.0.0.1:8000`
