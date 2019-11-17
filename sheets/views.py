import logging
import calendar
import datetime

from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    NewRecordForm,
    NewCardTypeForm,
    NewCardForm,
    NewCardQuestionFormset
)
from .models import (
    Record,
    CardType,
    Card,
    Question,
)

logger = logging.Logger('ERROR')
calen = calendar.Calendar()


def overview(request):

    today = timezone.localdate()
    raw_days = list(calen.itermonthdays(today.year, today.month))

    days = [raw_days[i:i+7] for i in range(0, len(raw_days), 7)]
    template_name = 'browsing/overview.html'
    context = {
        'days': days,
        'month': today.month,
        'year': today.year,
    }

    return render(request, template_name, context)


def record_view(request, year, month, day):
    template_name = 'browsing/record.html'
    date = datetime.date(year, month, day)
    logging.error(date)

    if Record.objects.filter(date=date, user=request.user).exists():
        record = Record.objects.get(date=date, user=request.user)
        context = {
            'record': record,
            'date': date,
        }
        return render(request, template_name, context)

    else:
        if request.method == "GET":
            form = NewRecordForm()
            context = {
                'form': form,
                'date': date,
            }
            return render(request, template_name, context)

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
                context = {
                    'record': record,
                    'date': date,
                }
                return render(request, template_name, context)
            else:
                context = {
                    'form': form,
                    'date': date,
                }
                return render(request, template_name, context)


def cards_view(request):

    template_name = 'cards/overview.html'
    card_types = CardType.objects.filter(user=request.user)
    card_groups = []
    for card_type in card_types:
        card_groups.append({'type': card_type,
                            'cards': Card.objects.filter(card_type=card_type)})
    context = {'card_groups': card_groups}
    logging.error(context)
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
