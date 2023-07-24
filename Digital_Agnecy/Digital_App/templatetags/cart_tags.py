from django import template
register = template.Library()
 
@register.filter
def total_price_products(cart_items): # total of all products
    sum =0
    for i in cart_items:
        sum += i['quantity']* i['service'].price
    return sum
    
