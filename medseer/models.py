from django.db import models


class Journal(models.Model):
    name = models.CharField(max_length=200, unique=True)
    rank = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    rank = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Author(models.Model):
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True, unique=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('forename', 'surname'), name='unique_author_name'),
        ]


class Paper(models.Model):
    pdf = models.FileField(upload_to='pdfs/%Y/%m/%d/', null=True, unique=True)
    tei = models.FileField(upload_to='xmls/%Y/%m/%d/', null=True,  unique=True)
    title = models.TextField(null=True, blank=True, unique=True)
    abstract = models.TextField(null=True, blank=True, unique=True)
    doi = models.CharField(max_length=100, null=True, blank=True, unique=True)
    url = models.URLField(null=True, blank=True, unique=True)
    authors = models.ManyToManyField(Author)
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
