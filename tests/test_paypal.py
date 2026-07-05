# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os

import pytest

from paypal_sdk.dto.payment import (
    Amount,
    ApplicationContext,
    Breakdown,
    Item,
    OrderRequest,
    OrderResponse,
    PurchaseUnits,
    Tax,
    UnitAmount,
)
from paypal_sdk.services.auth import Authorization
from paypal_sdk.services.client import PayPal

SANDBOX_CLIENT_ID = os.environ.get("PAYPAL_SANDBOX_CLIENT_ID")
SANDBOX_SECRET = os.environ.get("PAYPAL_SANDBOX_SECRET")
IS_SANDBOX = True

pytestmark = pytest.mark.skipif(
    not (SANDBOX_CLIENT_ID and SANDBOX_SECRET),
    reason="PayPal sandbox credentials not set (PAYPAL_SANDBOX_* env vars)",
)


def test_authorize():
    paypal = PayPal(client_id=SANDBOX_CLIENT_ID, client_secret=SANDBOX_SECRET, is_sandbox=IS_SANDBOX)
    paypal.authorize()
    assert isinstance(paypal.authorization, Authorization)


def test_create_order():
    order_data = OrderRequest(
        intent="CAPTURE",
        purchase_units=[
            PurchaseUnits(
                items=[
                    Item(
                        name="T-Shirt",
                        quantity="1",
                        description="Green XL",
                        sku="T-Shirt",
                        unit_amount=UnitAmount(currency_code="USD", value="80.00"),
                        tax=Tax(
                            currency_code="USD",
                            value="20.00",
                        ),
                    )
                ],
                amount=Amount(
                    currency_code="USD",
                    value="100.00",
                    breakdown=Breakdown(
                        item_total=UnitAmount(currency_code="USD", value="80.00"),
                        tax_total=UnitAmount(currency_code="USD", value="20.00"),
                    ),
                ),
            )
        ],
        application_context=ApplicationContext(
            return_url="https://example.com/return",
            cancel_url="https://example.com/cancel",
        ),
    )

    paypal = PayPal(client_id=SANDBOX_CLIENT_ID, client_secret=SANDBOX_SECRET, is_sandbox=IS_SANDBOX)
    response, is_success = paypal.create_order(order_data=order_data)
    assert isinstance(OrderResponse(**response), OrderResponse)
    assert is_success
