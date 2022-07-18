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


def teacher_login(request):
    if request.GET.__contains__("usr") and request.GET.__contains__("pwd"):
        teacher = zxw_login(request.GET.get('usr'), request.GET.get('pwd'))
    else:
        teacher = zxw_login(request.GET.get('user'), request.GET.get('password'))
    return teacher


def web_get_exam_detail(request):
    try:
        teacher = teacher_login(request)
    except Exception as err:
        return basic_error(err, -100, '登录教师账号失败')
    exam_id = request.GET.get('exam')
    try:
        original = teacher.get_exam_detail(exam_id)
        result = {
            'id': original.id,
            'name': original.name,
            'status': str(original.status),
            'gradeCode': original.grade_code,
            'isFinal': original.is_final,
        }
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -101, '获取考试信息失败')


def web_get_marking_progress(request):
    try:
        teacher = teacher_login(request)
    except Exception as err:
        return basic_error(err, -100, '登录教师账号失败')
    subject_id = request.GET.get('subject')
    school_id = request.GET.get('school')
    if not subject_id or not school_id:
        return basic_error(Exception("缺少必传参数"), -105, '获取考试阅卷情况失败')
    try:
        original = teacher.get_marking_progress(subject_id, school_id)
        result = []
        for i in original:
            teachers_ls = []
            for j in i.teachers:
                teachers_ls.append({
                    'teacherName': j.teacher_name,
                    'school': {
                        'id': j.school.id,
                        'name': j.school.name
                    },
                    "isOnline": j.is_online,
                    "teacherCode": j.teacher_code,
                    "completeCount": j.complete_count,
                    "uncompleteCount": j.uncomplete_count,
                })
            result.append({
                'dispTitle': i.disp_title,
                'topicNumber': i.topic_number,
                'completePrecent': i.complete_precent,
                'subjectID': i.subject_id,
                'teachers': teachers_ls,
            })
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -102, '获取考试阅卷情况失败')


def web_get_school_exam_classes(request):
    teacher = teacher_login(request)
    school_id = request.GET.get('school')
    subject_id = request.GET.get('topic')
    if not school_id or not subject_id:
        return basic_error(Exception("缺少必传参数"), -105, '获取参考班级失败')
    try:
        original = teacher.get_school_exam_classes(school_id, subject_id)
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
        return basic_error(err, -103, '获取参考班级失败')


def web_get_scores(request):
    teacher = teacher_login(request)
    exam_id = request.GET.get('exam')
    if not exam_id:
        return basic_error(Exception("缺少必传参数"), -105, '获取考试成绩失败')
    try:
        original = teacher.get_scores(exam_id)
        result = []
        for i in original:
            stu_scores = []
            for j in i:
                stu_scores.append({
                    "score": j.score,
                    "subject": {
                        "name": j.subject.name,
                        "code": j.subject.code,
                        "id": j.subject.id,
                        "standardScore": j.subject.standard_score,

                    },
                    "person": {
                        "id": j.person.id,
                        "class": {
                            "id": j.person.clazz.id,
                            "name": j.person.clazz.name,
                            "school": {
                                "id": j.person.clazz.school.id,
                                "name": j.person.clazz.school.name
                            }
                        },
                        "name": j.person.name,
                        "gender": str(j.person.gender)
                    },
                    "classRank": j.class_rank,
                    "gradeRank": j.grade_rank,
                    "examRank": j.exam_rank,
                })
            result.append(stu_scores)
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -104, '获取考试成绩失败')


def web_get_exam_extra_data(request):
    teacher = teacher_login(request)
    exam_id = request.GET.get('exam')
    if not exam_id:
        return basic_error(Exception("缺少必传参数"), -105, '获取考试额外数据失败')
    try:
        original = teacher.get_exam_extra_data(teacher.get_scores(exam_id))
        result = []
        for i in original:
            class_data = []
            school_data = []
            for j in i.class_extra_data:
                class_data.append({
                    "avgScore": j.avg_score,
                    "mediumScore": j.medium_score,
                    "passRate": j.pass_rate,
                    "excellentRate": j.excellent_rate,
                    "perfectRate": j.perfect_rate,
                    "var": j.var,
                    "classID": j.class_id,
                    "className": j.class_name,
                })
            for k in i.school_extra_data:
                school_data.append({
                    "avgScore": k.avg_score,
                    "mediumScore": k.medium_score,
                    "passRate": k.pass_rate,
                    "excellentRate": k.excellent_rate,
                    "perfectRate": k.perfect_rate,
                    "var": k.var,
                    "schoolID": k.school_id,
                    "schoolName": k.school_name,
                })
            result.append({
                "subject": {
                    "name": i.subject.name,
                    "code": i.subject.code,
                    "id": i.subject.id,
                    "standardScore": i.subject.standard_score,
                },
                "classExtraData": class_data,
                "schoolExtraData": school_data,
                "examExtraData": {
                    "avgScore": i.exam_extra_data.avg_score,
                    "mediumScore": i.exam_extra_data.medium_score,
                    "passRate": i.exam_extra_data.pass_rate,
                    "excellentRate": i.exam_extra_data.excellent_rate,
                    "perfectRate": i.exam_extra_data.perfect_rate,
                    "var": i.exam_extra_data.var,
                },
            })
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -104, '获取考试额外数据失败')
