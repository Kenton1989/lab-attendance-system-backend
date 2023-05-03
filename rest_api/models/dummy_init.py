from rest_api import models
from datetime import date, timedelta, timezone
from random import randrange, sample, choice
from datetime import timedelta, datetime, time
from django.contrib.auth.models import Group as AdminGroup
from rest_api.models import *
from rest_api.serializers import *
from django.conf import settings


class DummyCfg:
    STAFF_CNT = 20
    TEACHER_CNT = 20
    STUDENT_CNT = 100
    PASSWORD = '12345678'

    TEACHING_WEEK_CNT = 8
    RECESS_WEEK = 8
    FIRST_MONDAY = date(2023, 5, 1)

    LAB_CNT = 4

    COURSE_CNT = 5
    ROOM_CNT = 4
    GROUP_CNT = 3
    GROUP_TA_CNT = 2
    GROUP_MAX_STUD_CNT = 30

    GROUP_MAX_SESSION_CNT = 5


def rand_bool():
    return choice([True, False])


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

    def make_user(count, username_fmt, display_name, email, groups):
        for i in range(count):
            username = username_fmt.format(id=i)
            if models.User.objects.filter(username=username).exists():
                print(username, 'already exists')
                continue
            user = models.User.objects.create(
                username=username,
                display_name=display_name.format(id=i),
                email=email.format(id=i),
            )
            user.set_password(cfg.PASSWORD)

            for grp_name in groups:
                grp = AdminGroup.objects.get(name=grp_name)
                user.groups.add(grp)
            user.save()

            print('created', username)

    make_user(cfg.STAFF_CNT,
              'STAFF{id:04d}',
              'Staff {id}',
              'staff{id:04d}@ntu.edu.sg',
              ['staff'])
    make_user(cfg.TEACHER_CNT,
              'TA{id:04d}',
              'TA {id}',
              'ta{id:04d}@e.ntu.edu.sg',
              ['teacher'])
    make_user(cfg.STUDENT_CNT,
              'STUD{id:04d}',
              'Student {id}',
              'stud{id:04d}@e.ntu.edu.sg',
              ['student'])


def create_dummy_week(*_):
    cfg = DummyCfg()

    week_names = ['week {}'.format(i)
                  for i in range(1, cfg.TEACHING_WEEK_CNT+1)]
    week_names.insert(cfg.RECESS_WEEK-1, 'recess week')
    one_week = timedelta(days=7)
    monday = cfg.FIRST_MONDAY
    for name in week_names:
        s = WeekSerializer(data={
            'name': name,
            'monday': monday,
            'next_monday': monday+one_week
        })
        if s.is_valid():
            s.save()
            print('created', name)
        else:
            print(name, 'not created')
        # models.Week.objects.create(
        #     name=name,
        #     monday=monday,
        #     next_monday=monday+one_week
        # ).save()

        monday += one_week


def create_dummy_lab(*_):
    cfg = DummyCfg()
    lab_grp = AdminGroup.objects.get(name='lab')

    for i in range(cfg.LAB_CNT):
        username = 'LAB{}'.format(i+1)
        if models.User.objects.filter(username=username).exists():
            print(username, 'already exists')
            continue
        user, _ = models.User.objects.get_or_create(
            username='LAB{}'.format(i+1),
            display_name='Lab {}'.format(i+1),
            email='scse-enquiries@ntu.edu.sg'
        )
        user.set_password(cfg.PASSWORD)
        user.groups.add(lab_grp)
        user.save()
        lab, _ = models.Lab.objects.get_or_create(
            user=user,
            defaults={'room_count': 2}
        )
        exe = rand_staff()
        lab.executives.add(exe)
        lab.save()
        print('created lab', lab.user.username)


def create_dummy_course(*_):
    cfg = DummyCfg()

    for i in range(cfg.COURSE_CNT):
        code = 'SC{:04d}'.format(i+1)
        if models.Course.objects.filter(code=code).exists():
            print('course', code, 'already exists')
            continue
        course = models.Course.objects.create(
            code=code,
            title='Course {}'.format(i+1),
        )
        coord = rand_staff()
        course.coordinators.add(coord)
        course.save()


