from pathlib import Path
import json
import pytest


@pytest.fixture
def test_data_dir(scope="session"):
    return Path(__file__).parent / "test_data"


@pytest.fixture
def reactions_examples(test_data_dir):
    file_path = test_data_dir/"reactions.json"
    with open(file_path) as f:
        json_content = json.load(f)
    return json_content
