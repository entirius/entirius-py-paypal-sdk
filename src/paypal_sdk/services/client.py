# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
import time

from requests.auth import HTTPBasicAuth

from paypal_sdk.dto.payment import OrderRequest
from paypal_sdk.exceptions import PayPalError
from paypal_sdk.services.auth import Authorization
from paypal_sdk.services.request import Request
from paypal_sdk.utils.order import get_href_for_rel
from paypal_sdk.validators.response import (
    validate_paypal_auth_success,
    validate_paypal_create_order,
    validate_paypal_get_order,
    validate_paypal_response,
)

logger_process = logging.getLogger("process")


class PayPal:
    client_id: str
    client_secret: str
    is_sandbox: bool
    authorization: Authorization = None

    def __init__(self, client_id: str, client_secret: str, is_sandbox: bool, authorization: Authorization = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.is_sandbox = is_sandbox
        self.authorization = authorization
        self.authorize()

    def authorize(self):
        data = {"grant_type": "client_credentials"}
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        request = Request(method="POST", resource="/v1/oauth2/token", auth=auth, data=data, headers=headers)
        response = request.make_request(self.is_sandbox)
        validation, response_body = validate_paypal_response(response)
        if validation:
            success = validate_paypal_auth_success(response_body)
            if success:
                self.authorization = Authorization(
                    **response_body, expires_at=int(time.time()) + response_body["expires_in"]
                )
            else:
                logger_process.error(
                    "PayPal API response failed",
                    extra={"details": {"request_params": request.params, "response_body": response_body}},
                )
                raise PayPalError("PayPal response is not correct.")
        else:
            raise PayPalError(f"The PayPal API responded with an error. Message: {response_body.get('error')}")

    def create_order(self, order_data: OrderRequest):
        """Creates order in paypal. This request return response with 4 links:"""

        request = Request(
            method="POST",
            resource="/v2/checkout/orders",
            headers=self.authorization.get_auth_header(),
            data=json.dumps(order_data.to_dict()),
        )
        response = request.make_request(self.is_sandbox)
        validation, response_body = validate_paypal_response(response)
        if validation:
            success = validate_paypal_create_order(response_body)
            if success:
                return response_body, get_href_for_rel(response_body["links"], "approve")
            else:
                logger_process.error(
                    "PayPal API response failed",
                    extra={"details": {"request_params": request.params, "response_body": response_body}},
                )
                raise PayPalError("PayPal response is not correct.")
        else:
            logger_process.error(
                "PayPal API response failed",
                extra={"details": {"request_params": request.params, "response_body": response_body}},
            )
            raise PayPalError(f"The PayPal API responded with an error. Message: {response_body.get('message')}")

    def get_order(self, order_id: str):
        """Shows details for an order, by ID."""

        request = Request(
            method="GET", resource=f"/v2/checkout/orders/{order_id}", headers=self.authorization.get_auth_header()
        )
        response = request.make_request(self.is_sandbox)
        validation, response_body = validate_paypal_response(response)
        if validation:
            success = validate_paypal_get_order(response_body)
            if success:
                return response_body, response_body["status"]
            else:
                logger_process.error(
                    "PayPal API response failed",
                    extra={"details": {"request_params": request.params, "response_body": response_body}},
                )
                raise PayPalError("PayPal response is not correct.")
        else:
            raise PayPalError(f"The PayPal API responded with an error. Message: {response_body.get('message')}")

    def get_capture_payment_for_order(self, order_id: str):
        """Captures payment for an order. To successfully capture payment for an order, the buyer must first approve the order or a valid payment_source must be provided in the request."""

        request = Request(
            method="POST",
            resource=f"/v2/checkout/orders/{order_id}/capture",
            headers=self.authorization.get_auth_header(),
        )
        response = request.make_request(self.is_sandbox)
        validation, response_body = validate_paypal_response(response)
        if validation:
            success = validate_paypal_get_order(response_body)
            if success:
                return response_body, response_body["status"]
            else:
                logger_process.error(
                    "PayPal API response failed",
                    extra={"details": {"request_params": request.params, "response_body": response_body}},
                )
                raise PayPalError("PayPal response is not correct.")
        else:
            logger_process.error(
                "PayPal API response failed",
                extra={"details": {"request_params": request.params, "response_body": response_body}},
            )
            raise PayPalError(f"The PayPal API responded with an error. Message: {response_body.get('message')}")
