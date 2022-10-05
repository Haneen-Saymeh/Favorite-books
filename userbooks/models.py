from django.db import models


from django.db import models

from django.db import models
import re
import datetime


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
       
        if len(postData['firstName']) < 2:
            errors["firstName"] = "First name should be at least 2 characters"
        if len(postData['lastName']) < 2:
            errors["lastName"] = "Last name should be at least 2 characters"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
            
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['conpassword'] != postData['password']:
            errors['conpassword'] = "Passowrd should match!"
        return errors

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['title'] == "":
            errors["title"] = "Book's title  is required!"
       
        if len(postData['desc']) < 5:
            errors["desc"] = "Book's description should be at least 5 characters!"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 
    #uploaded_books
    #liked_books

class Book(models.Model):
    title = models.CharField(max_length=255)
    description=models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager() 
    




