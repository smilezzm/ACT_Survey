# Deployment Guide for ACT Survey App

## Option 1: Deploy to Heroku (Recommended for beginners)

### Prerequisites:
1. Create a free account at https://heroku.com
2. Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
3. Install Git if not already installed

### Steps:

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku app**:
   ```bash
   heroku create your-survey-app-name
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-random-secret-key-here
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

6. **Your app will be available at**: `https://your-survey-app-name.herokuapp.com`

---

## Option 2: Deploy to Railway (Detailed Step-by-Step)

Railway is one of the easiest platforms to deploy your Flask app and get a public URL.

### Prerequisites:
1. A GitHub account
2. Your code uploaded to a GitHub repository

### Step 1: Prepare Your Code for Railway

First, make sure your project has all necessary files:
- `app.py` (your Flask app)
- `requirements.txt` (Python dependencies)
- `runtime.txt` (Python version)
- `Procfile` (tells Railway how to start your app)
- `templates/` folder with HTML files

**Create a Procfile** (if you don't have one):
Create a file named `Procfile` (no extension) in your project root with this content:
```
web: python app.py
```

This tells Railway to start your app by running `python app.py`.

### Step 2: Upload to GitHub

1. **Create a GitHub repository**:
   - Go to https://github.com
   - Click "New repository"
   - Name it something like "act-survey-app"
   - Make it public (easier for deployment)

2. **Upload your files**:
   - Either use GitHub's web interface to upload files
   - Or use Git commands:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/yourusername/act-survey-app.git
     git push -u origin main
     ```

### Step 3: Deploy to Railway

1. **Go to Railway**:
   - Visit https://railway.app
   - Click "Login" and choose "Login with GitHub"
   - Authorize Railway to access your GitHub account

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your survey repository from the list

3. **Railway Auto-Detection**:
   - Railway will automatically detect it's a Python/Flask app
   - It will read your `requirements.txt` and `runtime.txt`
   - The build process will start automatically

4. **Set Environment Variables**:
   - Click on your project in Railway dashboard
   - Go to "Variables" tab
   - Add a new variable:
     - Name: `SECRET_KEY`
     - Value: `your-random-secret-key-here` (generate a secure key)
   - Add another variable:
     - Name: `PORT`
     - Value: `5000`

5. **Deploy and Get URL**:
   - Railway will build and deploy your app
   - Once deployed, click "Settings" → "Domains"
   - Click "Generate Domain"
   - Your app will be available at: `https://your-app-name.up.railway.app`

### Step 4: Test Your Deployment

1. **Visit your URL**: `https://your-app-name.up.railway.app`
2. **Test the survey**: Fill out a test survey to ensure it works
3. **Check admin panel**: Visit `https://your-app-name.up.railway.app/admin`
4. **Verify data saving**: Make sure responses are being saved

### Step 5: Share Your Survey

Once deployed, you can share these URLs:
- **Main survey**: `https://your-app-name.up.railway.app/`
- **Admin dashboard**: `https://your-app-name.up.railway.app/admin`
- **API stats**: `https://your-app-name.up.railway.app/api/stats`

### Troubleshooting Railway Deployment:

**If the app won't start:**
1. Check the build logs in Railway dashboard
2. Ensure `requirements.txt` has all dependencies
3. Verify your `app.py` runs locally first
4. **Make sure you have a `Procfile`** with content: `web: python app.py`
5. Check that your app listens on the correct port (should use `PORT` environment variable)

**If you get numpy/pandas compatibility errors:**
```
ValueError: numpy.dtype size changed, may indicate binary incompatibility
```
This happens when pandas and numpy versions are incompatible. Make sure your `requirements.txt` has:
```
pandas==1.5.3
numpy==1.24.3
openpyxl==3.1.2
```

**If you get database errors:**
1. Railway will create a new SQLite database automatically
2. The database will be persistent across deployments
3. Check Railway logs for specific error messages

**If you need to update your app:**
1. Push changes to your GitHub repository
2. Railway will automatically redeploy
3. No need to manually trigger deployment

### Railway Advantages:
- **Free tier**: 512MB RAM, 1GB disk space
- **Automatic deployments**: Updates when you push to GitHub
- **Easy setup**: No complex configuration needed
- **Built-in monitoring**: View logs and metrics
- **Custom domains**: Can add your own domain later

---

## Option 3: Deploy to Render

### Steps:

1. Go to https://render.com
2. Sign up and connect your GitHub account
3. Click "New" → "Web Service"
4. Connect your repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
6. Set environment variable: `SECRET_KEY=your-random-secret-key`

---

## Important Notes:

### Database Considerations:
- SQLite works for small surveys but has limitations in production
- For heavy usage, consider upgrading to PostgreSQL
- The current setup will work fine for classroom/small group surveys

### Security:
- Generate a strong SECRET_KEY for production
- Consider adding CSRF protection for forms
- Add rate limiting if expecting high traffic

### Monitoring:
- Check your app logs regularly: `heroku logs --tail` (for Heroku)
- Monitor response times and errors
- Set up alerts for downtime

### Data Backup:
- Regularly backup your database
- Consider setting up automated exports


- **Download database regularly**: Use the methods above to download your `.db` file
- **Excel exports**: Use `get_data.py` for easy-to-analyze Excel files
- **SQL dumps**: Create SQL backup files for complete data restoration

## Testing Your Deployment:

1. Visit your deployed URL
2. Fill out a test survey
3. Check the admin panel: `your-url.com/admin`
4. Verify data is being saved properly

## Sharing Your Survey:

Once deployed, you can share the URL with:
- Students in your class
- Research participants
- Survey respondents

The data will be automatically collected in the `survey_data.db` database.

## After Deployment - Managing Your Survey

### Your Survey URLs:
Once deployed on Railway, your survey will have these URLs:

1. **Main Survey Page**: `https://your-app-name.up.railway.app/`
   - This is the URL you share with participants
   - Shows the 5 ACT (Asthma Control Test) questions
   - Collects name, age, gender, phone, and question responses

2. **Admin Dashboard**: `https://your-app-name.up.railway.app/admin`
   - View all survey responses
   - See submission dates and scores
   - Download data for analysis

3. **API Statistics**: `https://your-app-name.up.railway.app/api/stats`
   - JSON data with total responses and average scores
   - Useful for integrating with other tools

### Collecting Data:

**For Research/Academic Use:**
- Share the main survey URL with participants
- Data is automatically saved to SQLite database
- Access admin panel to view and analyze responses

**For Classroom/Educational Use:**
- Students can access the survey via the public URL
- Teacher can monitor responses in real-time via admin panel
- Export data using the included `get_data.py` script

### Data Management:

**Viewing Responses:**
- Go to `/admin` to see all responses in a table format
- Responses are sorted by submission date (newest first)
- Each response shows: ID, name, age, gender, phone, individual question scores, total score, and timestamp

**Exporting Data:**
- Use the `get_data.py` script to export to Excel format
- Run: `python get_data.py` (generates `responses_export.xlsx`)
- Data includes all survey responses with calculated scores

**Downloading the Database File (.db) Locally:**

Railway doesn't provide direct file download access, but you can download your data in several ways:

1. **Method 1: Using Railway CLI (Recommended)**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Connect to your project
   railway link
   
   # Download the database file
   railway run python -c "
   import sqlite3
   import shutil
   shutil.copy('survey_data.db', 'downloaded_survey_data.db')
   print('Database copied successfully!')
   "
   ```

2. **Method 2: Add a Download Route to Your App**
   Add this route to your `app.py`:
   ```python
   from flask import send_file
   
   @app.route('/download-db')
   def download_db():
       return send_file('survey_data.db', 
                       as_attachment=True, 
                       download_name='survey_responses.db')
   ```
   Then visit: `https://your-app-name.up.railway.app/download-db`

3. **Method 3: Export via Custom Script**
   Create a backup script in your app that generates a downloadable backup:
   ```python
   @app.route('/backup')
   def backup_data():
       # Create SQL dump
       conn = sqlite3.connect('survey_data.db')
       with open('backup.sql', 'w') as f:
           for line in conn.iterdump():
               f.write('%s\n' % line)
       conn.close()
       return send_file('backup.sql', as_attachment=True)
   ```

**Understanding Scores:**
- Each question scored 1-5 (1 = worst control, 5 = best control)
- Total score range: 5-25
- Higher scores indicate better asthma control
- Score interpretation:
  - 20-25: Good control
  - 15-19: Moderate control  
  - 5-14: Poor control

### Security and Privacy:

**Data Protection:**
- All data is stored securely on Railway's servers
- HTTPS encryption for all communications
- No data is shared with third parties

**Access Control:**
- **IMPORTANT**: Admin panel currently has NO authentication 
- Anyone who knows the URL `/admin` can view all survey responses
- This is suitable ONLY for small, private surveys or classroom use

**How to Secure the Admin Panel:**

1. **Method 1: Add Simple Password Protection**
   Add this to your `app.py` before the admin route:
   ```python
   from functools import wraps
   
   def require_auth(f):
       @wraps(f)
       def decorated(*args, **kwargs):
           auth = request.authorization
           if not auth or not (auth.username == 'admin' and auth.password == 'your-secure-password'):
               return ('Authentication required', 401, {
                   'WWW-Authenticate': 'Basic realm="Admin Access"'})
           return f(*args, **kwargs)
       return decorated
   
   @app.route('/admin')
   @require_auth
   def admin_dashboard():
       # ...existing admin code...
   ```

2. **Method 2: Use Environment Variables for Credentials**
   ```python
   # In your app.py
   ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
   ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'changeme')
   
   def require_auth(f):
       @wraps(f)
       def decorated(*args, **kwargs):
           auth = request.authorization
           if not auth or not (auth.username == ADMIN_USERNAME and auth.password == ADMIN_PASSWORD):
               return ('Authentication required', 401, {
                   'WWW-Authenticate': 'Basic realm="Admin Access"'})
           return f(*args, **kwargs)
       return decorated
   ```
   
   Then set these in Railway:
   - `ADMIN_USERNAME`: your-admin-username
   - `ADMIN_PASSWORD`: your-secure-password

3. **Method 3: Hide Admin URL**
   Change the admin route to something secret:
   ```python
   @app.route('/secret-admin-panel-xyz123')  # Use your own secret path
   def admin_dashboard():
       # ...existing admin code...
   ```

4. **Method 4: IP Restriction (Advanced)**
   ```python
   from flask import request
   
   ALLOWED_IPS = ['YOUR.IP.ADDRESS.HERE']  # Your IP address
   
   @app.route('/admin')
   def admin_dashboard():
       if request.remote_addr not in ALLOWED_IPS:
           return "Access denied", 403
       # ...existing admin code...
   ```

**Recommended Security Setup:**
- Use Method 2 (environment variables) for username/password
- Also use Method 3 (secret URL) for extra security
- For sensitive data, consider adding login protection
- Survey responses are anonymous unless participants provide identifying information

### Monitoring Your Survey:

**Check Performance:**
- Railway dashboard shows app performance metrics
- Monitor response times and error rates
- View deployment logs for troubleshooting

**Usage Analytics:**
- Use `/api/stats` endpoint to get basic statistics
- Track total responses and average scores
- Monitor submission patterns over time
