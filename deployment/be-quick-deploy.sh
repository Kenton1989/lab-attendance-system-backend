MANAGE_PY=manage.py

if [ ! -f "$MANAGE_PY" ]; then
    cd ..
fi

if [ ! -f "$MANAGE_PY" ]; then
    echo cannot find $MANAGE_PY, please make sure you are running this script in the Django project root folder
    exit 1
fi

source venv/bin/activate

gunicorn lab_attendance_system_backend.wsgi
GUNICORN_EXIT_CODE=$?

if [[ $GUNICORN_EXIT_CODE == 1 ]]; then
    echo It is likely that gunicorn has already been deployed.
fi

exit $GUNICORN_EXIT_CODE