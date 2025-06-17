import json

import pytest

from zventus_blockchain import helper


@pytest.fixture(scope="module")
def input_payload():
    return {
        "body": '{"metadata": {"vendor": "receive_borrower", "topics": "6c63c756-3004-4a70-95c9-8558bb14e653", "message": "A simple message to keep things similar"}, "borrower_data": {"name": "oswaldo", "phone": "", "email": "", "street": "", "street_2": "", "property_city": "", "property_country": "", "property_state": "", "property_zip_code": "", "tell_us_about_your_loan": "", "property_location": "", "property_use": "", "property_value": "", "line_of_credit": "", "plans_for_the_funds": "", "loan_used_for_business": "", "suffix": "", "time_at_address": "", "best_time_to_call": "", "secondary_phone_number": "", "country_of_citizenship": "", "country_of_residence": "", "social_security_number": "", "date_of_birth": "", "marital_status": "", "preferred_language": "", "employment_status": "", "anual_income": "", "source_of_income": "", "additional_income": "", "coapplicant": "", "current_step": "starting_point", "data_ids": ["36c05b95-ef24-47d3-b5bd-9faef0fc8737", "7888be47-e18c-4e69-a21f-88bf4b96f763"]}}'
    }


@pytest.fixture(scope="module")
def payload_body(input_payload):
    return json.loads(input_payload["body"])


@pytest.fixture(scope="module")
def base_dict(payload_body):
    return helper.base_dictionary(payload_body)
