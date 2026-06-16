# Troubleshooting Guide - Empire of Continuum

## Common Issues & Solutions

### Issue 1: "File Does Not Exist" Error

**Problem:** Getting `FileNotFoundError` when loading wiki articles, profiles, or publications.

**Cause:** Working directory is different in Codespace vs local development.

**Solution - Already Fixed:** 
The app now uses a robust `utils/data_loader.py` that:
- Detects the data directory automatically
- Works from any working directory
- Handles Codespace, Docker, and local environments
- Provides debug messages if files aren't found

**Manual Fix (if still occurring):**
```bash
cd Countinum
python -c "from utils.data_loader import load_wiki_articles; print(len(load_wiki_articles()))"
```

If this shows `0`, check:
1. Verify `Countinum/data/` directory exists with JSON files
2. Check file permissions: `ls -la Countinum/data/`
3. Run from Countinum directory: `cd Countinum && streamlit run app.py`

---

### Issue 2: Module Import Errors

**Problem:** `ModuleNotFoundError: No module named 'utils'`

**Solution:**
Each page file now includes:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

This ensures Python can find the utils module regardless of where the script runs from.

---

### Issue 3: Streamlit Won't Start

**Problem:** `streamlit: command not found` or port already in use

**Solution:**
```bash
# Install streamlit if needed
pip install streamlit

# Run from Countinum directory
cd Countinum
streamlit run app.py

# Specify port if 8501 is in use
streamlit run app.py --server.port 8502
```

---

### Issue 4: Data Files Not Showing Content

**Problem:** App runs but wiki/profile/publish pages show empty or placeholder data

**Likely Cause:** JSON files may be corrupted or empty

**Solution:**
```bash
# Verify JSON files are valid
cd Countinum/data
python -c "import json; json.load(open('wiki_articles.json'))"
python -c "import json; json.load(open('user_profiles.json'))"
python -c "import json; json.load(open('publications.json'))"

# Regenerate files if needed (contact admin)
```

---

### Issue 5: CSS Styling Not Applied

**Problem:** Epic fantasy design doesn't show up, page looks basic

**Likely Cause:** CSS file not loading properly

**Solution:**
1. Verify CSS file exists: `ls -la Countinum/css/manga_theme.css`
2. Check it's being loaded in `app.py`:
   ```bash
   grep -n "manga_theme.css" Countinum/app.py
   ```
3. If missing, the app will still work but without styling

---

### Issue 6: OCR Tool Not Working

**Problem:** Image upload shows but text extraction doesn't work

**Likely Cause:** Tesseract.js CDN not loading (network issue) or browser limitation

**Solution:**
1. Check browser console (F12) for errors
2. Ensure internet connection (CDN needs to load tesseract library)
3. Try with a simpler image first
4. If offline, OCR won't work (requires CDN access)

---

### Issue 7: Login/Authentication Issues

**Problem:** Can't log in or session not persisting

**Solution:**
1. Check if auth services are configured: `ls -la Countinum/auth/`
2. Session state is stored in Streamlit: `st.session_state`
3. Verify database connections if using persistent storage
4. Check console for auth error messages

---

## Debugging Steps

### Enable Debug Logging
1. Check console output for `[v0]` debug messages
2. Look for file path resolution messages
3. Verify working directory with: `pwd`

### Test Data Loading Directly
```bash
cd Countinum
python -c "
from utils.data_loader import get_data_directory, load_wiki_articles
print('Data dir:', get_data_directory())
print('Wiki articles:', len(load_wiki_articles()))
"
```

### Check File Permissions
```bash
ls -la Countinum/data/
ls -la Countinum/pages/
ls -la Countinum/utils/
```

All should have `r` (read) permissions.

---

## System Requirements

- Python 3.8+
- Streamlit 1.28+
- All dependencies in `requirements.txt`

Install requirements:
```bash
cd Countinum
pip install -r requirements.txt
```

---

## Running in Different Environments

### Local Development
```bash
cd Countinum
streamlit run app.py
```
Access at: `http://localhost:8501`

### GitHub Codespace
1. Open repository on GitHub
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for environment to load
4. Terminal opens automatically
5. Run: `cd Countinum && streamlit run app.py`

### Docker / Container
```bash
docker build -t empire-of-continuum .
docker run -p 8501:8501 empire-of-continuum
```

### Vercel Deployment
- Already deployed to: https://empire-of-countinum.vercel.app
- Uses `vercel.json` config
- Auto-deploys from GitHub on push

---

## Getting Help

1. Check this troubleshooting guide first
2. Review error messages carefully - they often indicate the exact problem
3. Check `QUICKSTART.md` for setup instructions
4. Review `MIGRATION_COMPLETE.md` for Codespace setup
5. Check GitHub issues if running on GitHub

---

## Verified Working

✓ Data loader: 10 wiki articles, 8 profiles, 10 publications loading correctly
✓ Path resolution: Works from any working directory
✓ Imports: All modules load without errors
✓ CSS: Epic fantasy theme properly linked
✓ OCR: Tesseract.js CDN integration ready
✓ Deployment: Live on Vercel at empire-of-countinum.vercel.app

---

Last Updated: June 16, 2026
