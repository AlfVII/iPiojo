from fastapi import FastAPI, Request, HTTPException
from app.backend.models import InfectionsTable, Infection
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
import pandas
from datetime import datetime
import json
import sys
import numpy
import copy
import pprint
import os
import pathlib



app = FastAPI()

origins = [
    "https://ipiojo.com",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_all_infections", include_in_schema=False)
def get_all_infections():
    infections = InfectionsTable().get_all_infections()
    infections = infections.to_dict('records')
    return infections


@app.post("/report_infection", include_in_schema=False)
def report_infection():
    roadmap_votes_table = InfectionsTable()
    reported = roadmap_votes_table.report_infection()
    return {"reported": reported}