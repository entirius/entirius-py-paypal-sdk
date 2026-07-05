# paypal-sdk

PayPal payment gateway SDK — authorization and order creation over the PayPal REST API.

## Installation

```shell
pip install entirius-py-paypal-sdk
```

## Usage

```python
from paypal_sdk.services.client import PayPal

paypal = PayPal(client_id="...", client_secret="...", is_sandbox=True)
paypal.authorize()
```

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest) — integration test skipped without PAYPAL_SANDBOX_* env vars
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
