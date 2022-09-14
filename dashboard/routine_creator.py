import datetime

from account.models import *

from dashboard.models import *

available_teachers = Teacher.objects.filter(is_available=True)


def get_teachers(faculty_name):
    faculty = Faculty.objects.get(name=faculty_name)
    departments = faculty.department_set.all()
    teachers = available_teachers.filter(department__in=departments)

    examiners = []
    supervisors = []

    for teacher in teachers:
        if teacher.check_supervisor:
            supervisors.append(teacher)
        else:
            examiners.append(teacher)

    examiners = sorted(examiners, key=lambda t: t.total_creadits)
    supervisors = sorted(supervisors, key=lambda t: t.total_creadits)

    return supervisors, examiners


def get_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


def get_next_date(cur_date, delta=1):
    return cur_date + datetime.timedelta(days=delta)


def get_next_events(cur_date):
    return Event.objects.filter(start_date__lte=cur_date, end_date__gte=cur_date).all()


def get_next_exams(cur_date, room, shift):
    return Exam.objects.filter(exam_date=cur_date, room_number=room, exam_time=shift).all()


def get_available_date(cur_date, room, shift):

    if cur_date.weekday() == 4:
        cur_date = get_next_date(cur_date)

    if cur_date.weekday() == 5:
        cur_date = get_next_date(cur_date)

    events = get_next_events(cur_date)
    exams = get_next_exams(cur_date, room, shift)
    if len(events) == 0 and len(exams) == 0:
        return cur_date

    if len(events) != 0:
        cur_date = events[0].end_date
    cur_date = get_next_date(cur_date)

    return get_available_date(cur_date, room, shift)


def get_end_date(cur_date, room, shift, courses: Course):

    for _ in range(len(courses)):
        cur_date = get_available_date(cur_date, room, shift)
        cur_date = get_next_date(cur_date, (int)(courses[_].credits))

    return cur_date


def get_best_info(start_date, courses):
    rooms = Room.objects.all()
    shifts = Shift.objects.all()

    best_room = None
    best_shift = None
    best_end_date = None

    for room in rooms:
        for shift in shifts:
            cur_date = start_date
            end_date = get_end_date(
                cur_date, room.room_no, shift.time, courses)
            if (not best_end_date) or (best_end_date > end_date):
                best_room = room.room_no
                best_shift = shift.time
                best_end_date = end_date

    return best_room, best_shift


def CreateRoutine(routine_name, faculty_name, department_name, level, semester, exam_type, num_students, date_str):

    faculty = Faculty.objects.get(name=faculty_name)
    supervisors, examiners = get_teachers(faculty_name)
    department = Department.objects.get(name=department_name)

    courses = department.course_set.filter(
        level=level, semester=semester, is_sessional=exam_type)

    start_date = get_date(date_str)

    routine = Routine()
    routine.name = routine_name
    routine.department = department
    routine.start_date = start_date
    routine.is_approved = False
    routine.save()

    room, shift = get_best_info(start_date, courses)

    cur_date = get_date(date_str)
    need_examiners = max(2, (num_students-5) // 15)

    for course in courses:

        exam = Exam()

        cur_date = get_available_date(cur_date, room, shift)
        exam.exam_date = cur_date
        cur_date = get_next_date(cur_date, (int)(course.credits))

        exam.exam_time = shift

        exam.room_number = room

        exam.faculty = faculty

        exam.course = course

        exam.supervisor = supervisors[0]

        supervisors[0].total_creadits += course.credits

        exam.routine = routine

        exam.save()

        for _ in range(need_examiners):
            exam.examiners.add(examiners[_])
            examiners[_].total_creadits += course.credits

        examiners = sorted(examiners, key=lambda t: t.total_creadits)
        supervisors = sorted(supervisors, key=lambda t: t.total_creadits)
