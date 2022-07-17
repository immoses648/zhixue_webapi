from zhixuewang import login as zxw_login
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
import json


def basic_error(error: Exception, code: int, err_msg: str, target: object) -> HttpResponse:
    """
    抛出基本错误
    """
    result = {
        'Status': {
            'Code': code,
            'Message': err_msg
        },
        'ErrorBody': {
            'Target': str(target),
            'Error': str(error)
        }
    }
    return HttpResponseBadRequest(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')


def status_ok(result):
    ret = {
        'Status': {
            'Code': 0,
            'Message': '成功'
        },
        'Result': result
    }
    return HttpResponse(json.dumps(ret, indent=2, ensure_ascii=False), content_type='application/json')


def stu_login(request):
    try:
        stu = None
        if request.GET.__contains__("usr") and request.GET.__contains__("pwd"):  # 旧版参数
            stu = zxw_login(request.GET.get('usr'), request.GET.get('pwd'))
        else:
            stu = zxw_login(request.GET.get('user'), request.GET.get('password'))
        return stu
    except Exception as err:
        return err


def web_student(request):
    stu = stu_login(request)
    try:
        result = {
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
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -1, '尝试登录学生账号失败', stu)


def web_get_clazz(request):
    stu = stu_login(request)
    get_clazz = request.GET.get('clazz')
    try:
        original = stu.get_clazz(get_clazz)
        result = {
            'ID': original.id,
            'Name': original.name,
            'School':
            {
                'ID': original.school.id,
                'Name': original.school.name
            }
        }
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -2, '尝试获得班级失败', stu)


def web_get_clazzs(request):
    stu = stu_login(request)
    try:
        original = stu.get_clazzs()
        result = []
        for i in original:
            result.append(
                {'ID': i.id,
                 'Name': i.name,
                 'School': {
                     'ID': i.school.id,
                     'Name': i.school.name}}
            )
        return status_ok(result)
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
        return status_ok(result)
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
            'IsFinal': original.is_final,
        }
        return status_ok(result)
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
                'IsFinal': i.is_final,
            })
        return status_ok(result)
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
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -7, '尝试获得考试原卷失败', stu)


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
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -7, '尝试获得自身成绩失败', stu)


def web_get_all_subjects(request: HttpRequest):
    stu = stu_login(request)
    param = request.GET["param"]
    original = None
    try:
        original = stu.get_subjects(param)  # 支持传入考试名或ID
    except Exception as err:
        return basic_error(err, -8, '尝试获得考试所有学科失败', stu)
    result = []
    for subj in original:
        result.append(
            {
                'SubjectName': subj.name,
                'SubjectId': subj.id,
                'SubjectCode': subj.code
            }
        )
    return status_ok(result)
