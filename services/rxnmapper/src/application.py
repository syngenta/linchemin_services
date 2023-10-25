from multiprocessing import Pool
from typing import Tuple

import rdkit
import rxnmapper
from rxnmapper import RXNMapper
from schemas import *

TOOLKIT = "RDKit"
TOOLKIT_VERSION = rdkit.__version__
A2A_MAPPER = "rxnmapper"
A2A_MAPPER_VERSION = rxnmapper.__version__


def build_metadata() -> Metadata:
    return Metadata(
        ci_toolkit=Software(name=TOOLKIT, version=TOOLKIT_VERSION),
        a2a_mapper=Software(name=A2A_MAPPER, version=A2A_MAPPER_VERSION),
    )


def process_item(item: Tuple[int, QueryReactionString]):
    (idx, input_data) = item
    reaction_smiles = input_data.input_string
    query_id = input_data.query_id

    try:
        rxn_mapper = RXNMapper()
        result = rxn_mapper.get_attention_guided_atom_maps([reaction_smiles])[0]
        output_single = {
            "query_id": query_id,
            "output_string": result.get("mapped_rxn"),
            "confidence": round(result.get("confidence"), 3),
            "success": True,
            "notes": {},
        }
    except Exception as e:
        success = False
        output_single = {
            "query_id": query_id,
            "success": success,
            "error_msg": f"problems processing reaction: {e}",
        }

    return idx, ResultsReactionString(**output_single)


def run_batch(
    query_data: List[QueryReactionString],
    inp_fmt: str,
    out_fmt: str,
) -> RunBatchOut:
    qdm = dict(enumerate(query_data))

    with Pool(5) as p:
        results_raw = p.map(process_item, qdm.items())

    successes_list = []
    failures_list = []
    for idx, x in results_raw:
        if x.success:
            successes_list.append(x)
        else:
            failures_list.append(qdm.get(idx))
    output = {"successes_list": successes_list, "failures_list": failures_list}

    query_parameters = {
        "inp_fmt": inp_fmt,
        "out_fmt": out_fmt,
    }
    outcome = {}

    return RunBatchOut(
        metadata=build_metadata(),
        query_parameters=query_parameters,
        output=output,
        outcome=outcome,
    )
