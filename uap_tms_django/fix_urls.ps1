# This script will fix the URL patterns in your urls.py
$content = Get-Content -Path "urls.py" -Raw

# Fix the URL patterns by removing spaces after transport/
$fixed_content = $content -replace "transport/ s", "transport/s" -replace "transport/ l", "transport/l"

Set-Content -Path "urls.py" -Value $fixed_content
Write-Host "URL patterns fixed successfully!" -ForegroundColor Green
