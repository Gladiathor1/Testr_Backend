from django.utils.timezone import now
from authentication import models as user_model
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from versatileimagefield.fields import VersatileImageField, PPOIField

def get_upload_path(instance, filename):
    # model = instance.album.model.__class__._meta
    # name = model.verbose_name_plural.replace(' ', '_')
    # sub = instance.subject
    # times=instance.created
    fn = filename.split(".")
    return f'media/question_images/%s/%s.%s' % (str(instance.subject), instance.created,fn[1])


# class ImageAlbum(models.Model):
#     def default(self):
#         return self.images.filter(default=True).first()
#     def thumbnails(self):
#         return self.images.filter(width__lt=100, length_lt=100)


class Discipline(models.Model):
    title = models.CharField(blank=False, max_length=1000)
    created = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


class Subject(models.Model):
    title = models.CharField(blank=False, max_length=1000)
    created = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


class Paper(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    year = models.IntegerField()
    session = models.CharField(blank=True, max_length=50)
    code = models.CharField(unique=True, blank=False, max_length=254)
    title = models.CharField(blank=False, max_length=5000)
    created = models.DateTimeField(default=now)
    file_name = models.CharField(unique=True, blank=True, max_length=254, null=True)

    def __str__(self):
        return u"%s %s" % (self.title, self.code)


class Tag(models.Model):
    name = models.CharField(blank=False, max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    created = models.DateTimeField(default=now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'subject'], name='NSConstraint')
        ]

    def __str__(self):
        return self.name


class Question(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, blank=False, related_name='questions')
    name = models.TextField(blank=True)
    description = models.TextField(blank=False)
    answer = models.TextField(blank=False)
    difficulty = models.CharField(blank=False, max_length=50)
    created = models.DateTimeField(default=now)
    tag = models.ManyToManyField(Tag)
    type = models.CharField(blank=False, max_length=100)
    qimage = models.ManyToManyField('question.Image', related_name='mqimage', blank=True)
    aimage = models.ManyToManyField('question.Image', related_name='maimage', blank=True)
    author = models.ForeignKey(
        user_model.User,  # new
        on_delete=models.PROTECT,
        null=True, related_name='questionAuthor'
    )
    verify = models.TextField(default="In review")
    verifier = models.ForeignKey(
        user_model.User,  # new
        on_delete=models.PROTECT,
        null=True, related_name='questionVerifier',blank=True
    )

class Image(models.Model):
    # name = models.CharField(max_length=255, blank=True, null=True)
    image = VersatileImageField(
        'Image',
        upload_to=get_upload_path,
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()
    # image=models.ImageField(upload_to=get_upload_path)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    created = models.DateTimeField(default=now)
