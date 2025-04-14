from django.db import models
from django.contrib.auth.models import User

class News(models.Model):

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="Concert News")
    image=models.FileField(upload_to='static/images')
    date_posted = models.DateField()


    def __str__(self):
        return self.title
class Tickets(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    image = models.FileField(upload_to='static/images')
    date_posted = models.DateField()
    price = models.IntegerField()

    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('sold_out', 'Sold Out')], default='available')  # Ticket status

    def __str__(self):
        return f"{self.description} - {self.price} USD"
    
class Merchandise(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    image = models.FileField(upload_to='static/images')
    date_posted = models.DateField()
    price = models.IntegerField()

    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('sold_out', 'Sold Out')], default='available')  # Ticket status

    def __str__(self):
        return f"{self.description} - {self.price} USD"
    
class Album(models.Model):

    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    image = models.FileField(upload_to='static/images')
    date_posted = models.DateField()
    price = models.IntegerField()
 
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('sold_out', 'Sold Out')], default='available')  # Ticket status

    def __str__(self):
        return f"{self.description} - {self.price} USD"
    
# Cart model to represent a user's cart

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"



# CartItem model to store details about items in the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE, null=True, blank=True)
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        if self.ticket:
            return self.quantity * self.ticket.price
        elif self.merchandise:
            return self.quantity * self.merchandise.price
        elif self.album:
            return self.quantity * self.album.price
        return 0

    def __str__(self):
        item = self.ticket or self.merchandise or self.album
        return f"{item.description} x {self.quantity}"




    
    
