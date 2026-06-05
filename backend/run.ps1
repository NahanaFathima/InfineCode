Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
Write-Host "Activating virtual environment and installing requirements (if needed)..."
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Write-Host "Starting Uvicorn on http://127.0.0.1:8000"
uvicorn main:app --reload --host 127.0.0.1 --port 8000
