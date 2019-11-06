from django.utils import timezone
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView
from .forms import (
    NewSheetNameForm,
    NewSheetQuestionFormset,
    NewRecordDateForm,
    NewAnswerForm,
)
from django.forms import formset_factory

from .models import (
    Sheet,
    Question,
    Record,
    Answer,
    AnswerInt,
    AnswerStr,
    AnswerTag,
    Tag,
)


class SheetsView(ListView):
    template_name = 'browsing/sheets.html'
    context_object_name = 'sheets'

    def get_queryset(self):
        users_sheets = Sheet.objects.filter(user=self.request.user)
        return users_sheets


def sheet_new_view(request):

    if request.method == 'GET':
        formset_question = NewSheetQuestionFormset()

    elif request.method == 'POST':
        form_name = NewSheetNameForm(request.POST)
        formset_question = NewSheetQuestionFormset(request.POST)
        if form_name.is_valid() and formset_question.is_valid():

            name_of_sheet = form_name.cleaned_data['name']
            sheet = Sheet(name=name_of_sheet)
            sheet.user = request.user
            sheet.save()

            for form in formset_question:
                if form.cleaned_data.get('name'):

                    question = Question(sheet=sheet)
                    question.name = form.cleaned_data['name']
                    question.type = form.cleaned_data['type']
                    if form.cleaned_data['max_value']:
                        question.max_value = form.cleaned_data['max_value']
                    question.save()

            return redirect('sheets')

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(
                request,
                'addition/sheet_new.html',
                {
                    'form_name': NewSheetNameForm,
                    'formset_question': formset_question,
                })
    return render(
        request,
        'addition/sheet_new.html',
        {
            'form_name': NewSheetNameForm,
            'formset_question': formset_question,
        })


def sheet_details_view(request, sheet_name):
    template_name = 'browsing/sheet_details.html'

    sheet = get_object_or_404(Sheet, name=sheet_name, user=request.user)
    records = Record.objects.filter(sheet=sheet)
    questions = Question.objects.filter(sheet=sheet)
    records_answers = []
    for record in records:
        single_record_answers = []
        answers = Answer.objects.filter(record=record)
        for question, answer in zip(questions, answers):
            if question.type == 'STR':
                answer_str = AnswerStr.objects.get(answer=answer)
                single_record_answers.append(answer_str.value)
            elif question.type == 'INT':
                answer_int = AnswerInt.objects.get(answer=answer)
                single_record_answers.append(answer_int.value)
            elif question.type == 'TAG':
                answer_tag = AnswerTag.objects.get(answer=answer)
                tags_query = answer_tag.tag.all()
                tags = ", ".join([tag.name for tag in tags_query])
                single_record_answers.append(tags)
        records_answers.append((record, single_record_answers))

    context = {'sheet': sheet, 'questions': questions, 'records': records_answers}

    return render(request, template_name, context)


def sheet_delete_view(request, sheet_name):
    template_name = 'deletion/sheet_delete.html'

    sheet = Sheet.objects.get(name=sheet_name)
    number_of_records = len(Record.objects.filter(sheet=sheet))
    context = {'sheet': sheet, 'number_of_records': number_of_records}

    if request.method == 'POST':
        sheet.delete()
        return redirect('sheets')

    return render(request, template_name, context)


def record_new_view(request, sheet_name):

    template_name = 'addition/record_new.html'

    sheet = get_object_or_404(Sheet, name=sheet_name, user=request.user)
    questions = Question.objects.filter(sheet=sheet)

    if request.method == 'POST':
        form_date = NewRecordDateForm(request.POST)
        form_answers = []
        for index, question in enumerate(questions):
            form_answer = NewAnswerForm(
                data={'value': request.POST.getlist('value')[index]},
                label=question.name,
                type=question.type,
                max_value=question.max_value,
            )
            form_answers.append(form_answer)

        if form_date.is_valid() and all([form_answer.is_valid() for form_answer in form_answers]):
            date = form_date.cleaned_data['date']
            record = Record(date=date, sheet=sheet)
            record.save()

            for answer_value, question in zip(form_answers, questions):
                answer = Answer(question=question, record=record)
                answer.save()
                value = answer_value.cleaned_data['value']

                if question.type == 'STR':
                    answer_str = AnswerStr(answer=answer, value=value).save()

                elif question.type == 'INT':
                    answer_int = AnswerInt(answer=answer, value=value).save()

                elif question.type == 'TAG':
                    tags = [tag.lower() for tag in value.split(', ')]
                    answer_tag = AnswerTag(answer=answer)
                    answer_tag.save()
                    for tag_name in tags:
                        try:
                            tag = Tag.objects.get(name=tag_name)
                        except Tag.DoesNotExist:
                            tag = Tag(name=tag_name)
                            tag.save()
                        answer_tag.tag.add(tag)

        else:
            context = {
                'sheet': sheet,
                'form_answers': form_answers,
                'form_date': form_date,
            }
            return render(request, template_name, context)

        return redirect('sheet_details', sheet_name=sheet.name)

    elif request.method == 'GET':
        form_date = NewRecordDateForm()
        form_answers = []
        for question in questions:
            form_answer = NewAnswerForm(
                label=question.name,
            )
            form_answers.append(form_answer)

        context = {
            'sheet': sheet,
            'form_answers': form_answers,
            'form_date': form_date,
        }

        return render(request, template_name, context)


def record_delete_view(request, sheet_name, record_id):

    template_name = 'deletion/record_delete.html'

    sheet = get_object_or_404(Sheet, name=sheet_name, user=request.user)
    questions = Question.objects.filter(sheet=sheet)
    record = Record.objects.get(sheet=sheet, id=record_id)
    answers = Answer.objects.filter(record=record)

    questions_answers = []

    for question, answer in zip(questions, answers):
        if question.type == 'STR':
            answer_str = AnswerStr.objects.get(answer=answer)
            questions_answers.append((question, answer_str.value))
        elif question.type == 'INT':
            answer_int = AnswerInt.objects.get(answer=answer)
            questions_answers.append((question, answer_int.value))
        elif question.type == 'TAG':
            answer_tag = AnswerTag.objects.get(answer=answer)
            tags_query = answer_tag.tag.all()
            tags = ", ".join([tag.name for tag in tags_query])
            questions_answers.append((question, tags))

    context = {
        'sheet': sheet,
        'record': record,
        'questions_answers': questions_answers,
    }

    if request.method == 'POST':
        record.delete()
        return redirect('sheet_details', sheet_name=sheet_name)

    return render(request, template_name, context)
