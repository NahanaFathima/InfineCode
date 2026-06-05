# Dataset Explorer

## Project Setup Instructions

- **Frontend (Vite + React + TypeScript)**

  1. Open a terminal and change to the frontend folder:

  ```bash
  cd frontend
  ```

  2. Install dependencies (npm):

  ```bash
  npm install
  ```

  3. Start the development server:

  ```bash
  npm run dev
  ```

  The dev server usually runs at http://localhost:5173.

-- **Backend (FastAPI)**

  The backend uses FastAPI with Uvicorn. The main application file is `backend/main.py`. A `requirements.txt` and a convenience `run.ps1` script are provided to install dependencies and start the server.

  Quick run (PowerShell, from repo root):

  ```powershell
  cd backend
  .\run.ps1
  ```

  The `run.ps1` script will activate the existing virtual environment, install the requirements from `requirements.txt` if needed, and start Uvicorn at `http://127.0.0.1:8000`.

  Manual run (if you prefer):

  ```powershell
  cd backend
  .\venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  uvicorn main:app --reload --host 127.0.0.1 --port 8000
  ```

  Notes:
  - App module: `backend/main.py` (copy of the working app originally in `backend/venv/main.py`).
  - Requirements: `backend/requirements.txt` lists `fastapi`, `uvicorn`, `pandas`, and `python-multipart`.
  - If you'd rather keep the app inside the venv, that's fine — these additions are non-destructive.

## Features Implemented

- Frontend: React + TypeScript + Vite starter
- Tailwind CSS integration (package present)
- Axios installed for HTTP requests
- ESLint + TypeScript dev tooling configured
- Backend: FastAPI app implemented (`backend/main.py`) with dataset endpoints and CSV upload

## Screenshots of the Application


![Home view](docs/screenshots/home.png)
![Detail view](docs/screenshots/details.png)
```



## API Documentation / Endpoint List

The backend exposes dataset management endpoints at the base `http://127.0.0.1:8000`.

- GET /datasets
  - Description: Returns a list of datasets
  - Query params: `?search=` optional case-insensitive name search

- GET /datasets/stats
  - Description: Returns dataset counts by type and total

- GET /datasets/{id}
  - Description: Returns dataset details for the given `id`

- POST /datasets
  - Description: Create a new dataset
  - Body: JSON matching the `Dataset` model (id, name, description, type, rows, features, status)

- POST /datasets/upload-csv
  - Description: Upload a CSV file to create a new tabular dataset
  - Form field: file (multipart/form-data) — file must end with `.csv`

- PUT /datasets/{id}
  - Description: Replace/update dataset `id` with the provided JSON body

- DELETE /datasets/{id}
  - Description: Delete dataset `id`

Example curl requests:

```bash
# List datasets
curl http://127.0.0.1:8000/datasets

# Upload CSV (multipart)
curl -F "file=@mydata.csv" http://127.0.0.1:8000/datasets/upload-csv
```

