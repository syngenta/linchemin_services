from typing import List

import application
import schemas
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World from rxnmapper service!"}


@app.get("/metadata/", response_model=schemas.Metadata)
def get_medadata() -> schemas.Metadata:
    return application.build_metadata()


@app.post("/run_batch/", response_model=schemas.RunBatchOut)
async def perform_reaction_process_batch(
    query_data: List[schemas.QueryReactionString],
    inp_fmt: str = Query("smiles", enum=[x.value for x in schemas.ReactionFormat]),
    out_fmt: str = Query("smiles", enum=[x.value for x in schemas.ReactionFormat]),
) -> schemas.RunBatchOut:
    return application.run_batch(
        query_data=query_data,
        inp_fmt=inp_fmt,
        out_fmt=out_fmt,
    )
