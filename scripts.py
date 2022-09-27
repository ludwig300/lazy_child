import random

from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid
)

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_schoolkid(name_child):
    try:
        schoolkid = Schoolkid.objects.get(
            full_name=name_child
        )
    except MultipleObjectsReturned:
        return print('Найдено несколько совпадений')
    except ObjectDoesNotExist:
        return print('Ошибка. Вы не верно ввели ФИО')
    return schoolkid


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid):
    comments = Chastisement.objects.filter(schoolkid=schoolkid)
    comments.delete()


def create_commendation(schoolkid, subject_title):
    praises = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
    ]
    text = random.choice(praises)

    try:
        lesson = Lesson.objects.get(
            subject__title=subject_title,
            group_letter=schoolkid.group_letter,
            year_of_study=schoolkid.year_of_study
        )
    except ObjectDoesNotExist:
        return print('Ошибка в названии предмета')
    except MultipleObjectsReturned:
        lesson = Lesson.objects.filter(
            subject__title=subject_title,
            group_letter=schoolkid.group_letter,
            year_of_study=schoolkid.year_of_study
        ).order_by('date').first()

    Commendation.objects.create(
        text=text, created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
