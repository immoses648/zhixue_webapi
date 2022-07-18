from zhixuewang import login as zxw_login
from django.http import HttpResponse, HttpResponseBadRequest
import json


def basic_error(error: Exception, code: int, err_msg: str) -> HttpResponse:
    """
    抛出基本错误
    """
    ret = {
        'status': {
            'code': code,
            'message': err_msg,
            'error': str(error)
        },
    }
    return HttpResponseBadRequest(json.dumps(ret, indent=2, ensure_ascii=False), content_type='application/json')


def status_ok(result):
    ret = {
        'status': {
            'code': 0,
            'message': '成功'
        },
        'result': result
    }
    return HttpResponse(json.dumps(ret, indent=2, ensure_ascii=False), content_type='application/json')


def stu_login(request):
    if request.GET.__contains__("usr") and request.GET.__contains__("pwd"):  # 旧版参数
        stu = zxw_login(request.GET.get('usr'), request.GET.get('pwd'))
    else:
        stu = zxw_login(request.GET.get('user'), request.GET.get('password'))
    return stu


def web_student(request):
    try:
        stu = stu_login(request)
    except Exception as err:
        return basic_error(err, -1, '登录学生账号失败')
    try:
        result = {
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
            'gender': str(stu.gender)
        }
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -2, '获取学生信息失败')


def web_get_clazz(request):
    try:
        stu = stu_login(request)
    except Exception as err:
        return basic_error(err, -1, '登录学生账号失败')
    get_clazz = request.GET.get('clazz')
    try:
        original = stu.get_clazz(get_clazz)
        result = {
            'id': original.id,
            'name': original.name,
            'school':
            {
                'id': original.school.id,
                'name': original.school.name
            }
        }
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -3, '获取班级失败')


def web_get_clazzs(request):
    try:
        stu = stu_login(request)
    except Exception as err:
        return basic_error(err, -1, '登录学生账号失败')
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
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -4, '获取所有班级失败')


def web_get_classmates(request):
    try:
        stu = stu_login(request)
    except Exception as err:
        return basic_error(err, -1, '登录学生账号失败')
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
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -5, '获取同学失败')


def web_get_exam(request):
    try:
        stu = stu_login(request)
    except Exception as err:
        return basic_error(err, -1, '登录学生账号失败')
    get_exam_name = request.GET.get('exam')
    try:
        original = stu.get_exam(get_exam_name)
        result = {
            'id': original.id,
            'name': original.name,
            'status': str(original.status),
            'gradeCode': str(original.grade_code),
            'isFinal': original.is_final,
        }
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -6, '获取考试失败')


def web_get_exams(request):
    try:
        stu = stu_login(request)
    except Exception as err:
        return basic_error(err, -1, '登录学生账号失败')
    try:
        original = stu.get_exams()
        result = []
        for i in original:
            result.append({
                'id': i.id,
                'name': i.name,
                'status': str(i.status),
                'gradeCode': str(i.grade_code),
                'isFinal': i.is_final,
            })
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -7, '获取所有考试失败')


# def web_get_original(request):
#     stu = stu_login(request)
#     get_exam_name = request.GET.get('exam')
#     get_subject = request.GET.get('subject')
#     try:
#         result = stu.get_original(get_exam_name, get_subject)
#         if len(result) == 0:
#             return basic_error(Exception("无法获取原卷"), -7, '尝试获得原始成绩失败', stu)
#         return status_ok(result)
#     except Exception as err:
#         return basic_error(err, -7, '尝试获得考试原卷失败', stu)


def web_get_self_mark(request):
    try:
        stu = stu_login(request)
    except Exception as err:
        return basic_error(err, -1, '登录学生账号失败')
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
                        "standardScore": i.subject.standard_score
                    },
                    "classRank": i.class_rank,
                    "gradeRank": i.grade_rank,
                    "examRank": i.exam_rank
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
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -8, '获取自身成绩失败')


def web_get_all_subjects(request):
    try:
        stu = stu_login(request)
    except Exception as err:
        return basic_error(err, -1, '登录学生账号失败')
    get_exam = request.GET.get('exam')
    if not get_exam:
        return basic_error(Exception("必传参数错误"), -9, '获取所有科目失败')
    try:
        original = stu.get_subjects(get_exam)  # 支持传入考试名或ID
    except Exception as err:
        return basic_error(err, -9, '获取考试所有学科失败')
    result = []
    for subj in original:
        result.append(
            {
                'name': subj.name,
                'id': subj.id,
                'code': subj.code
            }
        )
    return status_ok(result)
