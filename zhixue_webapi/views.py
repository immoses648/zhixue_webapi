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


def status_ok(result: object) -> object:
    ret = {
        'status': {
            'code': 0,
            'message': '成功'
        },
        'result': result
    }
    return HttpResponse(json.dumps(ret, indent=2, ensure_ascii=False), content_type='application/json')


# 学生登录
def stu_login(request):
    if request.GET.__contains__("usr") and request.GET.__contains__("pwd"):  # 旧版参数
        stu = zxw_login(request.GET.get('usr'), request.GET.get('pwd'))
    else:
        stu = zxw_login(request.GET.get('user'), request.GET.get('password'))
    return stu


# 教师登录
def teacher_login(request):
    if request.GET.__contains__("usr") and request.GET.__contains__("pwd"):
        teacher = zxw_login(request.GET.get('usr'), request.GET.get('pwd'))
    else:
        teacher = zxw_login(request.GET.get('user'), request.GET.get('password'))
    return teacher


# 以下为学生接口
# 获取学生信息
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


# 获取学生班级信息
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


# 获取全年级全部班级
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


# 获取同学
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


# 获取考试信息
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


# 获取考试列表
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


# 获取学生成绩
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


# 获取考试科目
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
        result = []
        for i in original:
            result.append(
                {
                    'name': i.name,
                    'id': i.id,
                    'code': i.code
                }
            )
        return status_ok(result)
    except Exception as err:
        return basic_error(err, -9, '获取考试所有学科失败')


# 以下为教师端接口
# 获取考试信息
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


# 获取考试阅卷情况
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


# 获取参考班级
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


# 获取全部分数
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


# 获取考试额外数据
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
