# Render Deployment Guide for SmartCities

## Quick Deploy

### Option 1: Blueprint (Automated Setup)
1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml` and set up everything

### Option 2: Manual Setup

#### Step 1: Create PostgreSQL Database
1. Go to Render Dashboard
2. Click "New" → "PostgreSQL"
3. Name: `smartcities-db`
4. Database: `smartcities`
5. User: `smartcities`
6. Click "Create Database"
7. **Copy the "Internal Database URL"** (starts with `postgresql://`)

#### Step 2: Create Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** `smartcities`
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn SmartCities.wsgi:application`
   - **Instance Type:** Free (or any paid tier)

#### Step 3: Set Environment Variables
In your web service settings, add these environment variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.10.0` |
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate a secure key (or let Render generate) |
| `DATABASE_URL` | Paste the Internal Database URL from Step 1 |

**To generate a SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Step 4: Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies from `requirements.txt`
   - Run migrations
   - Collect static files
   - Start your application

## After Deployment

### Create Superuser
1. Go to your web service in Render Dashboard
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```

### Access Your Site
Your site will be available at: `https://smartcities.onrender.com` (or your custom domain)

## Troubleshooting

### View Logs
- Go to your web service → "Logs" tab
- Check for any errors during deployment

### Common Issues

1. **Static files not loading:**
   - Make sure `build.sh` ran successfully
   - Check that `whitenoise` is installed

2. **Database connection errors:**
   - Verify `DATABASE_URL` is set correctly
   - Make sure you're using the **Internal Database URL** (not External)

3. **Module not found errors:**
   - Check `requirements.txt` includes all dependencies
   - Trigger a manual deploy

## Database Management

### Backup Database
```bash
# In Render shell
python manage.py dumpdata > backup.json
```

### Connect to PostgreSQL
Use the connection details from your database dashboard with any PostgreSQL client.

## Updating Your App

1. Push changes to GitHub
2. Render auto-deploys on every push to your main branch
3. Or manually deploy from Render dashboard

## Media Files

**Note:** Render doesn't have persistent storage on free tier. For media files:
- Use AWS S3, Cloudinary, or similar
- Consider upgrading to a paid tier with persistent disk

## Custom Domain

1. Go to your web service → "Settings"
2. Scroll to "Custom Domains"
3. Add your domain
4. Update DNS records as instructed

---

**Need help?** Check [Render's Django Deployment Guide](https://render.com/docs/deploy-django)
