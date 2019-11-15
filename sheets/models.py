from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class CardType(models.Model):

    COLORS = {
        'red': 'red',
        'pink': 'pink',
        'purple': 'purple',
        'indigo': 'indigo',
        'blue': 'blue',
        'cyan': 'cyan',
        'teal': 'teal',
        'lime': 'lime',
        'yellow': 'yellow',
        'amber': 'amber',
        'orange': 'orange',
        'brown': 'brown',
        'grey': 'grey',
    }

    name = models.CharField(max_length=50, null=False, blank=False)
    color = models.CharField(max_length=6, choices=COLORS, default='')
    is_archived = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name


class Card(models.Model):

    cardType = models.ForeignKey('CardType', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    created = models.DateTimeField(default=timezone.now)
    is_archived = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name


class Record(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    card = models.ManyToManyField(Card)
    date = models.DateTimeField(primary_key=True, default=timezone.now)
    content = models.TextField()
    score = models.SmallIntegerField()

    def __str__(self):
        return ('Record: {}'.format(self.date))


class Question(models.Model):

    TYPES = [
        ('STR', 'Text'),
        ('INT', 'Number'),
        ('LST', 'List'),
        ('BOL', 'Boolean'),
        ('TAG', 'Tag'),
    ]

    card = models.ForeignKey('Card', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(max_length=3, choices=TYPES, default='STR')

    def __str__(self):
        return self.name


class Answer(models.Model):

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    record = models.ForeignKey('Record', on_delete=models.CASCADE)


class AnswerStr(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = models.CharField(blank=True, max_length=1000)

    def __str__(self):
        return self.value[:50]


class AnswerInt(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.value)


class AnswerLst(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = ArrayField(models.CharField(max_length=50, blank=True))

    def __str__(self):
        return str(self.value)


class AnswerBol(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = models.BooleanField(default=False)

    def __str__(self):
        return str(self.value)


class Tag(models.Model):

    name = models.CharField(max_length=1000)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AnswerTag(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
