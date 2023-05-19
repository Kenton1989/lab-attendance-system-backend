if [[ $BACKEND_SERVER == "" ]]; then
    export BACKEND_SERVER=127.0.0.1:8000
fi

if [[ $STATIC_FILE_PATH == "" ]]; then
    if [[ $FRONTEND_PROJ_FOLDER == "" ]]; then
        export STATIC_FILE_PATH=/home/VMadmin/dev/lab-attendance-system-webapp/build
    else
        export STATIC_FILE_PATH=$FRONTEND_PROJ_FOLDER/build
    fi
fi

envsubst '\$BACKEND_SERVER \$STATIC_FILE_PATH'