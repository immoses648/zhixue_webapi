from zhixuewang import login as zxw_login
from django.http import HttpResponse, HttpResponseBadRequest
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


def teacher_login(request):
    try:
        teacher = None
        if request.GET.__contains__("usr") and request.GET.__contains__("pwd"):
            teacher = zxw_login(request.GET.get('usr'), request.GET.get('pwd'))
        else:
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
            'ID': original.id,
            'Name': original.name,
            'Status': str(original.status),
            'GradeCode': original.grade_code,
            'IsFinal': original.is_final,
        }
        return status_ok(result)
    except Exception as err:
        return HttpResponseBadRequest(
            json.dumps({'login_error': str(teacher), 'run_error': str(err)}, indent=2, ensure_ascii=False))


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
                    'TeacherName': j.teacher_name,
                    'School': {
                        'ID': j.school.id,
                        'Name': j.school.name
                    },
                    "IsOnline": j.is_online,
                    "TeacherCode": j.teacher_code,
                    "CompleteCount": j.complete_count,
                    "UncompleteCount": j.uncomplete_count,
                })
            result.append({
                'DispTitle': i.disp_title,
                'TopicNumber': i.topic_number,
                'CompletePrecent': i.complete_precent,
                'SubjectID': i.subject_id,
                'Teachers': teachers_ls,
                'CompleteCount': i.lete_count,
                'UncompleteCount': i.uncomplete_count,
            })
        return status_ok(result)
    except Exception as err:
        return HttpResponseBadRequest(
            json.dumps({'login_error': str(teacher), 'run_error': str(err)}, indent=2, ensure_ascii=False))


def web_get_school_exam_classes(request):
    teacher = teacher_login(request)
    school_id = request.GET.get('school')
    subject_id = request.GET.get('topic')
    try:
        original = teacher.get_school_exam_classes(school_id, subject_id)
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
        return HttpResponseBadRequest(
            json.dumps({'login_error': str(teacher), 'run_error': str(err)}, indent=2, ensure_ascii=False))


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
                    "Score": j.score,
                    "Subject": {
                        "Name": j.subject.name,
                        "Code": j.subject.code,
                        "StandardScore": j.subject.standard_score,

                    },
                    "Person": {
                        "ID": j.person.id,
                        "Class": {
                            "ID": j.person.clazz.id,
                            "Name": j.person.clazz.name,
                            "School": {
                                "ID": j.person.clazz.school.id,
                                "Name": j.person.clazz.school.name
                            }
                        },
                        "Name": j.person.name,
                        "Gender": str(j.person.gender)
                    },
                    "ClassRank": j.class_rank,
                    "GradeRank": j.grade_rank,
                    "ExamRank": j.exam_rank,
                })
            result.append(stu_scores)
        return status_ok(result)
    except Exception as err:
        return HttpResponseBadRequest(
            json.dumps({'login_error': str(teacher), 'run_error': str(err)}, indent=2, ensure_ascii=False))


def web_get_exam_extra_data(request):
    teacher = teacher_login(request)
    exam_id = request.GET.get('exam')
    try:
        original = teacher.get_exam_extra_data(teacher.get_scores(exam_id))
        result = []
        for i in original:
            class_data = []
            school_data = []
            for j in i.class_extra_data:
                class_data.append({
                    "AvgScore": j.avg_score,
                    "MediumScore": j.medium_score,
                    "PassRate": j.pass_rate,
                    "ExcellentRate": j.excellent_rate,
                    "PerfectRate": j.perfect_rate,
                    "Var": j.var,
                    "ClassID": j.class_id,
                    "ClassName": j.class_name,
                })
            for k in i.school_extra_data:
                school_data.append({
                    "AvgScore": k.avg_score,
                    "MediumScore": k.medium_score,
                    "PassRate": k.pass_rate,
                    "ExcellentRate": k.excellent_rate,
                    "PerfectRate": k.perfect_rate,
                    "Var": k.var,
                    "SchoolID": k.school_id,
                    "SchoolName": k.school_name,
                })
            result.append({
                "Subject": {
                    "Name": i.subject.name,
                    "Code": i.subject.code,
                    "ID": i.subject.id,
                    "StandardScore": i.subject.standard_score,
                },
                "ClassExtraData": class_data,
                "SchoolExtraData": school_data,
                "ExamExtraData": {
                    "AvgScore": i.exam_extra_data.avg_score,
                    "MediumScore": i.exam_extra_data.medium_score,
                    "PassRate": i.exam_extra_data.pass_rate,
                    "ExcellentRate": i.exam_extra_data.excellent_rate,
                    "PerfectRate": i.exam_extra_data.perfect_rate,
                    "Var": i.exam_extra_data.var,
                },
            })
        return status_ok(result)
    except Exception as err:
        return HttpResponseBadRequest(
            json.dumps({'login_error': str(teacher), 'run_error': str(err)}, indent=2, ensure_ascii=False))
