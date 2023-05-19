# lab-attendance-system-backend

## Installation (for Linux only)

1. Clone and enter the repo
``` bash
git clone https://github.com/Kenton1989/lab-attendance-system-backend.git
cd lab-attendance-system-backend
```

2. Open the file deployment/init-database.sql, find the following line, and change the password between the quotes. This is the password of the user that will be used by the backend program to access the database. Remember your new password, you will use it again in the next step.
``` sql
IDENTIFIED BY 'Pa$$w0rd123'; -- TODO: CHANGE THE PASSWORD ON THIS LINE !!
```

3. Run the deployment script, it will install everything needed (hopefully) and start the backend server on 127.0.0.1:8000. Please follow the prompt and enter the required information, including confirmation of installing package, the password of database user, etc.
``` bash
sudo bash ./deployment/be-full-deploy.sh
```

4. If you have killed the server and want to restart it, please run the quick deployment script, which will directly run the server and not go through installation steps.
``` bash
sudo bash ./deployment/be-quick-deploy.sh
```