from django import template
from shopping_cart.models import Basket

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        return Basket.objects.filter(customer=user.customer)[0].items.count()
    return 0
