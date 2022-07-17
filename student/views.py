from zhixuewang import login as zxw_login
from django.http import HttpResponse
import json


def stu_login(request):
    try:
        stu = zxw_login(request.GET.get('usr'), request.GET.get('pwd'))
        return stu
    except Exception as e:
        return e


def web_student(request):
    stu = stu_login(request)
    try:
        result = {
            'id': stu.id,
            'class': {
                'id': stu.clazz.id,
                'name': stu.clazz.name,
                'school': {
                    'id': stu.clazz.school.id,
                    'name': stu.clazz.school.name
                },
            },
            'name': stu.name,
            'gender': str(stu.gender)
        }
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as err:
        return HttpResponse(json.dumps({'login_error': str(stu), 'run_error': str(err)}, indent=2, ensure_ascii=False))


def web_get_clazz(request):
    stu = stu_login(request)
    get_clazz = request.GET.get('clazz')
    try:
        original = stu.get_clazz(get_clazz)
        result = {'id': original.id,
                 'name': original.name,
                 'school': {
                     'id': original.school.id,
                     'name': original.school.name}}
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as err:
        return HttpResponse(json.dumps({'login_error': str(stu), 'run_error': str(err)}, indent=2, ensure_ascii=False))


def web_get_clazzs(request):
    stu = stu_login(request)
    try:
        original = stu.get_clazzs()
        result = []
        for i in original:
            result.append(
                {'id': i.id,
                 'name': i.name,
                 'school': {
                     'id': i.school.id,
                     'name': i.school.name}}
            )
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as err:
        return HttpResponse(json.dumps({'login_error': str(stu), 'run_error': str(err)}, indent=2, ensure_ascii=False))


def web_get_classmates(request):
    stu = stu_login(request)
    get_clazz = request.GET.get('clazz')
    try:
        original = stu.get_classmates(get_clazz)
        result = []
        for i in original:
            result.append({
                'id': i.id,
                'class': {
                    'id': i.clazz.id,
                    'name': i.clazz.name,
                    'school': {
                        'id': i.clazz.school.id,
                        'name': i.clazz.school.name
                    },
                },
                'name': i.name,
                'gender': str(i.gender)
            }
            )
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as err:
        return HttpResponse(json.dumps({'login_error': str(stu), 'run_error': str(err)}, indent=2, ensure_ascii=False))


def web_get_exam(request):
    stu = stu_login(request)
    get_exam_name = request.GET.get('exam')
    try:
        original = stu.get_exam(get_exam_name)
        result = {
            'id': original.id,
            'name': original.name,
            'status': str(original.status),
            'grade_code': str(original.grade_code),
            'is_final': str(original.is_final),
        }
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as err:
        return HttpResponse(json.dumps({'login_error': str(stu), 'run_error': str(err)}, indent=2, ensure_ascii=False))


def web_get_exams(request):
    stu = stu_login(request)
    try:
        original = stu.get_exams()
        result = []
        for i in original:
            result.append({
                'id': i.id,
                'name': i.name,
                'status': str(i.status),
                'grade_code': str(i.grade_code),
                'is_final': str(i.is_final),
            }
            )
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as err:
        return HttpResponse(json.dumps({'login_error': str(stu), 'run_error': str(err)}, indent=2, ensure_ascii=False))


def web_get_original(request):
    stu = stu_login(request)
    get_exam_name = request.GET.get('exam')
    get_subject = request.GET.get('subject')
    try:
        result = stu.get_original(get_exam_name, get_subject)
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as err:
        return HttpResponse(json.dumps({'login_error': str(stu), 'run_error': str(err)}, indent=2, ensure_ascii=False))


def web_get_self_mark(request):
    stu = stu_login(request)
    get_exam_name = request.GET.get('exam')
    try:
        original = stu.get_self_mark(get_exam_name)
        mark = []
        for i in original:
            mark.append(
                {
                    "score": i.score,
                    "subject": {
                        "name": i.subject.name,
                        "code": i.subject.code,
                        "id": i.subject.id,
                        "standard_score": i.subject.standard_score
                    },
                    "class_rank": i.class_rank,
                    "grade_rank": i.grade_rank,
                    "exam_rank": i.exam_rank
                }
            )
        result = {
            "person": {
                "name": original.person.name,
                "id": original.person.id,
                "class": {
                    "name": original.person.clazz.name,
                    "id": original.person.clazz.id,
                    "school": {
                        "name": original.person.clazz.school.name,
                        "id": original.person.clazz.school.id
                    }
                }
            },
            "mark": mark
        }
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as err:
        return HttpResponse(json.dumps({'login_error': str(stu), 'run_error': str(err)}, indent=2, ensure_ascii=False))
