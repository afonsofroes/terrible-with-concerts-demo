import pandas as pd
from test_package.main import main
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict")
def predict(min_date: str,
            max_date: str,
            city: str,
            artist_name: str,
            song_name: str):


    return {"results": main(min_date,max_date,city,artist_name,song_name)}



@app.get("/")
def root():
    return dict(greeting="Hello")
