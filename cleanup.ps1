# Cleanup Script for Virtual Interview Navigator
# This script removes old files that are no longer needed after migration to React + Flask API structure

Write-Host "🧹 Starting cleanup of old files..." -ForegroundColor Cyan
Write-Host ""

# Confirm before proceeding
$confirmation = Read-Host "This will delete old files. Continue? (y/n)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "Cleanup cancelled." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Deleting old backend files..." -ForegroundColor Yellow

# Delete old backend files at root
$oldFiles = @(
    "app.py",
    "config.py",
    "extensions.py",
    "forms.py",
    "model.py",
    "requirements.txt"
)

foreach ($file in $oldFiles) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  ✓ Deleted $file" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Deleting old frontend files..." -ForegroundColor Yellow

# Delete old frontend folders
$oldFolders = @(
    "templates",
    "static",
    "migrations",
    "instance"
)

foreach ($folder in $oldFolders) {
    if (Test-Path $folder) {
        Remove-Item $folder -Recurse -Force
        Write-Host "  ✓ Deleted $folder/" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Deleting cache files..." -ForegroundColor Yellow

# Delete Python cache
if (Test-Path "__pycache__") {
    Remove-Item "__pycache__" -Recurse -Force
    Write-Host "  ✓ Deleted __pycache__/" -ForegroundColor Green
}

Write-Host ""
Write-Host "⚠️  Optional deletions:" -ForegroundColor Yellow
$deleteVenv = Read-Host "Delete old venv/ folder? (you'll create new one in backend/) (y/n)"
if ($deleteVenv -eq 'y' -or $deleteVenv -eq 'Y') {
    if (Test-Path "venv") {
        Remove-Item "venv" -Recurse -Force
        Write-Host "  ✓ Deleted venv/" -ForegroundColor Green
    }
}

$deleteUploads = Read-Host "Delete old uploads/ folder? (sample CVs already copied to backend/uploads/) (y/n)"
if ($deleteUploads -eq 'y' -or $deleteUploads -eq 'Y') {
    if (Test-Path "uploads") {
        Remove-Item "uploads" -Recurse -Force
        Write-Host "  ✓ Deleted uploads/" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Remaining structure:" -ForegroundColor Cyan
Write-Host "  ✅ backend/     - New Flask API" -ForegroundColor Green
Write-Host "  ✅ frontend/    - New React App" -ForegroundColor Green
Write-Host "  ✅ Documentation files" -ForegroundColor Green
Write-Host ""
Write-Host "You can now proceed with setup using the new structure!" -ForegroundColor Cyan

