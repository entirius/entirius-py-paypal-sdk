# entirius-py-paypal-sdk

A Python client for the PayPal payment gateway REST API, part of Entirius, the open-source modular ecommerce platform.
It wraps OAuth authorization, order creation, order lookup and payment capture behind one `PayPal` class.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-paypal-sdk.svg)](https://pypi.org/project/entirius-py-paypal-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-paypal-sdk.svg)](https://pypi.org/project/entirius-py-paypal-sdk/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-paypal-sdk/blob/develop/LICENSE)

## What it does

- Authorizes against PayPal with OAuth client credentials (`authorize()`).
- Creates an order from a typed `OrderRequest` DTO (`create_order()`).
- Reads an order and its status by id (`get_order()`).
- Captures the payment of an approved order (`get_capture_payment_for_order()`).
- Targets the sandbox or the production API with the `is_sandbox` flag.

## Installation

```shell
uv add entirius-py-paypal-sdk
pip install entirius-py-paypal-sdk
```

The import name is `paypal_sdk`.

## Quick start

```python
from paypal_sdk.services.client import PayPal

paypal = PayPal(client_id="...", client_secret="...", is_sandbox=True)
paypal.authorize()
```

## Requirements

- Python 3.11 or newer.
- `requests` (installed as a dependency).
- A PayPal REST application (client id and client secret); a sandbox application for testing.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-paypal-sdk/blob/develop/CHANGELOG.md

## Part of Entirius

This SDK is one of the payment gateway clients used by the Entirius backend service (Volkanos) and its modules.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Checkout module: https://github.com/entirius/entirius-django-checkout
- Sibling gateway SDKs: https://github.com/entirius/entirius-py-payu-sdk, https://github.com/entirius/entirius-py-autopay-sdk, https://github.com/entirius/entirius-py-paynow-sdk

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest); the integration test is skipped without PAYPAL_SANDBOX_* env vars
```

Development and agent instructions: https://github.com/entirius/entirius-py-paypal-sdk/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-paypal-sdk/blob/develop/LICENSE.
