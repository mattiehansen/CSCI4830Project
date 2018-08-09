from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    """
    A User account that acts as base for Student and Teacher.
    Comes with username, password, email, first_name, and last_name fields.
    Attributes:
        is_student: True if account is a student one
        is_teacher: True if account is a teacher one
        pass_attempts: for student, number of passes attempted, whether accepted or rejected
        pass_rejections: for student, number of passes rejected
    """
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    pass_attempts = models.PositiveIntegerField(default=0)
    pass_rejections = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username


class Student(models.Model):
    """
    A Student account that has fields of CustomUser.

    Attributes:
        user: fields of CustomUser.
        classes_enrolled: Classes Student is enrolled in.
        accommodations: Student's accommodations.
        number_of_passes: Number of times passes total attempted by Student, whether accepted or rejected.
        number_of_rejections: Number of pass attempts that have been rejected by Teachers.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='student_profile')
    classes_enrolled = models.TextField()
    accommodations = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    number_of_passes = models.PositiveIntegerField(default=0)
    number_of_rejections = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def last_logged_in(self):
        return self.user.last_login

    def classes(self):
        return self.classes_enrolled

    def passes_attempted(self):
        return self.user.pass_attempts

    def passes_rejected(self):
        return self.user.pass_rejections


class Teacher(models.Model):
    """
    A Teacher account that has fields of CustomUser.

    Attributes:
        user: fields of CustomUser.
        classes_taught: Classes Teacher teaches.
        room_number: Room number of teacher's home room.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='teacher_profile')
    classes_taught = models.TextField()
    room_number = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def last_logged_in(self):
        return self.user.last_login

    def classes(self):
        return self.classes_taught


class Pass(models.Model):
    """
    A school pass.

    Attributes:
        student: Student that has "created" the pass
        teacher: Teacher that has signed the pass.
        description: Description of the pass Student has written.
        time_left: Date time when Teacher has approved of pass and sent Student off.
        time_returned: Date time when Teacher has signed pass and Student has returned.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.CharField(max_length=30)
    time_left = models.DateTimeField(default=datetime.now, blank=True)
    time_returned = models.DateTimeField(blank=True, null=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Student or Teacher user profile. Prints if created.
    Credit to Nipun Brahmbhatt:
    https://blog.botreetechnologies.com/supporting-multiple-roles-using-djangos-user-model-62afa9ce6f61
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return: none
    """
    print('****', created)
    if instance.is_student is True:
        Student.objects.get_or_create(user=instance)
        print('Student created')
    elif instance.is_teacher is True:
        Teacher.objects.get_or_create(user=instance)
        print('Teacher created')


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves a Student or Teacher user profile. Prints if saved.
    Credit to Nipun Brahmbhatt:
    https://blog.botreetechnologies.com/supporting-multiple-roles-using-djangos-user-model-62afa9ce6f61
    :param sender:
    :param instance:
    :param kwargs:
    :return: none
    """
    print('_-----')
    if instance.is_student is True:
        instance.student_profile.save()
        print('Student saved')
    elif instance.is_teacher is True:
        instance.teacher_profile.save()
        print('Teacher saved')



