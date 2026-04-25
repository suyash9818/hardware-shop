# Deploy to Render (Free)

## Prerequisites
- GitHub account
- Your code pushed to GitHub

## Step 1: Prepare Your Code

```bash
# Make sure DEBUG is False in production
# Your settings.py already supports this via environment variable
```

## Step 2: Push to GitHub

```bash
# In your project folder
git init
git add .
git commit -m "Ready for deployment"

# Create a new repository on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/hardware-shop.git
git push -u origin main
```

## Step 3: Deploy on Render

1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click "New Web Service"
3. Select your GitHub repository
4. Configure:

| Setting | Value |
|---------|-------|
| Name | hardware-shop |
| Region | Oregon (or closest) |
| Branch | main |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn hardware_shop.wsgi:application` |

5. Click "Create Web Service"

## Step 4: Add Environment Variables

In Render dashboard, go to "Environment" tab and add:

```
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-secure-random-key-here
DJANGO_ALLOWED_HOSTS=your-app-name.onrender.com
DJANGO_MIGRATE_ON_STARTUP=1
```

## Step 5: Database (Free PostgreSQL)

1. In Render, click "New PostgreSQL"
2. Give it a name (e.g., hardware-db)
3. Copy the "Internal Database URL"
4. Add to your Web Service's Environment Variables:

```
DATABASE_URL=postgres://... (copy from PostgreSQL)
```

## Step 6: Run Migrations

Migrations run automatically on app startup when `DJANGO_MIGRATE_ON_STARTUP=1`.
You can also run them manually from the Render shell:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

---

## Troubleshooting

### Static Files Not Loading
Add to settings.py STATIC_ROOT:
```python
import os
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
```

### 500 Error
Check logs in Render dashboard - click "Logs" tab

### Database Connection Error
Make sure DATABASE_URL is set correctly in environment variables
