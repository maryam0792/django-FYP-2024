from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    
    fullname=models.TextField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    image=models.FileField(upload_to="upload/profile",default="abc")
    type=models.CharField(max_length=100 , default="customer")
    status=models.CharField(max_length=100,default="Active")
    # Method to check if the user is a customer
    def is_customer(self):
        return self.type == "customer"
    
    # Method to check if the user is an admin
    def is_admin(self):
        return self.type == "admin"
    
    def __str__(self):
        return self.fullname

# game 

class PlayerScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    score = models.IntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'{self.player_name}: {self.score}'
    
# for  coins 

class UserCurrency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)
    rupees = models.FloatField(default=0.0)

    def update_coins_and_rupees(self, score):
        # Calculate and update coins
        new_coins = score * 20
        self.coins += new_coins
        
        # Update rupees based on coins
        self.rupees = self.coins // 100
        
        self.save()
        # discount
    def redeem_coins(self, amount):
        # Redeem coins for discount
        if self.coins >= 200:
            discount = min(self.coins // 500 * 100, amount)  # 100 Rs discount per 200 coins
            self.coins -= (discount // 100) * 500  # Deduct used coins
            self.save()
            return discount
        return 0

class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.FileField(upload_to='upload/')
    
class Product(models.Model):
    title=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    description=models.CharField(max_length=1000)
    image=models.FileField(upload_to='upload/products/')  
    tryon=models.FileField(upload_to='upload/tryon/')
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  # Add this line

class Cart(models.Model):
    quantity=models.IntegerField(default=0)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(User,on_delete=models.CASCADE)

class Order(models.Model):
    
    bill=models.IntegerField(default=0)
    fullname=models.CharField(max_length=100)
    phone=models.CharField(max_length=11)
    address=models.CharField(max_length=500)
    city=models.CharField(max_length=50)
    area=models.CharField(max_length=500)
    areacode=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
 
def __str__(self):
        return f"Order {self.id} by {self.fullname}"

class OrderItem(models.Model):
    quantity=models.IntegerField(default=0)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
