# setup-and-commit-tms.ps1
Write-Host "?? Setting up UAP-TMS with proper git commits..." -ForegroundColor Cyan

# Step 1: Ensure all directories exist
$apps = @("transportation", "custom_admin")
foreach ($app in $apps) {
    if (!(Test-Path $app)) {
        python manage.py startapp $app
        Write-Host "? Created $app app" -ForegroundColor Green
    }
}

# Step 2: Create templates directory
if (!(Test-Path "templates")) {
    New-Item -ItemType Directory -Path "templates" | Out-Null
    New-Item -ItemType Directory -Path "templates\transportation" | Out-Null
    New-Item -ItemType Directory -Path "templates\custom_admin" | Out-Null
    Write-Host "? Created templates directories" -ForegroundColor Green
}

Write-Host "`n?? Setting up database..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

Write-Host "`n?? Committing all changes to git..." -ForegroundColor Green
git add .
git commit -m "Complete UAP-TMS setup with:
- User authentication system (login/signup)
- Bus registration functionality
- Live tracking feature
- Payment system
- Admin panel via views
- All templates and views
- Database models"

Write-Host "`n?? UAP-TMS successfully set up and committed to git!" -ForegroundColor Green
Write-Host "?? Your work will now persist after restart" -ForegroundColor Yellow
Write-Host "?? Starting server..." -ForegroundColor Cyan

python manage.py runserver
