import json
import logging
import os

import boto3

import zventus_blockchain.data_model
import zventus_blockchain.data_model as data_model
from zventus_blockchain import helper, mock_db2


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_new_entry(payload_body):
    client = boto3.resource("dynamodb")
    table = client.Table("load_data_2")
    loan_id = str(payload_body["metadata"]["topics"])
    table_response = table.put_item(Item={"loan_data": loan_id})


def call_vendor(
    payload_body: dict,
    message: str,
    current_step: str,
    next_step: str,
    notes: str,
    default_value: str,
    base_dict: data_model.Borrower,
):
    """A function that manages the mock calls to different vendors.


    This function needs

    Args:
        payload_body : This is the input payload.
        message : Here you can add a custom pinned message together with the mocked response.
        current_step: Current step to mock.
        next_step: Next step which will trigger a mock to the following vendor.
        notes: Another field for leaving notes that will be pinned.
        default_value: This is the default value for the mocked process.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/
    """

    data, new_value, base_dict = call_mocked_provider(
        current_step=current_step,
        default_value=default_value,
        next_step=next_step,
        message=message,
        notes=notes,
        body=payload_body,
        base_dict=base_dict,
    )

    data = data_model.input_payload(**data)
    logger.info(current_step)
    logger.info(json.dumps(data.dict()))
    call_kaleido_api(
        data=data,
        next_step=next_step,
        payload_body=payload_body,
        current_step=current_step,
    )

    write_to_dynamo(
        current_step=current_step, new_value=new_value, payload_body=payload_body
    )

    return base_dict


def call_mocked_provider(
    current_step: str,
    default_value: str,
    next_step: str,
    message: str,
    notes: str,
    body: dict,
    base_dict: zventus_blockchain.data_model.Borrower,
):
    new_value = mock_db2.vendor_mock[current_step].get(
        body["borrower_data"]["name"].lower(), default_value
    )
    base_dict.current_step = new_value

    if current_step == "employment_verification":
        base_dict.employment_verification = new_value

    if current_step == "appraisal_run":
        new_value = mock_db2.vendor_mock[current_step].get(
            body["borrower_data"]["street"].lower(), default_value
        )
        base_dict.current_step = new_value
        base_dict.appraisal_amount = new_value

    if current_step == "credit_score":
        base_dict.credit_score = new_value

    if current_step == "title_run":
        base_dict.title_run = new_value

    data = {
        "value": {
            "metadata": {
                "message": message,
                current_step: new_value,
                "notes": notes,
                "vendor": next_step,
                "topics": body["metadata"]["topics"],
            },
            "borrower_data": base_dict,
        }
    }
    return data, new_value, base_dict


def call_kaleido_api(data: dict, next_step: str, payload_body: dict, current_step: str):
    """Send a message using Kaleido API

    Args:
        data: This is the borrower dictionary that will be sent as a message to Kaleido.
        next_step: Next step of the process.
        payload_body: Input payload as received by AWS Lambda.
        current_step: This is the current step.

    Returns:
        _type_: _description_
    """
    if "kaleido.io" in os.environ["FIREFLY_SERVER"]:
        firefly_receiver = "u0t9q1a0v9"
    else:
        firefly_receiver = "did:firefly:node/node_7182f1"
    response = helper.call_chain(
        data=data,
        tag=next_step,
        receiver=firefly_receiver,
        topics=payload_body["metadata"]["topics"],
    )

    response[current_step] = True
    filtered_response = {
        key: response[key] for key in [current_step, "data", "hash", "header"]
    }
    return filtered_response


def write_to_dynamo(current_step: str, new_value: str, payload_body: dict):
    """Update DynamoDB with the loan ID

    Args:
        current_step: This is the current step.
        new_value: This is the new value.
        payload_body: This is the payload received by AWS lambda.
    """
    client = boto3.resource("dynamodb")

    # this will search for dynamoDB table
    # your table name may be different
    table = client.Table("load_data_2")

    a, v = helper.get_update_params(
        {current_step: new_value, "payload_data": payload_body}
    )
    table.update_item(
        Key={"loan_data": str(payload_body["metadata"]["topics"])},
        UpdateExpression=a,
        ExpressionAttributeValues=dict(v),
    )
