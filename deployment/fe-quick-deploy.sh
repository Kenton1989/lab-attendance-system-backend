if [[ $FRONTEND_PROJ_FOLDER == "" ]]; then
    export FRONTEND_PROJ_FOLDER=/home/VMadmin/dev/lab-attendance-system-webapp
fi

#############################

echo checking location of frondend project folder...

if [ ! -d "$FRONTEND_PROJ_FOLDER" ]; then
    echo cannot find frondend project folder \($FRONTEND_PROJ_FOLDER\), please clone it or set the env variable \$FRONTEND_PROJ_FOLDER properly
    exit 1
fi

cd $FRONTEND_PROJ_FOLDER

###########################

echo installing packages
npm install

###########################

echo building product
npm run build
export STATIC_FILE_PATH=$FRONTEND_PROJ_FOLDER/build

