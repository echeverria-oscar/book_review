from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def login(self, post):
        user_list = User.objects.filter(email = post['email'])
        if user_list:
            user = user_list[0]
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:

                return user
        return None

    def register(self, post):
        encrypted_password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        User.objects.create(name = post['name'], alias = post['alias'], email = post['email'], password = encrypted_password )

    def validate(self, post):
        errors = []

        if len(post['name']) == 0:
            errors.append("Name is required")

        if len(post['alias']) == 0:
            errors.append("alias is required")

        if len(post['email']) == 0:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(post['email']):
            errors.append("Please enter a valid email")

        if len(post['password']) == 0:
            errors.append("must enter a password")
        elif len(post['password']) < 8:
            errors.append("password must have at least 8 characters")
        elif post['password'] != post['confirm_pass']:
            errors.append("password and confirmation must match")

        if len(User.objects.filter(email = post['email'])) > 0 :
            errors.append("Email address is unavailable!")

        return errors

class AuthorManager(models.Manager):
    def create_author(self):
        return None


class BookManager(models.Manager):
    def create_book(self,):
        return None

class ReviewManager(models.Manager):
    def create_review(self):
        return None




class User(models.Model):
    name = models.CharField(max_length = 45)
    alias = models.CharField(max_length = 45)
    email = models.EmailField(max_length= 60)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    author = models.CharField(max_length = 50)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AuthorManager()

class Book(models.Model):
    book = models.CharField(max_length = 100)
    author = models.ForeignKey(Author)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()

class Review(models.Model):
    review = models.CharField(max_length = 255)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReviewManager()
