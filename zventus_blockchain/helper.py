import json
import logging
import os
import time

import requests

import zventus_blockchain.data_model as data_model


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# define Python user-defined exceptions
class KaleidoIsDown(Exception):
    """Raised when Kaleido is not responding even after retrying"""

    pass


class IncorrectPayload(Exception):
    """Raised when incorrect input payload is sent"""

    pass


def call_chain(
    data: dict,
    tag: str,
    topics: str,
    receiver: str,
):

    firefly_server = os.environ["FIREFLY_SERVER"]
    logger.info(f"this is the server url {firefly_server}")
    headers = {
        "Authorization": "Basic dTBqbW1mam12NTphNGV3WjZuNVh1bHBSVElmMXNKX2FWa1pYQjZ3RGtLaFVhSVFUMEVNbVJF",
        "Content-Type": "application/json",
    }
    if "kaleido.io" not in firefly_server:
        del headers["Authorization"]

    payload = json.dumps(
        {
            "header": {"tag": tag, "topics": [topics]},
            "data": [data.dict()],
            "group": {"members": [{"identity": receiver}]},
        }
    )

    logger.debug("call chain payload")
    logger.debug(payload)

    return _call_chain(firefly_server, payload, headers)


def _call_chain(firefly_server, payload, headers):
    logger = logging.getLogger()
    logging.debug("Calling kaleido")
    for _ in range(0, 3):
        try:
            response = requests.request(
                "POST",
                firefly_server + "/api/v1/namespaces/default/messages/private",
                headers=headers,
                data=payload,
            )
            logger.debug(response.text)
            return json.loads(response.text)
        except json.JSONDecodeError:
            time.sleep(_ * 5)
            logger.info(f"Kaleido backend failing retrying in {_ * 5} seconds")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.info(message)
    logger.error("Kaleido is not responding even after retrying")
    raise KaleidoIsDown("Kaleido is not responding even after retrying")


def get_update_params(body):
    """Given a dictionary we generate an update expression and a dict of values
    to update a dynamodb table.

    Params:
        body (dict): Parameters to use for formatting.

    Returns:
        update expression, dict of values.
    """
    update_expression = ["set "]
    update_values = dict()

    for key, val in body.items():
        update_expression.append(f" {key} = :{key},")
        update_values[f":{key}"] = val

    return "".join(update_expression)[:-1], update_values


def response(payload: dict):
    return {
        "statusCode": 200,
        "body": json.dumps(payload),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Allow": "GET, OPTIONS, POST",
            "Access-Control-Allow-Methods": "GET, OPTIONS, POST",
            "Access-Control-Allow-Headers": "*",
        },
    }


def parse_input_payload(body: dict):
    borrower_info = data_model.Borrower(**body["borrower_data"])
    data = {
        "value": {
            "metadata": {
                "vendor": "run_credit_check",
                "topics": body["metadata"]["topics"],
                "message": "First level",
            },
            "borrower_data": borrower_info,
        }
    }
    data = data_model.input_payload(**data)
    return data


def base_dictionary(data):
    data = data_model.Borrower(**data["borrower_data"])
    return data
