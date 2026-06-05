from io import StringIO
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Dataset(BaseModel):
    id: int
    name: str
    description: str
    type: str
    rows: int
    features: int
    status: str

datasets = [
    {
        "id": 1,
        "name": "Iris Dataset",
        "description": "Flower classification dataset",
        "type": "Tabular",
        "rows": 150,
        "features": 4,
        "status": "Ready for Training"
    },
    {
        "id": 2,
        "name": "MNIST",
        "description": "Handwritten digit images",
        "type": "Image",
        "rows": 70000,
        "features": 784,
        "status": "Exploring"
    },
    {
        "id": 3,
        "name": "IMDB Reviews",
        "description": "Movie review sentiment data",
        "type": "Text",
        "rows": 50000,
        "features": 1,
        "status": "Not Explored"
    },
    {
        "id": 4,
        "name": "ESC-50",
        "description": "Environmental audio clips",
        "type": "Audio",
        "rows": 2000,
        "features": 1,
        "status": "Exploring"
    },
    {
        "id": 5,
        "name": "Titanic",
        "description": "Passenger survival prediction dataset",
        "type": "Tabular",
        "rows": 891,
        "features": 12,
        "status": "Trained"
    }
]


def get_next_dataset_id() -> int:
    return max((dataset["id"] for dataset in datasets), default=0) + 1


@app.get("/datasets")
def get_datasets(search: str | None = None):
    if search:
        search_term = search.lower()
        return [
            dataset
            for dataset in datasets
            if search_term in dataset["name"].lower()
        ]

    return datasets

@app.get("/datasets/stats")
def get_stats():
    return {
        "total": len(datasets),
        "tabular": len([d for d in datasets if d["type"] == "Tabular"]),
        "image": len([d for d in datasets if d["type"] == "Image"]),
        "text": len([d for d in datasets if d["type"] == "Text"]),
        "audio": len([d for d in datasets if d["type"] == "Audio"]),
    }
@app.post("/datasets")
def create_dataset(dataset: Dataset):
    datasets.append(dataset.dict())
    return dataset


@app.post("/datasets/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    contents = await file.read()

    try:
        dataframe = pd.read_csv(StringIO(contents.decode("utf-8-sig")))
    except UnicodeDecodeError:
        dataframe = pd.read_csv(StringIO(contents.decode("latin-1")))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {exc}") from exc

    rows, columns = dataframe.shape
    dataset = {
        "id": get_next_dataset_id(),
        "name": Path(file.filename).stem,
        "description": "Imported from CSV file",
        "type": "Tabular",
        "rows": rows,
        "features": columns,
        "status": "Not Explored",
        "columns": columns,
    }

    datasets.append(dataset)
    return dataset

@app.get("/datasets/{id}")
def get_dataset(id: int):

    for dataset in datasets:
        if dataset["id"] == id:
            return dataset

    return {"message": "Dataset not found"}

@app.delete("/datasets/{id}")
def delete_dataset(id: int):

    for dataset in datasets:
        if dataset["id"] == id:
            datasets.remove(dataset)
            return {"message": "Dataset deleted"}

    return {"message": "Dataset not found"}

@app.put("/datasets/{id}")
def update_dataset(id: int, updated_dataset: Dataset):

    for i in range(len(datasets)):
        if datasets[i]["id"] == id:
            datasets[i] = updated_dataset.dict()
            return updated_dataset


    return {"message": "Dataset not found"}
