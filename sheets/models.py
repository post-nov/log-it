from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class CardType(models.Model):

<<<<<<< HEAD
    name = models.CharField(max_length=50, null=False, blank=False)
    color = models.CharField(max_length=6, default='')
    is_archived = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name
=======
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
>>>>>>> 4534d1e6e4ffb229c7b32dca7e66d44ebe207036


<<<<<<< HEAD
class Card(models.Model):
=======
    def __str__(self): return self.name[:50]
>>>>>>> 4534d1e6e4ffb229c7b32dca7e66d44ebe207036

    cardType = models.ForeignKey('CardType', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    created = models.DateTimeField(default=timezone.now)
    is_archived = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name

<<<<<<< HEAD

class Record(models.Model):
=======
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
>>>>>>> 4534d1e6e4ffb229c7b32dca7e66d44ebe207036

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    card = models.ManyToManyField(Card)
    date = models.DateField(primary_key=True)
    content = models.TextField()

    AVAILABLE_SCORES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    score = models.SmallIntegerField(default=0, choices=AVAILABLE_SCORES)

<<<<<<< HEAD
    def __str__(self):
        return ('Record: {}'.format(self.date))
=======
    def __str__(self): return self.name[:50]
>>>>>>> 4534d1e6e4ffb229c7b32dca7e66d44ebe207036


class Question(models.Model):

    TYPES = [
        ('STR', 'Text'),
        ('INT', 'Number'),
        ('LST', 'List'),
        ('BOL', 'Boolean'),
        ('TAG', 'Tag'),
    ]

<<<<<<< HEAD
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(max_length=3, choices=TYPES, default='STR')

    def __str__(self):
        return self.name
=======
    sheet = models.ForeignKey('Sheet', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
>>>>>>> 4534d1e6e4ffb229c7b32dca7e66d44ebe207036


class Answer(models.Model):

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    record = models.ForeignKey('Record', on_delete=models.CASCADE)
<<<<<<< HEAD

=======
>>>>>>> 4534d1e6e4ffb229c7b32dca7e66d44ebe207036

class AnswerStr(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = models.CharField(blank=True, max_length=1000)

    def __str__(self):
        return self.value[:50]

<<<<<<< HEAD

class AnswerInt(models.Model):

=======
>>>>>>> 4534d1e6e4ffb229c7b32dca7e66d44ebe207036
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.value)


class AnswerLst(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
<<<<<<< HEAD
    value = ArrayField(models.CharField(max_length=50, blank=True))

    def __str__(self):
        return str(self.value)


class AnswerBol(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = models.BooleanField(default=False)
=======

    value = models.CharField(blank=True, max_length=1000)
>>>>>>> 4534d1e6e4ffb229c7b32dca7e66d44ebe207036

    def __str__(self):
        return str(self.value)


class Tag(models.Model):

    name = models.CharField(max_length=1000)
<<<<<<< HEAD
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
=======
>>>>>>> 4534d1e6e4ffb229c7b32dca7e66d44ebe207036

    def __str__(self):
        return self.name


class AnswerTag(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
