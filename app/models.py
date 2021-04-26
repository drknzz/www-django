from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

CATEGORY_CHOICES = (
    (0, 'procedure'),
    (1, 'property'),
    (2, 'lemma'),
    (3, 'assertion'),
    (4, 'invariant'),
    (5, 'precondition'),
    (6, 'postcondition'))

STATUS_CHOICES = (
    (0, 'proved'),
    (1, 'invalid'),
    (2, 'counterexample'),
    (3, 'unchecked'))


class User(models.Model):
    name = models.CharField(max_length=20, primary_key=True, unique=True)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    last_updated = models.DateTimeField(auto_now=True)
    validity = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Directory(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_directory = models.ForeignKey("Directory", on_delete=models.CASCADE, null=True, blank=True)
    availability = models.BooleanField(default=True)
    #path
    #level
    last_updated = models.DateTimeField(auto_now=True)
    validity = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=20, primary_key=True, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    directory = models.ForeignKey("Directory", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()
    availability = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    validity = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SectionCategory(models.Model):
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    last_updated = models.DateTimeField(auto_now=True)
    validity = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.category


class Status(models.Model):
    status = models.CharField(max_length=20,
    choices=STATUS_CHOICES)
    last_updated = models.DateTimeField(auto_now=True)
    validity = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.status


class StatusData(models.Model):
    status_data = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    validity = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.status_data


class FileSection(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    category = models.OneToOneField(SectionCategory, on_delete=models.CASCADE)
    status = models.OneToOneField(Status, on_delete=models.CASCADE)
    status_data = models.OneToOneField(StatusData, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    parent_section = models.ForeignKey("FileSection", on_delete=models.CASCADE, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    #sectbegin
    #sectend
    validity = models.BooleanField(default=True)

    def __str__(self):
        return self.name