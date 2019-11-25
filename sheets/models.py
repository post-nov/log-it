from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class CardType(models.Model):

    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default='')
    is_archived = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name


class Card(models.Model):

    card_type = models.ForeignKey('CardType', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    created = models.DateTimeField(default=timezone.now)
    is_archived = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name


class Record(models.Model):

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

    def lst_answers(self):
        return AnswerLst.objects.get(answer=self).value

    def __str__(self):
        if self.question.type == 'STR':
            return AnswerStr.objects.get(answer=self).value
        elif self.question.type == 'INT':
            return str(AnswerInt.objects.get(answer=self).value)
        elif self.question.type == 'LST':
            elements = [f'{index}. {value}' for index, value in enumerate(
                AnswerLst.objects.get(answer=self).value, start=1)]
            return ', '.join(elements)
        elif self.question.type == 'TAG':
            tags = [str(t) for t in AnswerTag.objects.get(answer=self).tag.all()]
            return ', '.join(tags)
        elif self.question.type == 'BOL':
            if AnswerBol.objects.get(answer=self).value:
                return str(1)
            else:
                return str(0)
        else:
            return 'NOTHING'


class AnswerStr(models.Model):

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = models.CharField(blank=True, max_length=1000)

    def __str__(self):
        return self.value


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
