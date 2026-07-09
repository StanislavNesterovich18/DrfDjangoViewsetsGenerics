import stripe

from config.settings import STRIPE_TOKEN

stripe.api_key = STRIPE_TOKEN


def create_stripe_product(name):
    stripe_product = stripe.Product.create(
        name=name,
    )
    return stripe_product


def create_stripe_price(product_id, price):
    stripe_price = stripe.Price.create(
        currency="usd",
        product=product_id,
        unit_amount=price,
    )
    return stripe_price


def create_stripe_session(price):
    stripe_session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        line_items=[
            {
                "price": price,
                "quantity": 1,
            }
        ],
        mode="payment",
    )
    return stripe_session
