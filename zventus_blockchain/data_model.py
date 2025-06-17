from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Borrower(BaseModel):
    street: Optional[str] = ""
    name: str
    email: Optional[str] = ""
    phone: str
    street_2: Optional[str] = ""
    property_city: Optional[str] = ""
    property_country: Optional[str] = ""
    property_state: Optional[str] = ""
    property_zip_code: Optional[str] = ""
    tell_us_about_your_loan: Optional[str] = ""
    property_location: Optional[str] = ""
    property_use: Optional[str] = ""
    property_value: Optional[str] = ""
    line_of_credit: Optional[str] = ""
    plans_for_the_funds: Optional[str] = ""
    loan_used_for_business: Optional[str] = ""
    suffix: Optional[str] = ""
    time_at_address: Optional[str] = ""
    best_time_to_call: Optional[str] = ""
    secondary_phone_number: Optional[str] = ""
    country_of_citizenship: Optional[str] = ""
    country_of_residence: Optional[str] = ""
    social_security_number: Optional[str] = ""
    date_of_birth: Optional[str] = ""
    marital_status: Optional[str] = ""
    preferred_language: Optional[str] = ""
    employment_status: Optional[str] = ""
    anual_income: Optional[str] = ""
    source_of_income: Optional[str] = ""
    additional_income: Optional[str] = ""
    coapplicant: Optional[str] = ""
    current_step: Optional[str]
    data_ids: Optional[list]
    employment_verification: Optional[str] = ""
    appraisal_amount: Optional[str] = ""
    credit_score: Optional[str] = ""
    title_run: Optional[str] = ""


class metadata(BaseModel):
    message: str
    vendor: str
    topics: str


class metadata_and_data(BaseModel):
    metadata: metadata
    borrower_data: Borrower


class input_payload(BaseModel):
    value: metadata_and_data


#### TODO: Fix this mess, I'm mapping the status-quo, but is visibly wrong
class vendor_small_data(BaseModel):
    vendor: str
    decision: str
    topics: str


class metadata_decision_mess(BaseModel):
    vendor: str
    metadata: vendor_small_data


class decision_borrower_info(BaseModel):
    full_data: metadata_decision_mess
    decision: str


class decision_metadata(BaseModel):
    message: str
    vendor: str
    topics: str
    borrower_data: decision_borrower_info


class decision(BaseModel):
    value: decision_metadata
