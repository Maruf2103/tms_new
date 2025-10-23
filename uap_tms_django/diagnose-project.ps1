# diagnose-project.ps1
Write-Host "?? Project Structure Diagnostic" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Yellow

# Check current directory
Write-Host "`n?? Current Location:" -ForegroundColor Green
Get-Location

# Check Django project structure
Write-Host "`n?? Directory Structure:" -ForegroundColor Green
Get-ChildItem -Recurse -Depth 2 | Select-Object Name, FullName | Format-Table -AutoSize

# Check if manage.py exists
Write-Host "`n?? Django Files Check:" -ForegroundColor Green
if (Test-Path "manage.py") {
    Write-Host "? manage.py found" -ForegroundColor Green
} else {
    Write-Host "? manage.py NOT found - Not in Django project root" -ForegroundColor Red
}

# Check for apps
$apps = @("transportation", "custom_admin")
foreach ($app in $apps) {
    if (Test-Path $app) {
        Write-Host "? $app directory found" -ForegroundColor Green
        if (Test-Path "$app\urls.py") {
            Write-Host "  ? $app/urls.py found" -ForegroundColor Green
        } else {
            Write-Host "  ? $app/urls.py NOT found" -ForegroundColor Red
        }
    } else {
        Write-Host "? $app directory NOT found" -ForegroundColor Red
    }
}

# Check main urls.py
if (Test-Path "uap_tms_django\urls.py") {
    Write-Host "? uap_tms_django/urls.py found" -ForegroundColor Green
} else {
    Write-Host "? uap_tms_django/urls.py NOT found" -ForegroundColor Red
}

Write-Host "`n?? Recommended Action:" -ForegroundColor Cyan
if (Test-Path "manage.py") {
    Write-Host "You're in the correct directory. Let's fix the missing files." -ForegroundColor Green
} else {
    Write-Host "You need to navigate to your Django project directory." -ForegroundColor Yellow
}
