from zhixuewang import login as zxw_login
from django.http import HttpResponse, HttpResponseBadRequest
import json


def basic_error(error: Exception, code: int, errMsg: str, target: object) -> HttpResponse:
    """
    抛出基本错误
    """
    result = \
    {
        'Result':
        {
            'Code': code,
            'Message': errMsg
        },
        'ErrorBody':
        {
            'Target': str(target),
            'Error': str(error)
        }
    }
    return HttpResponseBadRequest(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')


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
            'Result': {
                'code': 0,
                'status': 'OK',
                'message': '操作成功完成'
            },
            'id': stu.id,
            'class':
            {
                'id': stu.clazz.id,
                'name': stu.clazz.name,
                'school':
                {
                    'id': stu.clazz.school.id,
                    'name': stu.clazz.school.name
                },
            },
            'name': stu.name,
            'gender': str(stu.gender)}
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -1, '尝试登录学生账号失败', stu)


def web_get_clazz(request):
    stu = stu_login(request)
    get_clazz = request.GET.get('clazz')
    try:
        original = stu.get_clazz(get_clazz)
        result = {
            'Result': {
                'code': 0,
                'status': 'OK',
                'message': '操作成功完成'
            },
            'id': original.id,
            'name': original.name,
            'school':
            {
                'id': original.school.id,
                'name': original.school.name
            }
        }
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -2, '尝试获得班级失败', stu)


def web_get_clazzs(request):
    stu = stu_login(request)
    try:
        original = stu.get_clazzs()
        classes = []
        for i in original:
            classes.append(
                {'id': i.id,
                 'name': i.name,
                 'school': {
                     'id': i.school.id,
                     'name': i.school.name}}
            )
        return HttpResponse(json.dumps(classes, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -3, '尝试获得所有班级失败', stu)


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
            })
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -4, '尝试获得同学失败', stu)


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
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -5, '尝试获得考试失败', stu)


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
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -6, '尝试获得所有考试失败', stu)


def web_get_original(request):
    stu = stu_login(request)
    get_exam_name = request.GET.get('exam')
    get_subject = request.GET.get('subject')
    try:
        result = stu.get_original(get_exam_name, get_subject)
        if len(result) == 0:
            return basic_error(Exception("无法获取原卷"), -7, '尝试获得原始成绩失败', stu)
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -7, '尝试获得考试原卷失败', stu)


# def web_get_original(request):
#     stu = stu_login(request)
#     get_exam_name = request.GET.get('exam')
#     get_subject = request.GET.get('subject')
#     try:
#         result = stu.get_original(get_exam_name, get_subject)
#         return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False))
#     except Exception as err:
#         return HttpResponseBadRequest(json.dumps({'login_error': str(stu), 'run_error': str(err)}, indent=2, ensure_ascii=False))


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
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -7, '尝试获得自身成绩失败', stu)
