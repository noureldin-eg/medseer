from bs4 import BeautifulSoup
from dateutil import parser
from django.core.validators import FileExtensionValidator
from django.db import IntegrityError, models


class Journal(models.Model):
    name = models.CharField(max_length=300, unique=True)
    rank = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=300, unique=True)
    rank = models.PositiveSmallIntegerField(default=0)
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
    published_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title or "<Untitled Paper>"

    def parse_tei(self):
        soup = BeautifulSoup(self.tei, 'xml')
        title_tag = soup.title
        while not title_tag.getText():
            title_tag = title_tag.find_next('title')
        self.title = title_tag.getText()
        self.abstract = soup.abstract.getText()
        # self.doi = soup.find('idno', type='DOI').getText()
        date_published_tag = soup.find('date', type='published')
        if date_published_tag:
            self.published_at = parser.parse(date_published_tag.get('when'))
        authors = []
        for author_tag in soup.find_all('author'):
            try:
                organization, created = Organization.objects.get_or_create(
                    name="; ".join(org.getText() for org in author_tag.find_all('orgName')))
                author, created = Author.objects.update_or_create(
                    forename=author_tag.forename.getText() if author_tag.forename else None,
                    surname=author_tag.surname.getText() if author_tag.surname else None,
                    defaults={
                        'email': author_tag.email.getText() if author_tag.email else None,
                        'organization': organization
                    }
                )
                authors.append(author)
            except IntegrityError:
                pass
        self.authors.set(authors)
        return self
