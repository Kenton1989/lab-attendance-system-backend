if [[ $BACKEND_SERVER == "" ]]; then
    export BACKEND_SERVER=127.0.0.1:8000
fi

if [[ $STATIC_FILE_PATH == "" ]]; then
    export STATIC_FILE_PATH=${HOME}/dev/lab-attendance-system-webapp/build
fi

envsubst '\$BACKEND_SERVER \$STATIC_FILE_PATH'