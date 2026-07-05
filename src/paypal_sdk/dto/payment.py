# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import asdict, dataclass


def remove_none_values(dictionary):
    return {k: v for k, v in dictionary.items() if v is not None}


@dataclass
class DTO:
    def to_dict(obj):
        return asdict(obj, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})


@dataclass
class UnitAmount(DTO):
    currency_code: str
    value: str


@dataclass
class Breakdown(DTO):
    item_total: UnitAmount = None
    shipping: UnitAmount = None
    handling: UnitAmount = None
    tax_total: UnitAmount = None
    insurance: UnitAmount = None
    shipping_discount: UnitAmount = None
    discount: UnitAmount = None


@dataclass
class Tax(DTO):
    currency_code: str
    value: str


@dataclass
class Item(DTO):
    name: str
    quantity: str
    sku: str
    unit_amount: UnitAmount
    tax: Tax
    description: str = None
    category: str = None


@dataclass
class Amount(DTO):
    currency_code: str
    value: str
    breakdown: Breakdown | None = None


@dataclass
class PaymentInstruction(DTO):
    amount: Amount
    payee: dict


@dataclass
class Address(DTO):
    address_line_1: str
    admin_area_1: str
    postal_code: str
    country_code: str
    address_line_2: str
    admin_area_2: str


@dataclass
class Shipping(DTO):
    type: str

    address: Address
    name: dict = None


@dataclass
class SupplementaryData(DTO):
    card: dict


@dataclass
class PurchaseUnits(DTO):
    items: list[Item]
    amount: Amount
    reference_id: str = None
    description: str = None
    custom_id: str = None
    invoice_id: str = None
    soft_descriptor: str = None
    payee: dict = None
    payment_instruction: PaymentInstruction = None
    shipping: Shipping = None
    supplementary_data: SupplementaryData = None


@dataclass
class Payer(DTO):
    email_address: str
    name: dict
    phone: dict
    birth_date: str = None
    tax_info: dict = None
    address: Address = None


@dataclass
class PaymentSource(DTO):
    card: dict = None
    token: dict = None
    paypal: dict = None
    bancontact: dict = None
    blik: dict = None
    eps: dict = None
    giropay: dict = None
    ideal: dict = None
    mybank: dict = None
    p24: dict = None
    sofort: dict = None
    trustly: dict = None
    venmo: dict = None


@dataclass
class ApplicationContext(DTO):
    return_url: str
    cancel_url: str
    brand_name: str = None
    landing_page: str = None
    shipping_preference: str = None
    user_action: str = None
    locale: str = None
    payment_method: dict = None
    stored_payment_source: dict = None


@dataclass
class OrderRequest(DTO):
    purchase_units: list[PurchaseUnits]
    intent: str
    application_context: ApplicationContext
    payer: Payer | None = None
    payment_source: PaymentSource | None = None


@dataclass
class OrderResponseLinks(DTO):
    href: str
    rel: str
    method: str


@dataclass
class OrderResponse(DTO):
    id: str
    status: str
    links: list[OrderResponseLinks]
