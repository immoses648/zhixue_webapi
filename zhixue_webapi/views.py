from zhixuewang import login as zxw_login
from django.http import HttpResponse, HttpResponseBadRequest
import json
import re


def basic_error(error: Exception, code: int, err_msg: str) -> object:
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
    return HttpResponse(json.dumps(ret, indent=2, ensure_ascii=False))


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
    req_get_exam = request.GET.get('exam')
    if not req_get_exam:
        return basic_error(Exception("必传参数错误"), -9, '获取所有科目失败')
    try:
        original = stu.get_subjects(req_get_exam)  # 支持传入考试名或ID
        exam_id = stu.get_exam(req_get_exam).id
        result = []
        for i in original:
            r = stu._session.get("https://www.zhixue.com/zhixuebao/report/exam/getLevelTrend", params={
                "examId": exam_id,
                "pageIndex": "1",
                "pageSize": "5",
                "paperId": i.code
            }, headers=stu._get_auth_header())
            data = r.json()
            try:
                gradeCount = data["result"]["list"][1]["dataList"][0]["statTotalNum"]
            except:
                gradeCount = 0
            try:
                examCount = data["result"]["list"][2]["dataList"][0]["totalNum"]
            except:
                examCount = 0
            result.append(
                {
                    'name': i.name,
                    'id': i.id,
                    'code': i.code,
                    'standardScore': i.standard_score,
                    'classCount': data["result"]["list"][0]["dataList"][0]["statTotalNum"],
                    'gradeCount': gradeCount,
                    'examCount': examCount
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
        return basic_error(Exception("缺少必传参数"), -102, '获取考试阅卷情况失败')
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
        return basic_error(Exception("缺少必传参数"), -103, '获取参考班级失败')
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

# 获取原卷
def web_get_original_paper(request):
    teacher = teacher_login(request)
    stu_id = request.GET.get('stu')
    subject_id = request.GET.get('topic')
    if not subject_id or not stu_id:
        return basic_error(Exception("缺少必传参数"), -104, '获取原卷失败')
    try:
        data = teacher._session.get("https://www.zhixue.com/classreport/class/student/checksheet/", params={
            "userId": stu_id,
            "paperId": subject_id,
        })
        return HttpResponse(data.text.replace("//static.zhixue.com", "https://static.zhixue.com"))
    except Exception as err:
        return basic_error(err, -104, '获取原卷失败')


# 获取一个分数
def web_get_one_score(request):
    teacher = teacher_login(request)
    stu_id = request.GET.get('stu')
    subject_id = request.GET.get('topic')
    if not subject_id or not stu_id:
        return basic_error(Exception("缺少必传参数"), -105, '获取分数失败')
    try:
        data = json.loads(
            re.findall(r'var sheetDatas = (.*?);',
                       teacher._session.get("https://www.zhixue.com/classreport/class/student/checksheet/", params={
                           "userId": stu_id,
                           "paperId": subject_id
                       }).text)[0])["userAnswerRecordDTO"]["answerRecordDetails"]
        score = 0.0
        for i in data:
            score += i["score"]
        return status_ok(score)
    except Exception as err:
        return basic_error(err, -105, '获取分数失败')
