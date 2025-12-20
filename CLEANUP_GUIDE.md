# Cleanup Guide - Removing Old Files

## 🗑️ Files to Delete (No Longer Needed)

These old files have been replaced by the new structure in `backend/` and `frontend/`:

### Old Backend Files (Root Level)
- ✅ `app.py` (old Flask app with templates)
- ✅ `config.py` (old config)
- ✅ `extensions.py` (old extensions)
- ✅ `forms.py` (not needed - no forms in API)
- ✅ `model.py` (old models - now in backend/)
- ✅ `requirements.txt` (old - use backend/requirements.txt)

### Old Frontend Files
- ✅ `templates/` folder (old HTML templates)
- ✅ `static/` folder (old CSS/JS files)

### Old Database Files
- ✅ `migrations/` folder (duplicate - we have it in backend/migrations/)
- ✅ `instance/` folder (old Flask instance)

### Cache Files
- ✅ `__pycache__/` folders (Python cache - can regenerate)

### Virtual Environment (Optional)
- ⚠️ `venv/` folder (optional - you can delete if you want to create fresh one in backend/)

---

## 📁 Files to KEEP

### New Structure
- ✅ `backend/` folder - NEW Flask API
- ✅ `frontend/` folder - NEW React app

### Documentation
- ✅ `README.md`
- ✅ `SETUP_GUIDE.md`
- ✅ `DEPLOYMENT_GUIDE.md`
- ✅ `QUICK_START.md`
- ✅ `CLEANUP_GUIDE.md` (this file)

### Optional/Useful
- ⚠️ `uploads/` folder - Has sample CVs (abhi.pdf, sample_cv.pdf)
  - You can move these to `backend/uploads/` for testing
  - Or delete if you don't need them
- ⚠️ `backup.sql` - Database backup (keep if useful)
- ⚠️ `venv/` - Old virtual environment (safe to delete, you'll create new one in backend/)

---

## 🚀 Quick Cleanup Script

I'll create a cleanup script for you to run, or you can manually delete these files.

**Before deleting, make sure:**
1. ✅ You've tested the new backend and frontend work
2. ✅ Any important data is backed up
3. ✅ You've moved sample CVs if you want to keep them

---

## 📝 Manual Cleanup Steps

### Step 1: Move Sample CVs (Optional)
If you want to keep the sample CVs for testing:

```powershell
# Copy sample CVs to new uploads folder
Copy-Item "uploads\*.pdf" "backend\uploads\"
```

### Step 2: Delete Old Files
You can manually delete these files/folders, or use the cleanup script I'll create.

---

## ✅ After Cleanup

Your project structure should look like:
```
InterviewPrac/
├── backend/          ✅ NEW - Flask API
├── frontend/         ✅ NEW - React App
├── uploads/          ⚠️  Old (optional - delete or keep sample CVs)
├── README.md         ✅ Keep
├── SETUP_GUIDE.md    ✅ Keep
├── DEPLOYMENT_GUIDE.md ✅ Keep
├── QUICK_START.md    ✅ Keep
└── backup.sql        ⚠️  Optional - keep if useful
```

---

**Ready to clean up? I can create a cleanup script or you can manually delete the files listed above.**

