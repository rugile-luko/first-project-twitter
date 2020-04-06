from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    description = models.TextField(max_length=1000, null=True, blank=True, default="",
                                   help_text='The max length of your description is 1000 symbols.')
    followers = models.ManyToManyField(User, blank=True, symmetrical=False, related_name='user_followers')
    following = models.ManyToManyField(User, blank=True, symmetrical=False, related_name='user_following')

    def __str__(self):
        return self.user.username + ' ' + 'Profile'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



