from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
   title = models.CharField(max_length=100)
   content = models.TextField()
   date_posted = models.DateTimeField(default=timezone.now)
   # we need an author for each post i.e. the user that created the post
   # this user has a diff table so we'll import the user model
   # which is stored in django.contrib.... one to many one user to many posts
   # now the "Post" and "User" models will have a relationship
   # we'll use a foreign key here
   author = models.ForeignKey(User, on_delete=models.CASCADE) # cacade will delete posts if user is deleted
   # above statement's on delete means that after deletion of user what happens to its created posts

   def __str__(self):
       return self.title

class Stock_detail(models.Model):
    symbol=models.CharField(max_length=10)
    company=models.CharField(max_length=100,default=None)
    uname=models.CharField(max_length=100)

    def __str__(self):
        return self.symbol

