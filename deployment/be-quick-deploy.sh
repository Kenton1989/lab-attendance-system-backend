MANAGE_PY=manage.py

if [ ! -f "$MANAGE_PY" ]; then
    cd ..
fi

if [ ! -f "$MANAGE_PY" ]; then
    echo cannot find $MANAGE_PY, please make sure you are running this script in the Django project root folder
    exit 1
fi

#########################

ENV_FILE=.env

echo checking location of $ENV_FILE...

if [ ! -f "$ENV_FILE" ]; then
    echo cannot find $ENV_FILE, please make sure $ENV_FILE is properly created
    exit 1
fi

#############################

source venv/bin/activate

#############################

echo checking database migrations...

python3 "$MANAGE_PY" migrate

echo database migrations done

#############################

echo starting backend server...

gunicorn lab_attendance_system_backend.wsgi &