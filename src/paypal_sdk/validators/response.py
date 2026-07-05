# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from requests import Response


def validate_paypal_response(response: Response) -> (bool, dict):
    response_body = json.loads(response.text)

    if response.status_code == 200:
        return True, response_body

    if response.status_code == 201:
        return True, response_body

    if response.status_code == 302:
        return True, response_body

    if response.status_code == 400:
        validation, error_message = validate_paypal_response_body_when_error(response_body)
        if validation:
            raise ValueError(error_message)

    if response.status_code == 401:
        validation, error_message = validate_paypal_response_body_when_error(response_body)
        if validation:
            raise ConnectionError(error_message)

    if response.status_code == 403:
        validation, error_message = validate_paypal_response_body_when_error(response_body)
        if validation:
            raise PermissionError(error_message)

    if response.status_code == 404:
        validation, error_message = validate_paypal_response_body_when_error(response_body)
        if validation:
            raise ValueError(error_message)

    if response.status_code == 408:
        validation, error_message = validate_paypal_response_body_when_error(response_body)
        if validation:
            raise TimeoutError(error_message)

    if response.status_code == 500:
        validation, error_message = validate_paypal_response_body_when_error(response_body)
        if validation:
            raise SystemError(error_message)

    if response.status_code == 503:
        validation, error_message = validate_paypal_response_body_when_error(response_body)
        if validation:
            raise BrokenPipeError(error_message)

    return False, response_body


def validate_paypal_response_body_when_error(response_body: dict) -> (bool, str):
    if "message" in response_body and "debug_id" in response_body:
        error_message = [response_body["message"]]
        debug_id = response_body["debug_id"] if "debug_id" in response_body else ""
        if debug_id != "":
            error_message.append(debug_id)
        details = response_body["details"] if "details" in response_body else {}
        error_message.append(f"details: {details}")
        return True, " | ".join(error_message)
    return False, ""


def validate_paypal_auth_success(response_body: dict) -> bool:
    if (
        "scope" in response_body
        and "access_token" in response_body
        and "token_type" in response_body
        and "app_id" in response_body
        and "expires_in" in response_body
        and "nonce" in response_body
    ):
        return True
    return False


def validate_paypal_create_order(response_body: dict) -> bool:
    if (
        "id" in response_body
        and "status" in response_body
        and "links" in response_body
        and response_body["status"] == "CREATED"
    ):
        return True
    return False


def validate_paypal_get_order(response_body: dict) -> bool:
    if "id" in response_body and "status" in response_body:
        return True
    return False
