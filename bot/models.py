from django.db import models


# Create your models here.


class TgUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    ism = models.CharField(max_length=1278, null=True)
    familiya = models.CharField(max_length=1278, null=True)
    username = models.CharField(max_length=56, null=True)
    phone = models.CharField(max_length=20, null=True)
    lang = models.CharField(max_length=2, default='uz')
    log = models.JSONField(default={"state": 0})
    is_admin = models.BooleanField(default=False)
    menu = models.SmallIntegerField(default=1)


class Category(models.Model):
    name = models.CharField(max_length=128)
    img = models.ImageField(upload_to='ctg')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    ctg = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='product')
    price = models.IntegerField()
    tarkibi = models.TextField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.BigIntegerField()
    quent = models.IntegerField(default=1)
    summ = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.summ = int(self.quent) * int(self.product.price)
        return super(Cart, self).save(*args, **kwargs)
