from linchemin_services.rxnmapper import service


def test_endpoint_metadata():
    rxnmapper_service = service.RxnMapperService(base_url="http://127.0.0.1:8003/")
    # print("\n metadata")
    endpoint = rxnmapper_service.endpoint_map.get("metadata")
    inp_example = endpoint.input_example
    out_example = endpoint.output_example
    out_request = endpoint.submit(request_input=inp_example)
    # print("input", inp_example)
    # print("expected", out_example)
    # print("actual", out_request)
    assert inp_example is None
    assert out_example.keys() == out_request.keys()


def test_endpoint_run_batch():
    rxnmapper_service = service.RxnMapperService(base_url="http://127.0.0.1:8003/")
    # print("\n run_batch")
    endpoint = rxnmapper_service.endpoint_map.get("run_batch")
    inp_example = endpoint.input_example
    out_example = endpoint.output_example
    request_output = endpoint.submit(request_input=inp_example)
    # print("input", inp_example)
    # print("expected", out_example)
    # print("actual", request_output)
    assert out_example.get("output") == request_output.get("output")


def test_reactions(reactions_examples):
    rxnmapper_service = service.RxnMapperService(base_url="http://127.0.0.1:8003/")
    endpoint = rxnmapper_service.endpoint_map.get("run_batch")
    query_data = reactions_examples
    request_input = {"classification_code": "rxnmapper",
                     "inp_fmt": "smiles",
                     "out_fmt": "smiles",
                     "mapping_style": "matching",
                     "query_data": query_data

                     }

    request_output = endpoint.submit(request_input=request_input)
    assert "metadata" in request_output.keys()
    assert "query_parameters" in request_output.keys()
    assert "outcome" in request_output.keys()
    assert "output" in request_output.keys()
    output = request_output.get("output")
    assert "successes_list" in output.keys()
    assert "failures_list" in output.keys()
    successes_list = output.get("successes_list")
    failures_list = output.get("failures_list")
    assert isinstance(successes_list, list)
    assert isinstance(failures_list, list)

