import logging
import calendar
import datetime

from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import (
    NewRecord,
)
from .models import (
    Record
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
            form = NewRecord()
            context = {
                'form': form,
                'date': date,
            }
            return render(request, template_name, context)

        else:
            form = NewRecord(request.POST)
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
