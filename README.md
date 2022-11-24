#   Profile Management Service
##  Prerequisites
- Python v3.10

### Packages
- [Django](https://www.djangoproject.com/start/overview/) v4.1
- [Django Rest Framework](https://www.django-rest-framework.org/) v3.14.0
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) v5.2.2

See full list in `requirements.txt`
##  Structure
##  Getting started
1. Run through steps described in [Google Cloud Install SDK](https://cloud.google.com/sql/docs/mysql/connect-instance-auth-proxy#macos-64-bit)
2. Run `gcloud auth login` and login with your google cloud user
3. Run `gcloud auth application-default login` and login with your google cloud user
4. Run through steps described in [Google Cloud SQL Proxy](https://cloud.google.com/sql/docs/mysql/quickstart-proxy-test#install-proxy)
5. Run `./cloud_sql_proxy -instances=cohesive-slate-368310:us-central1:profile-management-service=tcp:5435`
6. Make sure, proxy is running
7. Start service by running `python manage.py runserver`
##  Deployment