from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


STATUS = ((0, "Private"), (1, "Public"))


class To_Do_List(models.Model):

    """
    Stores a single to do list related to :model:`auth.User`.
    """

    list_title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="to_do_list"
    )
    list_content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    complete = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.list_title} | written by: {self.author}"

    def save(self, *args, **kwargs):

        if not self.slug:
            unique_slug = slugify(self.list_title)
            counter = 1
            while To_Do_List.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slugify(self.list_title)}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class UserCharacter(models.Model):
    """
    Model which represents one Runscape character per user.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="character"
    )
    character_name = models.CharField(max_length=50, unique=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.character_name


class Skills(models.Model):
    """
    Models which represents all skills related to a character.
    """
    user_character = models.ForeignKey(
        UserCharacter,
        on_delete=models.CASCADE,
        related_name="skills"
    )
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    experience = models.BigIntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - Level: {self.level}"
