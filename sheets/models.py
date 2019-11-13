from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator


class Sheet(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self): return self.name[:50]


class Question(models.Model):

    sheet = models.ForeignKey('Sheet', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)

    TEXT = 'STR'
    NUMBER = 'INT'
    TAG = 'TAG'
    AVAILABLE_TYPES = [
        (TEXT, 'Text'),
        (NUMBER, 'Number'),
        (TAG, 'Tag'),
    ]
    type = models.CharField(max_length=3, choices=AVAILABLE_TYPES, default=TEXT)

    max_value = models.SmallIntegerField(
        blank=True,
        # Apparently, it's mandatory to set default value for this type of fields
        default=0
    )

    def __str__(self): return self.name[:50]


class Record(models.Model):

    sheet = models.ForeignKey('Sheet', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class Answer(models.Model):

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    record = models.ForeignKey('Record', on_delete=models.CASCADE)


class AnswerInt(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.value)


class AnswerStr(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

    value = models.CharField(blank=True, max_length=1000)

    def __str__(self):
        return self.value[:50]


class Tag(models.Model):

    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class AnswerTag(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
