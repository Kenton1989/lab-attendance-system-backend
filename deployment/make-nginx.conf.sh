export BACKEND_URL=http://127.0.0.1:8000
export STATIC_FILE_PATH=${HOME}/dev/lab-attendance-system-webapp/build
envsubst '\$BACKEND_URL \$STATIC_FILE_PATH'