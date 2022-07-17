from zhixuewang import login as zxw_login
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest, Http404
import json
from nanoid import generate
import os


def basic_error(error: Exception, code: int, errMsg: str, target: object) -> HttpResponse:
    '''
    抛出基本错误
    '''
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


def teacher_login(request):
    try:
        teacher = zxw_login(request.GET.get('user'), request.GET.get('password'))
        return teacher
    except Exception as e:
        return e


def web_get_exam_detail(request):
    teacher = teacher_login(request)
    exam_id = request.GET.get('exam')
    try:
        original = teacher.get_exam_detail(exam_id)
        result = {
            'id': original.id,
            'name': original.name,
            'status': str(original.status),
            'grade_code': original.grade_code,
            'is_final': original.is_final,
        }
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -8, '教师尝试获取考试信息时发生了错误', str(teacher))


def web_get_marking_progress(request):
    teacher = teacher_login(request)
    subject_id = request.GET.get('subject')
    school_id = request.GET.get('school')
    try:
        original = teacher.get_marking_progress(subject_id, school_id)
        result = []
        for i in original:
            teachers_ls = []
            for j in i.teachers:
                teachers_ls.append({
                    'teacher_name': j.teacher_name,
                    'school': {
                        'id': j.school.id,
                        'name': j.school.name
                    },
                    "is_online": j.is_online,
                    "teacher_code": j.teacher_code,
                    "complete_count": j.complete_count,
                    "uncomplete_count": j.uncomplete_count,
                })
            result.append({
                'disp_title': i.disp_title,
                'topic_number': i.topic_number,
                'complete_precent': i.complete_precent,
                'subject_id': i.subject_id,
                'teachers': teachers_ls,
                'lete_count': i.lete_count,
                'uncomplete_count': i.uncomplete_count,
            })
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -9, '尝试获取教师批改进度时发生错误', str(teacher))


def web_get_school_exam_classes(request):
    teacher = teacher_login(request)
    school_id = request.GET.get('school')
    subject_id = request.GET.get('topic')
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
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -10, '尝试获得学校所有考试班级时发生错误', str(teacher))


def web_get_scores(request):
    teacher = teacher_login(request)
    exam_id = request.GET.get('exam')
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
                        "standard_score": j.subject.standard_score,

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
                    "class_rank": j.class_rank,
                    "grade_rank": j.grade_rank,
                    "exam_rank": j.exam_rank,
                })
            result.append(stu_scores)
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -11, '教师获取分数时发生错误', str(teacher))


def web_get_exam_extra_data(request):
    teacher = teacher_login(request)
    exam_id = request.GET.get('exam')
    try:
        original = teacher.get_exam_extra_data(teacher.get_scores(exam_id))
        result = []
        for i in original:
            class_data = []
            school_data = []
            exam_data = []
            for j in i.class_extra_data:
                class_data.append({
                    "avg_score": j.avg_score,
                    "medium_score": j.medium_score,
                    "pass_rate": j.pass_rate,
                    "excellent_rate": j.excellent_rate,
                    "perfect_rate": j.perfect_rate,
                    "var": j.var,
                    "class_id": j.class_id,
                    "class_name": j.class_name,
                })
            for k in i.school_extra_data:
                school_data.append({
                    "avg_score": k.avg_score,
                    "medium_score": k.medium_score,
                    "pass_rate": k.pass_rate,
                    "excellent_rate": k.excellent_rate,
                    "perfect_rate": k.perfect_rate,
                    "var": k.var,
                    "school_id": k.school_id,
                    "school_name": k.school_name,
                })
            result.append({
                "subject": {
                    "name": i.subject.name,
                    "code": i.subject.code,
                    "id": i.subject.id,
                    "standard_score": i.subject.standard_score,
                },
                "class_extra_data": class_data,
                "school_extra_data": school_data,
                "exam_extra_data": {
                    "avg_score": i.exam_extra_data.avg_score,
                    "medium_score": i.exam_extra_data.medium_score,
                    "pass_rate": i.exam_extra_data.pass_rate,
                    "excellent_rate": i.exam_extra_data.excellent_rate,
                    "perfect_rate": i.exam_extra_data.perfect_rate,
                    "var": i.exam_extra_data.var,
                },
            })
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -12, '教师获取考试其他信息时发生错误', str(teacher))

def web_teacher_original(request: HttpRequest):
    tea = teacher_login(request)
    userId = request.GET["userId"]
    subjectId = request.GET["subjectId"]
    saveId = generate() # 保存位置
    try:
        tea.get_original_paper(userId, subjectId, './teacher/cache/' + saveId + ".html")
        data = ""
        with open("./teacher/cache/" + saveId + ".html", encoding='utf-8') as cardrdr:
            x = cardrdr.readlines()
            for l in x:
                data = data + "\n" + l
        result = \
            {
                'Result':
                {
                    'Code': 0,
                    'Message': '操作成功完成'
                },
                'DataBody': data
            }
        removeCache(saveId)
        return HttpResponse(json.dumps(result, indent=2, ensure_ascii=False), content_type='application/json')
    except Exception as err:
        return basic_error(err, -14, '获取原卷时发生错误', tea.username)


def removeCache(id: str):
    os.remove('./teacher/cache/' + id + ".html")
