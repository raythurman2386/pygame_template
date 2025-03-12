Write-Host "Creating virtual environment..." -ForegroundColor Green
python -m venv venv
Write-Host "Activating virtual environment..." -ForegroundColor Green
.\venv\Scripts\Activate

Write-Host "Installing package and dependencies..." -ForegroundColor Green
pip install -e .

Write-Host "Building executable with PyInstaller..." -ForegroundColor Green
pyinstaller pygame_template.spec

Write-Host "Build complete! Executable is in the dist folder." -ForegroundColor Green