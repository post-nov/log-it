import logging
import calendar
import datetime

from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import (
    NewRecordForm,
    NewCardTypeForm,
    NewCardForm,
    NewCardQuestionFormset,

    AnswerStrForm,
    AnswerIntForm,
    AnswerLstForm,
    AnswerBolForm,
    AnswerTagForm,
)
from .models import (
    Record,
    CardType,
    Card,
    Question,
    Answer,
    AnswerStr,
    AnswerInt,
    AnswerLst,
    AnswerBol,
    AnswerTag,
    Tag,
)

logger = logging.getLogger(__name__)
calen = calendar.Calendar()


def overview(request):

    today = timezone.localdate()
    raw_days = list(calen.itermonthdays(today.year, today.month))

    records = Record.objects.filter(date__year=today.year, date__month=today.month)

    def create_filled_calendar(days, records):
        days_by_weeks = [raw_days[i:i+7] for i in range(0, len(raw_days), 7)]
        days = []
        for week in days_by_weeks:
            filled_week = []
            for day in week:
                if day in [record.date.day for record in records]:
                    record = records.get(date__day=day)
                    cards = ', '.join(
                        [str(rec) for rec in record.card.all()]
                    ) if record.card.exists() else None
                    filled_week.append({'num': day,
                                        'score': record.score,
                                        'cards': cards})
                else:
                    filled_week.append({'num': day, 'score': None, 'cards': None})
            days.append(filled_week)
        logger.error(days)
        return days

    template_name = 'browsing/overview.html'
    context = {
        'days': create_filled_calendar(raw_days, records),
        'month': today.month,
        'year': today.year,
    }
    return render(request, template_name, context)


def record_view(request, year, month, day):
    template_name = 'browsing/record.html'
    date = datetime.date(year, month, day)

    def cards_to_choose_from(record_cards_queryset=None):
        "Выдает словарь типа CARD_TYPE:CARDS для формочки в самом низу"
        card_types = CardType.objects.filter(user=request.user)
        card_groups = {}
        for card_type in card_types:
            cards = Card.objects.filter(card_type=card_type)
            if record_cards_queryset:
                for index, card in enumerate(cards):
                    if card in record_cards_queryset:
                        cards = cards.exclude(id=card.id)
            if cards:
                card_groups[card_type.name] = cards
        logging.error(card_groups)
        return card_groups

    # Если запись уже имеется
    if Record.objects.filter(date=date, user=request.user).exists():
        # Пользователь выбрал, какую карточку добавить
        if request.method == 'POST':
            # На самом деле POST здесь не нужен, но не получается совместить данные
            # из optgroup с названием карточки через GET
            target_card_type, target_card = request.POST['card'].split('---|||---')
            return redirect('record_card',
                            year=year,
                            month=month,
                            day=day,
                            card_type_name=target_card_type,
                            card_name=target_card)

        # Пользователь просто смотрит на свою запись
        else:
            record = Record.objects.get(date=date, user=request.user)

            record_cards_queryset = record.card.all()

            # Заполненные карточки
            record_cards = []
            for card in record_cards_queryset:
                questions = Question.objects.filter(card=card)
                answers = Answer.objects.filter(question__in=questions, record=record)
                record_cards.append({
                    'card_name': card.name,
                    'card_color': card.card_type.color,
                    'card_type_name': card.card_type.name,
                    'card_qa': zip(questions, answers),
                })
                logging.error(f'{list(zip(questions, answers))}')

            card_groups = cards_to_choose_from(record_cards_queryset)

            context = {
                'record': record,
                'card_groups': card_groups,
                'record_cards': record_cards,
            }
            return render(request, template_name, context)

    # Пользователь впервые открыл данную дату
    else:
        if request.method == "GET":
            form = NewRecordForm()
            context = {
                'form': form,
                'date': date,
            }
            return render(request, template_name, context)

        # Пользователь заполнил форму, переправляем его на полноценный вью
        else:
            form = NewRecordForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                score = form.cleaned_data['score']
                record = Record(user=request.user,
                                date=date,
                                content=content,
                                score=score)
                record.save()

                # Еще ни одна карточка гарантированно не заполнена, поэтому
                # достаточно добавить только ссылки на карточки
                card_groups = cards_to_choose_from()

                context = {
                    'record': record,
                    'date': date,
                    'card_groups': card_groups,
                }
                return render(request, template_name, context)
            else:
                context = {
                    'form': form,
                    'date': date,
                }
                return render(request, template_name, context)


