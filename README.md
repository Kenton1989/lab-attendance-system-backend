# lab-attendance-system-backend

## Installation (for Linux (Ubuntu) only)

1. Clone and enter the repo

```bash
git clone https://github.com/Kenton1989/lab-attendance-system-backend.git
cd lab-attendance-system-backend
```

2. Open the file deployment/init-database.sql, find the following line, and change the password between the quotes. This is the password of the user that will be used by the backend server to access the database. Remember your new password, you will use it again in the next step.

```sql
IDENTIFIED BY 'Pa$$w0rd123'; -- TODO: CHANGE THE PASSWORD ON THIS LINE !!
```

3. Run the deployment script, it will install everything needed (hopefully) and start the backend server on 127.0.0.1:8000. Please follow the prompt and enter the required information, including confirmation of installing package, the password of database user, etc.

```bash
sudo bash ./deployment/be-full-deploy.sh
```

4. Create a admin user if necessary. Please follow the prompt and enter the required information like username, password, etc.

```bash
python3 ./manage.py create_las_admin
```

5. Populate some dummy data if needed. It will randomly populate many data, including user, course, group, session, etc.

```bash
python3 ./manage.py populate_dummy
```

6. To find out the running lab_attendance_system_backend process, you can try the following command. After knowing the PID of backend server process, you can just use `sudo kill {PID}` to stop the backend server.

```bash
ps aux | grep lab_attendance_system_backend
```

7. If you have killed the server process and want to restart it, please run the quick deployment script, which will directly start the server and not go through installation steps.

```bash
sudo bash ./deployment/be-quick-deploy.sh
```
