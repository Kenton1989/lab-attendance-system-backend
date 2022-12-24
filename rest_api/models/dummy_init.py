from rest_api import models
from datetime import date, timedelta
from random import randrange, choices, choice
from datetime import timedelta, datetime, time


class DummyCfg:
    STAFF_CNT = 20
    TEACHER_CNT = 20
    STUDENT_CNT = 100
    PASSWORD = '12345678'

    TEACHING_WEEK_CNT = 14
    RECESS_WEEK = 8
    FIRST_MONDAY = date(2023, 1, 9)

    LAB_CNT = 4

    COURSE_CNT = 5
    ROOM_CNT = 4
    GROUP_CNT = 5
    GROUP_TA_CNT = 2
    GROUP_STUD_CNT = 20

    SESSION_CNT = 5


def rand_user(format: str, id_beg, id_end):
    username = format.format(randrange(id_beg, id_end))
    return models.User.objects.get(username=username)


def rand_staff():
    return rand_user('STAFF{:04d}', 0, DummyCfg.STAFF_CNT)


def rand_ta():
    return rand_user('TA{:04d}', 0, DummyCfg.TEACHER_CNT)


def rand_lab():
    return rand_user('LAB{:01d}', 1, DummyCfg.LAB_CNT+1)


def rand_student():
    return rand_user('STUD{:04d}', 0, DummyCfg.STUDENT_CNT)


def create_dummy_user(*_):
    cfg = DummyCfg()

    def make_user(count, username, display_name, email):
        for i in range(count):
            user = models.User.objects.create(
                username=username.format(id=i),
                display_name=display_name.format(id=i),
                email=email.format(id=i),
            )
            user.set_password(cfg.PASSWORD)
            user.save()
            print('created', username.format(id=i))

    make_user(cfg.STAFF_CNT,
              'STAFF{id:04d}',
              'Staff {id}',
              'staff{id:04d}@ntu.edu.sg')
    make_user(cfg.TEACHER_CNT,
              'TA{id:04d}',
              'TA {id}',
              'ta{id:04d}@e.ntu.edu.sg')
    make_user(cfg.STUDENT_CNT,
              'STUD{id:04d}',
              'Student {id}',
              'stud{id:04d}@e.ntu.edu.sg')


def create_dummy_week(*_):
    cfg = DummyCfg()

    week_names = ['week {}'.format(i)
                  for i in range(1, cfg.TEACHING_WEEK_CNT+1)]
    week_names.insert(cfg.RECESS_WEEK-1, 'recess week')
    one_week = timedelta(days=7)
    monday = cfg.FIRST_MONDAY
    for name in week_names:
        models.Week.objects.create(
            name=name,
            monday=monday,
            next_monday=monday+one_week
        ).save()
        print('created', name)
        monday += one_week


def create_dummy_lab(*_):
    cfg = DummyCfg()

    for i in range(cfg.LAB_CNT):
        user = models.User.objects.create(
            username='LAB{}'.format(i+1),
            display_name='Lab {}'.format(i+1),
            email='scse-enquiries@ntu.edu.sg'
        )
        user.set_password(cfg.PASSWORD)
        user.save()
        lab = models.Lab.objects.create(
            user=user,
            room_count=4,
        )
        exe = rand_staff()
        lab.executives.add(exe)
        lab.save()


def create_dummy_course(*_):
    cfg = DummyCfg()

    for i in range(cfg.COURSE_CNT):
        course = models.Course.objects.create(
            code='SC{:04d}'.format(i+1),
            title='Course {}'.format(i+1),
        )
        coord = rand_staff()
        course.coordinators.add(coord)
        course.save()


def create_dummy_group(*_):
    cfg = DummyCfg()
    all_codes = ['SC{:04d}'.format(i+1) for i in range(cfg.COURSE_CNT)]
    for i in range(cfg.GROUP_CNT):
        codes = choices(all_codes, k=2)
        for code in codes:
            course = models.Course.objects.get(code=code)
            name = 'CZ{}'.format(i+1)
            print('create', course.code, name)
            grp = models.Group.objects.create(
                course=course,
                name=name,
                lab_id=rand_lab().id,
                room_no=choice([1, 2, 3, None])
            )
            grp.supervisors.add(rand_staff())
            for j in range(cfg.GROUP_TA_CNT):
                grp.teachers.add(rand_ta())
            for j in range(cfg.GROUP_STUD_CNT):
                grp.students.add(rand_student())
            grp.save()


def create_dummy_session(*_):
    weeks = list(models.Week.objects.all())
    one_week_hours = 7*24 - 2
    two_hours = timedelta(hours=2)

    cfg = DummyCfg()
    for grp in models.Group.objects.all():
        for i in range(cfg.SESSION_CNT):
            week = choice(weeks)
            start = datetime.combine(
                week.monday, time())+timedelta(hours=randrange(one_week_hours))
            models.Session.objects.create(
                group=grp,
                start_datetime=start,
                end_datetime=start+two_hours
            ).save()


def create_dummy_attendance(*_):
    cfg = DummyCfg()

    for sess in models.Session.objects.all().order_by('start_datetime')[:10]:
        for stud in sess.group.students.all():
            models.StudentAttendance.objects.create(
                session=sess,
                attender=stud,
            ).save()
        for ta in sess.group.teachers.all():
            models.TeacherAttendance.objects.create(
                session=sess,
                attender=ta,
            ).save()


def create_all_dummy():
    create_dummy_week()
    create_dummy_user()
    create_dummy_lab()
    create_dummy_course()
    create_dummy_group()
    create_dummy_session()
    create_dummy_attendance()
