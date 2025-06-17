import json
import logging

import boto3

import zventus_blockchain.data_model
import zventus_blockchain.helper
import zventus_blockchain.vendor_management


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger = logging.getLogger()
    payload_body = json.loads(event["body"])
    logger.info("Borrower data received")
    try:
        client = boto3.resource("dynamodb")
        table = client.Table("load_data_2")
        loan_id = str(payload_body["metadata"]["topics"])
        table_response = table.put_item(Item={"loan_data": loan_id})

        logger.debug(table_response)
        logger.info("Receiving borrower data")
        if "decision" in payload_body["metadata"]:
            raise zventus_blockchain.helper.IncorrectPayload(
                "You are caling the wrong endpoint"
            )
        print(payload_body)
        base_dict = zventus_blockchain.helper.base_dictionary(payload_body)
        base_dict = zventus_blockchain.vendor_management.call_vendor(
            payload_body=payload_body,
            message="First level",
            current_step="receive_borrower",
            next_step="credit_score",
            notes="Sucess",
            default_value=False,
            base_dict=base_dict,
        )

        logger.info("run credit check")
        base_dict = zventus_blockchain.vendor_management.call_vendor(
            payload_body=payload_body,
            message="Second level",
            current_step="credit_score",
            next_step="appraisal_run",
            notes="Sucess",
            default_value=False,
            base_dict=base_dict,
        )

        logger.info("appraisal check")
        base_dict = zventus_blockchain.vendor_management.call_vendor(
            payload_body=payload_body,
            message="Third level",
            current_step="appraisal_run",
            next_step="title_run",
            notes="Sucess",
            default_value="1M",
            base_dict=base_dict,
        )

        logger.info("title check")
        base_dict = zventus_blockchain.vendor_management.call_vendor(
            payload_body=payload_body,
            message="Fourth level",
            current_step="title_run",
            next_step="employment_verification",
            notes="Sucess",
            default_value=False,
            base_dict=base_dict,
        )

        logger.info("employment check")
        base_dict = zventus_blockchain.vendor_management.call_vendor(
            payload_body=payload_body,
            message="Fifth level",
            current_step="employment_verification",
            next_step="customer_fully_processed",
            notes="Sucess",
            default_value=False,
            base_dict=base_dict,
        )
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"Result": "End to end process has finished successfully"}
            ),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Allow": "GET, OPTIONS, POST",
                "Access-Control-Allow-Methods": "GET, OPTIONS, POST",
                "Access-Control-Allow-Headers": "*",
            },
        }
    except zventus_blockchain.helper.KaleidoIsDown:
        return {
            "statusCode": 503,
            "body": "Kaleido did not respond. Check if Kaleido server is up",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Allow": "GET, OPTIONS, POST",
                "Access-Control-Allow-Methods": "GET, OPTIONS, POST",
                "Access-Control-Allow-Headers": "*",
            },
        }

    except zventus_blockchain.helper.IncorrectPayload:
        return {
            "statusCode": 406,
            "body": "This is not the decision analysis endpoint",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Allow": "GET, OPTIONS, POST",
                "Access-Control-Allow-Methods": "GET, OPTIONS, POST",
                "Access-Control-Allow-Headers": "*",
            },
        }
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
