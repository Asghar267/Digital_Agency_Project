from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    id = models.AutoField(primary_key=True,)
    full_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    # password2 = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.full_name



class Service(models.Model):

    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    id = models.AutoField(primary_key=True)
    service_title = models.CharField(max_length=150)   
    description = models.TextField(default=lorem)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Service_images/', blank=True, null=True)
    
    def __str__(self):
        return self.service_title

 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart: {self.service.service_title}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    orderitem = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    # shipping = models.ForeignKey(Shipping_Address, on_delete=models.CASCADE)
    # quantity = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending")
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    
    # OrderItem.objects.create(order=order, service=service, quantity=quantity, price=service.price)
    def __str__(self):
        return self.customer.first_name
