# GitHub Codespace Setup Guide

## Quick Start with Codespace

### Step 1: Open Codespace
1. Go to https://github.com/DWI671979/empire-of-continuum
2. Click the green **Code** button
3. Select **Codespaces** tab
4. Click **Create codespace on app-enhancements-and-coding**
5. Wait for the environment to initialize (2-3 minutes)

### Step 2: Install Dependencies
Once Codespace opens, run in the terminal:

```bash
cd Countinum
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will start on a local URL. Codespace will open a preview automatically.

---

## Environment Variables

Create a `.streamlit/secrets.toml` file in the Countinum directory:

```toml
# Database credentials (if using)
db_host = "your_db_host"
db_user = "your_db_user"
db_password = "your_db_password"
db_name = "empire_of_continuum"

# API keys (if needed)
api_key = "your_api_key"
```

---

## Project Structure

```
empire-of-continuum/
├── Countinum/
│   ├── app.py                 # Main Streamlit app
│   ├── requirements.txt       # Python dependencies
│   ├── pages/
│   │   ├── copyright.py       # Copyright management with OCR
│   │   ├── wiki.py            # Wiki encyclopedia system
│   │   ├── profile.py         # User profiles
│   │   ├── publish.py         # Publishing system
│   │   └── home.py            # Home/dashboard
│   ├── services/
│   │   ├── copyright_service.py
│   │   ├── wiki_service.py
│   │   ├── profile_service.py
│   │   └── story_service.py
│   ├── data/
│   │   ├── wiki_articles.json      # Sample wiki data
│   │   ├── user_profiles.json      # Sample profiles
│   │   ├── publications.json       # Sample publications
│   │   ├── featured.json
│   │   └── announcements.json
│   └── css/
│       └── manga_theme.css    # Epic fantasy styling
├── .devcontainer/
│   └── devcontainer.json      # Codespace configuration
└── ENHANCEMENTS.md            # Implementation details
```

---

## Features Included

### Design
- ✨ Epic fantasy theme with mystical colors (purples, golds, blues)
- 🎨 Smooth animations and gradient effects
- 📱 Responsive layout

### Functionality
- 📖 **Wiki System**: Browse, search, and create articles
- 👤 **Creator Profiles**: User profiles with statistics
- 🖋️ **Publishing**: Submit stories and content for moderation
- © **Copyright Management**: Track ownership claims
- 🔍 **OCR Tool**: Extract text from images (Tesseract.js, no OpenAI)

### Sample Data
- 10 wiki articles with lore
- 8 creator profiles with stats
- 10 publications

---

## Development Commands

### Run the App
```bash
cd Countinum
streamlit run app.py
```

### Run with specific port
```bash
streamlit run app.py --server.port 8501
```

### View logs
```bash
# In Codespace terminal, check Streamlit output
```

---

## Database Integration (Optional)

The app is ready to integrate with:
- PostgreSQL
- SQLite
- MySQL

Update the service files in `services/` with your database credentials.

---

## Deploying to Vercel

```bash
# Already deployed to:
# https://empire-of-countinum.vercel.app

# To redeploy after changes:
vercel deploy --prod
```

---

## Troubleshooting

### Port Already in Use
```bash
lsof -i :8501
kill -9 <PID>
streamlit run app.py
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Cache Issues
```bash
rm -rf ~/.streamlit/cache
streamlit run app.py --logger.level=debug
```

---

## Next Steps

1. **Customize Data**: Edit JSON files in `data/` directory
2. **Connect Database**: Update service files with real DB
3. **Add Authentication**: Implement user login in `pages/home.py`
4. **Extend Features**: Add new pages following existing patterns
5. **Deploy**: Use `vercel deploy --prod` for production

---

## Support

- Repository: https://github.com/DWI671979/empire-of-continuum
- Issues: https://github.com/DWI671979/empire-of-continuum/issues
- Discussions: https://github.com/DWI671979/empire-of-continuum/discussions

---

## Documentation Files

- **ENHANCEMENTS.md**: Detailed list of improvements made
- **IMPLEMENTATION_COMPLETE.md**: Completion status and metrics
- **README.md**: Main project documentation
- **CODESPACE_SETUP.md**: This file
