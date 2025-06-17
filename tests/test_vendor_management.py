import json

import pytest
from lambda_local.context import Context
from lambda_local.main import call
from moto import mock_dynamodb

from zventus_blockchain import lambda_function, vendor_management


@pytest.mark.skip(reason="no way of currently testing this")
def test_version(input_payload):

    event = input_payload
    context = Context(5)
    response = call(lambda_function.lambda_handler, event, context)
    assert response[0] == 201


def test_call_mock_provider(payload_body, base_dict):
    result = vendor_management.call_mocked_provider(
        current_step="credit_score",
        next_step="a_test_vendor",
        default_value="default_value",
        message="message",
        notes="notes",
        body=payload_body,
        base_dict=base_dict,
    )

    assert result[1] == 500
    assert result[0]["value"]["metadata"]["vendor"] == "a_test_vendor"
    assert result[0]["value"]["metadata"]["message"] == "message"
    assert result[0]["value"]["metadata"]["notes"] == "notes"
    assert "credit_score" in result[0]["value"]["metadata"].keys()