def create_dummy_group(*_):
    cfg = DummyCfg()
    all_codes = ['SC{:04d}'.format(i+1) for i in range(cfg.COURSE_CNT)]
    for i in range(cfg.GROUP_CNT):
        # codes = sample(all_codes, k=2)
        codes = all_codes
        for code in codes:
            course = models.Course.objects.get(code=code)
            name = 'CZ{}'.format(i+1)
            g = GroupSerializer(data={
                'course_id': course.id,
                'name': name,
                'lab_id': rand_lab().id,
                'room_no': choice([1, 2, 3, None]),
                'supervisor_ids': [rand_staff().id],
                'teacher_ids': [rand_ta().id for j in range(cfg.GROUP_TA_CNT)],
            })
            if not g.is_valid():
                print('group', course.code, name, 'not created', g.errors)
                continue

            g_model = g.save()
            stud_cnt = 0
            for student_no in range(cfg.GROUP_MAX_STUD_CNT):
                gs = GroupStudentSerializer(data={
                    'student_id': rand_student().id,
                    'group_id': g_model.id,
                })
                if gs.is_valid():
                    gs.save()
                    stud_cnt += 1
            print('group', course.code, name,
                  'created with', stud_cnt, 'students')


def create_dummy_session(*_):
    weeks = list(models.Week.objects.all())
    one_week_hours = 7*24 - 2
    two_hours = timedelta(hours=2)
    tz = datetime.utcnow().astimezone().tzinfo

    cfg = DummyCfg()
    for grp in Group.objects.all():
        session_cnt = 0
        for i in range(cfg.GROUP_MAX_SESSION_CNT):
            week = choice(weeks)
            start = datetime.combine(
                week.monday, time(), tz)+timedelta(hours=randrange(one_week_hours))
            s = SessionSerializer(data={
                'group_id': grp.id,
                'start_datetime': start,
                'end_datetime': start+two_hours,
                'is_compulsory': rand_bool(),
                'allow_late_check_in': rand_bool(),
                'check_in_deadline_mins': 30,
            })
            if s.is_valid():
                s.save()
                session_cnt += 1
            else:
                print(s.errors)
            # models.Session.objects.create(
            #     group=grp,
            #     start_datetime=start,
            #     end_datetime=start+two_hours
            # ).save()
        print('created', session_cnt, 'sessions for group',
              grp.course.code, grp.name)


def create_dummy_attendance(*_):
    cfg = DummyCfg()
    past_sess = models.Session.objects.filter(
        start_datetime__lt=datetime.utcnow().astimezone())

    print('createing attendance records for', len(past_sess), 'sessions')

    for sess in past_sess:
        for stud in sess.group.students.all():
            s = StudentAttendanceSerializer(data={
                'session_id': sess.id,
                'attender_id': stud.id,
                'check_in_state': choice([
                    CheckInState.ABSENT,
                    CheckInState.ATTEND,
                    CheckInState.LATE,
                ])
            })
            if s.is_valid():
                s.save()
            else:
                print(s.errors)
        for ta in sess.group.teachers.all():
            s = TeacherAttendanceSerializer(data={
                'session_id': sess.id,
                'attender_id': ta.id,
                'check_in_state': CheckInState.ATTEND
            })
            if s.is_valid():
                s.save()
            else:
                print(s.errors)
        print('created attendance record for', sess)


def create_dummy_admin():
    if User.objects.filter(username='ADMIN').exists():
        print('ADMIN already created')
        return

    create_admin = False
    if settings.DEBUG:
        create_admin = True
    else:
        ch = input('do you want to create dummy ADMIN in non-debug mode? (y/n)')
        if ch.startswith('y') or ch.startswith('Y'):
            create_admin = True

    if create_admin:
        admin = User.objects.create_superuser(
            username='ADMIN',
            email='admin@example.com',
            password='12345678',
        )

        admin_grp = AdminGroup.objects.get(name='admin')

        admin.groups.add(admin_grp)
        admin.save()

        print('created ADMIN')
    else:
        print('ADMIN not created')


def create_all_dummy():
    create_dummy_week()
    create_dummy_admin()
    create_dummy_user()
    create_dummy_lab()
    create_dummy_course()
    create_dummy_group()
    create_dummy_session()
    create_dummy_attendance()
