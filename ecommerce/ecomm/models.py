# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ObjectManager(models.Manager):
    def get_by_natural_key(self, NameProduct, PictureProductName):
        return self.get(NameProduct=NameProduct, PictureProductName=PictureProductName)


class ConfigFail(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    ID = models.IntegerField(primary_key = True)
    Name = models.CharField(max_length=20)
    FailureRateService = models.FloatField(default=0)
    ErrorMessage = models.CharField(max_length=255, default="")
    OkMessage = models.CharField(max_length=255, default="OK")

       # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('ConfigFail', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.ID) + " " + str(self.Name) + " " + str(self.FailureRateService)


class TimeRate(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    ID = models.IntegerField(primary_key=True)
    ID_ConfigFail = models.ForeignKey(ConfigFail, on_delete=models.CASCADE)
    TimeRate = models.FloatField(default=0)
    TimeMin = models.IntegerField(default=0)
    TimeMax = models.IntegerField(default=0)

       # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('ConfigFail', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return "id: {} TimeRate: {} TimeMin: {} TimeMax: {}".format(self.ID,self.TimeRate,self.TimeMin,self.TimeMax)


class Currency(models.Model):
    # Fields
    ID = models.IntegerField(primary_key = True)
    Name = models.CharField(max_length=255)
    Symbol = models.CharField(max_length=1, default="")
    In_Use = models.BooleanField(default=False)

       # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('User', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return "id: {} Name: {} Symbol: {} In Use: {}".format(self.ID, self.Name, self.Symbol, self.In_Use)


class Language(models.Model):
    # Fields
    ID = models.IntegerField(primary_key = True)
    Name = models.CharField(max_length=255)
    Symbol = models.CharField(max_length=255, default="")
    In_Use = models.BooleanField(default=False)

       # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('User', args=[str(self.id)])

    @property
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return "id: {} Name: {} Symbol: {} In Use: {}".format(self.ID, self.Name, self.Symbol, self.In_Use)

                                       
class User(models.Model):
    # Fields
    ID = models.IntegerField(primary_key=True)
    Username = models.CharField(max_length=255, default="")
    Name = models.CharField(max_length=255)
    Lastname = models.CharField(max_length=255, default="")
    Mail = models.CharField(max_length=255, default="")
    Password = models.CharField(max_length=255, default="")
    Address = models.CharField(max_length=255, default="")
    isLogged = models.BooleanField(default=False)
    ID_Currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)
    ID_Language = models.ForeignKey(Language, on_delete=models.CASCADE, default=1)

       # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('User', args=[str(self.id)])

    @property
    def __str__(self):
        """
            String for representing the MyModelName object (in Admin site etc.)
        """
        return "id: {} Username: {} Name: {} Lastname: {} Mail: {} Password: {} Address: {} isLogged: {}".format(self.ID, self.Username, self.Name, self.Lastname, self.Mail, self.Password, self.Address, self.isLogged, self.ID_Currency, self.ID_Language)

class ShippingAddress(models.Model):
    # Fields
    ID = models.IntegerField(primary_key=True)
    Firstname = models.CharField(max_length=255, default="")
    Lastname = models.CharField(max_length=255, default="")
    Mail = models.CharField(max_length=255, default="")
    Company = models.CharField(max_length=255, default="")
    Street = models.CharField(max_length=255, default="")
    City = models.CharField(max_length=255, default="")
    Zip = models.CharField(max_length=255, default="")
    State = models.CharField(max_length=255, default="")
    Province = models.CharField(max_length=255, default="")
    Phone = models.CharField(max_length=255, default="")
    ID_User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
       # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('shipppingAddress', args=[str(self.id)])

    @property
    def __str__(self):
        """
            String for representing the MyModelName object (in Admin site etc.)
        """
        return "id: {} Firstname: {} Lastname: {} Company: {} Mail: {} Street: {} City: {} Zip: {} Province: {} State {} Phone: {}".format(self.ID, self.Firstname, self.Lastname, self.Company, self.Mail, self.Street, self.City, self.Zip, self.Province, self.State, self.Phone)


class Category(models.Model):
    # Fields
    ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=255)
       # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('Product', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return "id: " + str(self.ID) + " " + self.NameProduct + " " + str(self.Price) + " " + self.Desc + " " + str(self.Amount)


class Product(models.Model):
    # Fields
    objects = ObjectManager()
    ID = models.IntegerField(primary_key=True)
    NameProduct = models.CharField(max_length=255)
    Subtitle = models.CharField(max_length=255,default="")
    Price = models.DecimalField(max_digits=5, decimal_places=2)
    Desc = models.CharField(max_length=255)
    Info = models.CharField(max_length=255)
    Amount = models.IntegerField()
    Sale = models.DecimalField(max_digits=5, decimal_places=2)
    ID_Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    PictureProductName = models.CharField(max_length=255)

       # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('Product', args=[str(self.id)])

    def natural_key(self):
        tot = (self.Price*(100-self.Sale))/100
        return {'NameProduct': self.NameProduct, 'PictureProductName': self.PictureProductName, 'Price': self.Price, 'Sale': self.Sale, 'Tot': tot}

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return "id: " + str(self.ID) + " " + self.NameProduct + " " + str(self.Price) + " " + self.Desc + " " + str(self.Amount)


class Basket(models.Model):
    # Fields
    ID = models.IntegerField(primary_key = True)
    ID_User = models.ForeignKey(User, on_delete=models.CASCADE)
    ID_Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)

       # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('Basket', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return "id: {} User: {} Product: {} Quantity: {}".format(self.ID, self.ID_User, str(self.ID_Product), self.Quantity)