def record_card_view(request, year, month, day, card_type_name, card_name):
    template_name = 'browsing/record_card.html'
    date = datetime.date(year, month, day)
    record = Record.objects.get(date=date)
    card_type = CardType.objects.get(user=request.user, name=card_type_name)
    card = Card.objects.get(card_type=card_type, name=card_name)
    questions = Question.objects.filter(card=card)

    def create_forms(questions, data=None):
        questions_forms = []
        for index, question in enumerate(questions):
            if question.type == 'STR':
                if data:
                    pair = (question, (AnswerStrForm(data={'value': data[index]})))
                else:
                    pair = (question, (AnswerStrForm()))
                questions_forms.append(pair)
            elif question.type == 'INT':
                if data:
                    pair = (question, (AnswerIntForm(data={'value': data[index]})))
                else:
                    pair = (question, (AnswerIntForm()))
                questions_forms.append(pair)
            elif question.type == 'LST':
                if data:
                    pair = (question, (AnswerLstForm(data={'value': data[index]})))
                else:
                    pair = (question, (AnswerLstForm()))
                questions_forms.append(pair)
            elif question.type == 'BOL':
                if data:
                    pair = (question, (AnswerBolForm(data={'value': data[index]})))
                else:
                    pair = (question, (AnswerBolForm()))
                questions_forms.append(pair)
            elif question.type == 'TAG':
                if data:
                    pair = (question, (AnswerTagForm(data={'value': data[index]})))
                else:
                    pair = (question, (AnswerTagForm()))
                questions_forms.append(pair)
        return questions_forms

    if request.method == 'POST':
        questions_forms = create_forms(questions, request.POST.getlist('value'))
        logger.error(request.POST.getlist('value'))

        if all([question_form[1].is_valid() for question_form in questions_forms]):
            for question, form in questions_forms:
                logger.error(f"{question.name} - {question.type} : {form.cleaned_data['value']}")
                answer = Answer(record=record, question=question)
                answer.save()
                value = form.cleaned_data['value']
                if question.type == 'STR':
                    answer_str = AnswerStr(answer=answer, value=value)
                    answer_str.save()
                elif question.type == 'INT':
                    answer_int = AnswerInt(answer=answer, value=value)
                    answer_int.save()
                elif question.type == 'LST':
                    value = value.split('\n')
                    answer_lst = AnswerLst(answer=answer, value=value)
                    answer_lst.save()
                elif question.type == 'BOL':
                    answer_bol = AnswerBol(answer=answer, value=bool(int(value)))
                    answer_bol.save()
                elif question.type == 'TAG':
                    tags = [tag for tag in value.split(', ')]
                    answer_tag = AnswerTag(answer=answer)
                    answer_tag.save()
                    for tag_name in tags:
                        try:
                            tag = Tag.objects.get(name=tag_name, question=question)
                        except ObjectDoesNotExist:
                            tag = Tag(name=tag_name, question=question)
                            tag.save()
                        answer_tag.tag.add(tag)
                record.card.add(card)
            return redirect('record', year=year, month=month, day=day)

        else:
            for error in [question_form[1].errors for question_form in questions_forms]:
                logger.error(error)
                messages.error(request, error)
            context = {'card': card,
                       'questions_forms': questions_forms}
            return render(request, template_name, context)
    else:
        questions_forms = create_forms(questions)
        logger.error(questions_forms[0][1].is_bound)
        context = {'card': card,
                   'questions_forms': questions_forms}
        return render(request, template_name, context)


def record_card_delete_view(request, year, month, day, card_type_name, card_name):
    template_name = 'browsing/record_card_delete.html'
    date = datetime.date(year, month, day)
    record = Record.objects.get(date=date)
    card_type = CardType.objects.get(user=request.user, name=card_type_name)
    card = Card.objects.get(card_type=card_type, name=card_name)

    questions = Question.objects.filter(card=card)
    answers = Answer.objects.filter(question__in=questions, record=record)
    {
        'card_name': card.name,
        'card_color': card.card_type.color,
        'card_qa': zip(questions, answers),
    }

    if request.method == 'POST':
        answers.delete()
        record.card.remove(card)
        return redirect('record', year=year, month=month, day=day)

    else:
        context = {'record': record,
                   'card_name': card.name,
                   'card_color': card.card_type.color,
                   'card_qa': zip(questions, answers)}
        return render(request, template_name, context)


def cards_view(request):

    template_name = 'cards/overview.html'
    card_types = CardType.objects.filter(user=request.user)
    card_groups = []
    for card_type in card_types:
        card_groups.append({'type': card_type,
                            'cards': Card.objects.filter(card_type=card_type)})
    context = {'card_groups': card_groups}
    logger.error(context)
    return render(request, template_name, context)


def new_card_type_view(request):

    template_name = 'cards/new_card_type.html'
    AVAILABLE_COLORS = ['red', 'pink', 'purple', 'deep-purple', 'indigo',
                        'blue', 'light-blue', 'cyan', 'teal', 'green',
                        'light-green', 'lime', 'yellow', 'amber', 'orange',
                        'deep-orange', 'brown', 'grey', 'blue-grey']
    if request.method == 'POST':
        form = NewCardTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            color = form.cleaned_data['color']
            card_type = CardType(name=name, color=color, user=request.user)
            card_type.save()
            return redirect('cards')
        else:
            for error in form.errors:
                messages.error(request, "{}:{}".format(error, form.errors[error]))
            context = {'form': form,
                       'colors': AVAILABLE_COLORS}
            return render(request, template_name, context)

    else:
        form = NewCardTypeForm()
        context = {'form': form,
                   'colors': AVAILABLE_COLORS}
        return render(request, template_name, context)


def new_card_view(request, card_type):
    template_name = 'cards/new_card.html'

    if request.method == 'POST':
        form_card = NewCardForm(request.POST)
        formset = NewCardQuestionFormset(request.POST)
        formset[0].empty_permitted = True
        if form_card.is_valid() and formset.is_valid():
            type = CardType.objects.get(name=card_type)
            card = Card(name=form_card.cleaned_data['name'],
                        card_type=type)
            card.save()
            for form in formset:
                if form.cleaned_data.get('name'):
                    question = Question(name=form.cleaned_data['name'],
                                        type=form.cleaned_data['type'],
                                        card=card)
                    question.save()
            return redirect('cards')

    else:
        form_card = NewCardForm()
        formset = NewCardQuestionFormset()
        formset[0].empty_permitted = True
        context = {'card_type': card_type,
                   'form_card': form_card,
                   'formset': formset}
        return render(request, template_name, context)
