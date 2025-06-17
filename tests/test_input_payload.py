import json

import pytest
from pydantic import ValidationError

import zventus_blockchain.data_model as data_model


def test_input_payload(input_payload):
    # Tests borrower_info inside the body
    borrower_data = json.loads(input_payload["body"])["borrower_data"]
    assert data_model.Borrower(**borrower_data)
    del borrower_data["name"]
    with pytest.raises(ValidationError):
        data_model.Borrower(**borrower_data)

    # Test data and metadata
    data_and_meta = json.loads(input_payload["body"])
    assert data_model.metadata_and_data(**data_and_meta)
    with pytest.raises(ValidationError):
        del data_and_meta["borrower_data"]
        data_model.metadata_and_data(**data_and_meta)
