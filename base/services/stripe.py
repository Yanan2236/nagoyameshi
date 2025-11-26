from django.conf import settings
import stripe
from base.models import UserBilling

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_or_create_billing(user):
    billing, created = UserBilling.objects.get_or_create(user=user)
    return billing


def get_or_create_stripe_customer(user):
    billing = get_or_create_billing(user)

    if billing.stripe_customer_id:
        return billing.stripe_customer_id

    customer = stripe.Customer.create(
        email=user.email,
        metadata={"user_id": user.id},
    )

    billing.stripe_customer_id = customer.id
    billing.save(update_fields=["stripe_customer_id"])

    return billing.stripe_customer_id


def charge_subscription(user, amount_jpy: int):
    billing = user.billing

    try:
        charge = stripe.PaymentIntent.create(
            amount=amount_jpy,
            currency="jpy",
            customer=billing.stripe_customer_id,
            payment_method=billing.default_payment_method_id,
            off_session=True,
            confirm=True,
        )
        return charge
    except stripe.error.CardError as e:
        # カードエラーの処理
        raise e