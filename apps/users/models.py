from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse
from django.template.defaultfilters import slugify
from .managers import MyAccountManager
import hashlib

class Account(AbstractBaseUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, default='male', max_length=10)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def get_avatar(self):
        email = self.email
        email_hash = hashlib.md5(email.encode()).hexdigest()
        root_url = 'https://www.gravatar.com/avatar/'
        default = 'patlys.co.ke/static/img/ke.png'
        avatar = f"{root_url}{email_hash}?d={default}"
        return avatar
    
    @property
    def get_short_name(self):
        return self.name if self.name else self.email.split('@')[0]
    
class Event(models.Model):
    EVENT_TYPES = (
        ('Everyone', 'Everyone'),
        ('Adults', 'Adults'),
        ('Children', 'Children'),
    )
    EVENT_STATUSES = (
        ('Confirmed', 'Confirmed'),
        ('Pending', 'Pending'),
        ('Children', 'Children'),
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="events/")
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES, default="Everyone")
    details = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    ticket_price = models.IntegerField()
    speaker = models.ForeignKey('users.Speaker', on_delete=models.CASCADE)
    venue = models.ForeignKey('users.Venue', on_delete=models.SET_NULL, null=True, blank=True)
    total_seats = models.IntegerField()
    total_views = models.IntegerField(default=1)
    event_status = models.CharField(max_length=10, choices=EVENT_STATUSES, default="Confirmed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:event", kwargs={
            'slug': self.slug
        })

    def get_update_url(self):
        return reverse("users:update-event", kwargs={
            'slug': self.slug
        })

    def get_delete_url(self):
        return reverse("users:delete-event", kwargs={
            'slug': self.slug
        })
    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    quantity = models.IntegerField(Account, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_short_name} - {self.event.title}"
    
class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(Account, default=5)
    details = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_short_name} - {self.event.title} ({self.rating}/5)"
      
class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    details = models.TextField(null=True)
    image = models.ImageField(upload_to="venues/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Forum(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    details = models.TextField(null=True)
    image = models.ImageField(upload_to="forums/", null=True)
    total_views = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:forum", kwargs={
            'slug': self.slug
        })
    
class ForumComment(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    details = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_short_name} - {self.forum.name}"
    
class Speaker(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ( 'Female','Female'),
        ('Other', 'Other')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    bio = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    career = models.CharField(max_length=50, default='Speaker')
    gender = models.CharField(max_length=6, null=True, blank=True, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to="speakers/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Attendant(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_short_name} - {self.event.title}"