from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = ((0, "Private"), (1, "Public"))

class To_Do_List(models.Model):

    """
    Stores a single to do list related to :model:`auth.User`.
    """

    list_title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_do_list")
    list_content = TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    approved = models.BooleanField(default=False)
