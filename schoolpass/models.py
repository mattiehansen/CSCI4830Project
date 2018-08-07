from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    classes = models.TextField(blank=True)

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='student_profile')
    accommodations = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    number_of_passes = models.PositiveIntegerField(default=0)
    number_of_rejections = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def last_logged_in(self):
        return self.user.last_login

    def classes(self):
        return self.user.classes

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='teacher_profile')
    room_number = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def last_logged_in(self):
        return self.user.last_login

    def classes(self):
        return self.user.classes

class Pass(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    time_left = models.DateTimeField(default=datetime.now, blank=True)
    time_returned = models.DateTimeField(blank=True)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    print('****', created)
    if instance.is_student is True:
        Student.objects.get_or_create(user=instance)
    else:
        Teacher.objects.get_or_create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    print('_-----')
    if instance.is_student is True:
        instance.student_profile.save()
    else:
        Teacher.objects.get_or_create(user=instance)


