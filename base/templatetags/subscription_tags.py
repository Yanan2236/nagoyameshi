from django import template 

register = template.Library()

@register.filter(name="is_subscribed")
def is_subscribed(user):
    return user.is_authenticated and hasattr(user, "subscription") and user.subscription.is_active