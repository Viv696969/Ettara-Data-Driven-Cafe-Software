from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    email=models.CharField(max_length=200,blank=False,null=False)
    name=models.CharField(max_length=200,blank=False,null=False)
    age = models.CharField(max_length=5,blank=False,null=False) # Assuming age is stored as an integer
    mobile = models.CharField(max_length=15,blank=False,null=False)  # CharField with max length to accommodate various mobile number formats
    city = models.CharField(max_length=100,blank=False,null=False)  # CharField with max length for city names
    company = models.CharField(max_length=100,blank=True,null=True)  # CharField with max length for city names
    country = models.CharField(max_length=100,blank=False,null=False)  # CharField with max length for city names
    state = models.CharField(max_length=100,blank=False,null=False)  # CharField with max length for state names
    pin = models.CharField(max_length=10,blank=False,null=False)  # CharField with max length for pin codes
    address = models.TextField()  # TextField for a potentially long address
    user=models.OneToOneField(User,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.user.username
    
class SentimentAnalysis(models.Model):
    review=models.CharField(max_length=1000,blank=False,null=False)
    date_of_review=models.DateField()
    sentiment=models.CharField(max_length=100,blank=False,null=False)
    sentiment_score=models.CharField(max_length=100,blank=False,null=False)

    # @classmethod
    # def count_reviews(table):
    #     return table.objects.count()

    def __str__(self) -> str:
        return self.review[:200]
