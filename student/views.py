from zhixuewang import login as zxw_login
from django.http import HttpResponse, HttpResponseBadRequest
import json


def basic_error(error: Exception, code: int, errMsg: str, target: object) -> HttpResponse:
    """
    抛出基本错误
    """
    result = {
        'Result': {
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
                'Code': 0,
                'Message': '操作成功完成'
            },
            'ID': stu.id,
            'Class':
            {
                'ID': stu.clazz.id,
                'Name': stu.clazz.name,
                'School':
                {
                    'ID': stu.clazz.school.id,
                    'Name': stu.clazz.school.name
                },
            },
            'Name': stu.name,
            'Gender': str(stu.gender)
        }
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
                'Code': 0,
                'Message': '操作成功完成'
            },
            'ID': original.id,
            'Name': original.name,
            'School':
            {
                'ID': original.school.id,
                'Name': original.school.name
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
                {'ID': i.id,
                 'Name': i.name,
                 'School': {
                     'ID': i.school.id,
                     'Name': i.school.name}}
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
                'ID': i.id,
                'Class': {
                    'ID': i.clazz.id,
                    'Name': i.clazz.name,
                    'School': {
                        'ID': i.clazz.school.id,
                        'Name': i.clazz.school.name
                    },
                },
                'Name': i.name,
                'Gender': str(i.gender)
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
            'ID': original.id,
            'Name': original.name,
            'Status': str(original.status),
            'GradeCode': str(original.grade_code),
            'IsFinal': str(original.is_final),
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
                'ID': i.id,
                'Name': i.name,
                'Status': str(i.status),
                'GradeCode': str(i.grade_code),
                'IsFinal': str(i.is_final),
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
                    "Score": i.score,
                    "Subject": {
                        "Name": i.subject.name,
                        "Code": i.subject.code,
                        "ID": i.subject.id,
                        "StandardScore": i.subject.standard_score
                    },
                    "ClassRank": i.class_rank,
                    "GradeRank": i.grade_rank,
                    "ExamRank": i.exam_rank
                }
            )
        result = {
            "Person": {
                "Name": original.person.name,
                "ID": original.person.id,
                "Class": {
                    "Name": original.person.clazz.name,
                    "ID": original.person.clazz.id,
                    "School": {
                        "Name": original.person.clazz.school.name,
                        "ID": original.person.clazz.school.id
                    }
                }
            },
            "Mark": mark
        }
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -7, '尝试获得自身成绩失败', stu)
