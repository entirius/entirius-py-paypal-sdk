# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from requests import Response

if TYPE_CHECKING:
    from paypal_sdk.services.client import PayPal

from requests.auth import HTTPBasicAuth

SANDBOX_URL = "https://api-m.sandbox.paypal.com"
LIVE_URL = "https://api-m.paypal.com"


def get_api_url(is_sandbox):
    if is_sandbox:
        return SANDBOX_URL
    else:
        return LIVE_URL


class Request:
    method: str
    resource: str
    auth: PayPal | HTTPBasicAuth
    headers: dict | None
    params: dict | None
    data: dict | None

    def __init__(
        self,
        method: str,
        resource: str,
        auth: PayPal | HTTPBasicAuth = None,
        params=None,
        headers=None,
        data: dict | str = None,
    ):
        if headers is None:
            headers = {}
        self.method = method
        self.resource = resource
        self.auth = auth
        self.headers = headers
        self.params = params
        self.data = data

    def _build_url(self, is_sandbox) -> str:
        return get_api_url(is_sandbox) + self.resource

    def add_prefer_to_header(self):
        self.headers["Prefer"] = "return=representation"

    def add_content_type_to_header(self):
        self.headers["Content-Type"] = "application/json"

    def make_request(self, is_sandbox) -> Response:
        self.add_content_type_to_header()
        res = requests.request(
            method=self.method, url=self._build_url(is_sandbox), auth=self.auth, headers=self.headers, data=self.data
        )
        return res
