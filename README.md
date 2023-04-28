# Lesson u Ivana

## Setup
1. Clone repo using `git clone https://github.com/.../`
2. Install Python 3.11 +
3. Install PostgreSQL 14 +
4. Install virtualenv package for Python `pip install virtualenv`
5. Create virtualenv `virtualenv <name_of_env>`
6. Activate it `source <name_of_env>/bin/activate` (for Windows: `cd <name_of_env>/Scripts`, `activate`)
7. Install all the required packages for project using
   ### For Linux / MacOs
    Run the command - `pip install -r requirements.txt`
   ### For Windows
   1 . Comment `uvloop` module in `requirements.txt` 
   
   2 . Run the command - `pip install -r requirements.txt`

## Start Server
1. Create `.env` file inside cloned project and type inside it:

```
# SMTP Settings
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=
MAIL_STARTTLS=
MAIL_SSL_TLS=
USE_CREDENTIALS=
VALIDATE_CERTS=

# Slack API Token
SLACK_API_TOKEN=

# SWAGGER URL
SWAGGER_URL=

# DB Connection
 DB_NAME=
 DB_USER=
 DB_PASSWORD=
 DB_HOST=
 DB_PORT=
 DB_URL=

 # Bucket Connection
 BUCKET_DOMAIN=
 AWS_STORAGE_BUCKET_NAME=
 AWS_BUCKET_REGION=
 AWS_ACCESS_KEY_ID=
 AWS_SECRET_ACCESS_KEY=

 # Third party API's
 LEAFLET=

 # Allowed hosts
 BACKEND_CORS_ORIGINS=
```

You must fill the variables given for you by Team-Lead
## 2. Start the app
- Now you can start the project `uvicorn main:app` and navigate to `localhost:8000`
- The flag `--reload` allows you to automatically restart the server after the applied changes in the code
- The flag `--port` allows you to change port.