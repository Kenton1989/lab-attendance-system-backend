## Common Query Parameter
- fields=xxx
- search=xxx
- is_active=true/false/*
- limit=50&offset=0
## API List
- /settings
  - system_email
  - early_check_in_mins

- /weeks
  - fields=id,name,monday,next_monday
  - available query
    - search, limit, offset
    - contain_timestamp

- /users
  - fields=id,username,email,display_name,is_active
  - search, is_active, limit, offset
- /users/{id} (id can be "me", which has looser permission check)
  - write only fields=password
- /users/{id}/coordinator_of_courses
- /users/{id}/student_of_courses
<!-- - /users/{id}/teacher_of_courses -->
- /users/{id}/supervisor_of_groups
- /users/{id}/student_of_groups
- /users/{id}/teacher_of_groups
- /users/{id}/executive_of_labs
- /users/{id}/student_attendances
- /users/{id}/teacher_attendances
- /users/{id}/student_make_up_sessions


- /labs
  - fields=id,username,display_name,room_count,{executives},is_active
  - search, is_active, limit, offset
  - executives_contain
- /labs/{id}
  - write only fields=executives_ids
<!-- - /labs/{id}/executives -->
<!-- - /labs/{id}/executives/{id} -->
- /labs/{id}/groups
- /labs/{id}/sessions


- /courses
  - fields=id,code,title,is_active,{coordinators}
  - available query
    - search, is_active, limit, offset
    - coordinators_contain
    - students_contain
- /courses/{id}
  - write only fields=coordinators_ids
<!-- - /courses/{id}/coordinators -->
<!-- - /courses/{id}/coordinators/{id} -->
- /courses/{id}/groups
- /courses/{id}/students
<!-- - /courses/{id}/teachers -->


- /groups
  - fields=id,course,course_code,course_id,name,is_active,{supervisors},{teachers}
  - read only fields=all representations of course
  - write only fields=supervisors_ids, teachers_ids
  - available query
    - search, is_active, limit, offset
    - course_id
    - lab_id
    - supervisors_contain
    - teachers_contain
    - students_contain
- /groups/{id}
<!-- - /groups/{id}/supervisors -->
<!-- - /groups/{id}/supervisors/{id} -->
<!-- - /groups/{id}/teachers -->
<!-- - /groups/{id}/teachers/{id} -->
- /groups/{id}/students
- /groups/{id}/sessions

- /group_students
  - fields=id,user,user_id,group,group_id,seat
  - read only fields=user, group
  - available query
    - limit, offset
    - group_id
    - user_id
- /group_students/{id}


- /sessions
  - fields=id,group,lab,room_no,start_datetime,end_datetime,
           is_compulsory,allow_late_check_in,check_in_deadline,is_active
  - write only: group_id, lab_id
  - available query
    - is_active, limit, offset
    - lab_id
    - group_id
    - user_id
    - min_start_datetime
    - max_start_datetime
- /sessions/{id}

- /student_make_up_sessions
  - fields=id,user,original_session,make_up_session
  - write only: user_id,original_session_id,make_up_session_id
  - available query
    - limit, offset
    - user_id
    - original_session_id
    - make_up_session_id
    - original_group_id
    - make_up_group_id
- /student_make_up_sessions/{id}


- /student_attendances
  - fields=id,session,user,
           check_in_state,check_in_datetime,
           last_modify,remark,is_active
  - write only: session_id,user_id
  - available query
    - limit, offset
    - course_id
    - group_id
    - sessions_id
    - user_id
    - teacher_id
    - min_check_in_time
    - max_check_in_time
- /student_attendances/{id}
- /teacher_attendances
- /teacher_attendances/{id}


- /statistics/student_attendance_counts/
  - fields=course/group/student/teacher,attendance_rate
  - available query
    - limit, offset, ordering
    - grouping=course/group/student/teacher
    - course
    - course_coordinators_contain
    - group
    - group_supervisors_contain
    - student
    - attending_teachers_contain


- /statistics/teacher_attendance_counts/
  - fields=course/group/teacher,attendance_rate
  - available query
    - limit, offset, ordering
    - grouping=course/group/teacher
    - course
    - course_coordinators_contain
    - group
    - group_supervisors_contain
    - teacher

lab per session? session outside of lab?
teacher per session?