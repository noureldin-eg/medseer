from django.core.validators import FileExtensionValidator
from django.db import models


class Journal(models.Model):
    name = models.CharField(max_length=200, unique=True)
    rank = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    rank = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True, unique=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.forename} {self.surname}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('forename', 'surname'), name='unique_author_name'),
        ]


class Paper(models.Model):
    pdf = models.FileField(upload_to='pdfs/%Y/%m/%d/', blank=True,
                           help_text="Upload *.pdf file and Save to generate .tie.xml using Grobid",
                           validators=[FileExtensionValidator(['pdf'])])
    tei = models.FileField(upload_to='xmls/%Y/%m/%d/', blank=True,
                           help_text="Upload *.tie.xml file and Save to autofill paper data",
                           validators=[FileExtensionValidator(['xml'])])
    title = models.CharField(max_length=500, null=True,
                             blank=True, unique=True)
    abstract = models.TextField(blank=True)
    doi = models.CharField(max_length=100, null=True, blank=True, unique=True)
    url = models.URLField(null=True, blank=True, unique=True)
    authors = models.ManyToManyField(Author, blank=True)
    journal = models.ForeignKey(
        Journal, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "<Untitled Paper>"
