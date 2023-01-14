
![Logo](https://avatars.githubusercontent.com/u/117459812?s=200&v=4)
#   Newsify - Profile Management Service
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=fff&style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=fff&style=for-the-badge)

## Table of Content
1. [Prerequisites](#prerequisites)
2. [Getting started](#getting-started)
3. [Repository Overview](#repository-overview)
4. [Deployment](#deployment)

This service implements a REST interface for user management based on Django.
##  Prerequisites
- Python v3.10
- [Activated Google OAuth2](https://console.cloud.google.com/apis/credentials), see Google documentation [here](https://developers.google.com/identity/account-linking/oauth-linking).
### Packages
- [Django](https://www.djangoproject.com/start/overview/) v4.1
- [Django Rest Framework](https://www.django-rest-framework.org/) v3.14.0
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) v5.2.2
- [django-allauth](https://django-allauth.readthedocs.io/en/latest/) v0.51

See full list in `requirements.txt`

##  Getting started
1. Run `python -m venv venv` to create a virtual environment
2. Activate virtual environment with 
   * MacOS: `source ./venv/bin/activate`
   * Windows: `source ./venv/Scripts/activate`
2. Install all necessary packages by runnng `pip install -r requirements.txt`
3. Make migratoins: `python manage.py migrate`
4. Create an initial super-user account to configure profile-management by running `python manage.py createsuperuser` and follow the steps
5. Start development service by running `python manage.py runserver`
6. Visit http://127.0.0.1:8000/admin/socialaccount/socialapp/, login with the previous created super-user account
7. Add social app e.g. Google OAuth as follows:
![Add Social App](https://github.com/Cloud-Computing-WI3/.github/blob/main/images/profile-management/profile_management_add-social-app.png?raw=true)
8. Make sure to add http://127.0.0.1:8000/accounts/google/login/callback/ as authorized Redirect URI in your [Google OAuth2](https://console.cloud.google.com/apis/credentials)  

##  Repository Overview
### Folder Structure
```bash
profile_management
│   README.md
│   manage.py
│   Dockerfile
│   requirements.txt
│
└───accounts
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializers.py
│   │   tests.py
│   │   urls.py
│   │   views.py
|
└───categories
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializers.py
│   │   tests.py
│   │   urls.py
│   │   views.py
|
└───core
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
|
└───keywords
    │   admin.py
    │   apps.py
    │   models.py
    │   serializers.py
    │   tests.py
    │   urls.py
    │   views.py
```

One folder is created per "app" in a Django project. A special case is the "core" directory. This is the directory that contains settings for the entire project. Take a look at the [Django documentation](https://www.djangoproject.com/start/overview/) to understand why the folders exist.
In each app, different files are created that perform a specific task. 

In the file "admin.py" important functions are defined for the admin area. The file "apps.py" creates a namespace for the app, which is necessary for Python. 
"models.py" is one of the most important files. Here the entities, such as user or the keywords and categories with their attributes are created. Since we use the REST framework of Django and export the data from the database as JSON objects, it is necessary to "serialize" them (see https://www.django-rest-framework.org/api-guide/serializers/). This is the only way to pass the objects to the frontend via the API. This is done in the file "serializers.py". Tests are defined in "tests.py". Under "urls.py" the routes are defined, under which the functions from "views.py" are addressable. 


##  Deployment
![Amazon RDS](https://img.shields.io/badge/Amazon%20RDS-527FFF?logo=amazonrds&logoColor=fff&style=for-the-badge)
![Amazon S3 Badge](https://img.shields.io/badge/Amazon%20S3-569A31?logo=amazons3&logoColor=fff&style=for-the-badge)
![Google Cloud Run](https://img.shields.io/badge/Google%20Cloud-4285F4?logo=googlecloud&logoColor=fff&style=for-the-badge)

Full tutorial of how to deploy a Django app to Google Cloud is provided [here](https://cloud.google.com/python/django/run).

> Tip: Think about where you want to host the database. This guide uses an Amazon Redshift database. How to deploy to Google Cloud SQL is explained in the documentation above. 

### Prerequisites
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
- [AWS Free Tier Account](https://aws.amazon.com/free/?nc1=h_ls&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all)

#### Deployment steps

Use S3 Bucket as storage for user profile pictures:
1. Login to AWS
2. Navigate to [Create Bucket](https://s3.console.aws.amazon.com/s3/bucket/create)
3. Set a bucket name
4. Leave _Block all public access_ as is
5. Click Create Bucket
6. Create a user who should have full access to S3 ([here](https://us-east-1.console.aws.amazon.com/iamv2/home#/users)) 
7. Click _Add Users_
8. Set a Username
9. Select _Access key - Programmatic access_ as credential type
10. Click Next
11. Under _Permissions_ select _Attach existing policies directly_, search for `AmazonS3FullAccess` and select it
12. Click Next 2 times
13. Create User
> **IMPORTANT:** Save generated Access key ID and Secret access key

14. In `core/settings.py` set 
    * `AWS_ACCESS_KEY_ID` to your _Access key ID_
    * `AWS_SECRET_ACCESS_KEY` to your _Secret access key_
    * `AWS_STORAGE_BUCKET_NAME` to the _name of your Bucket_ ([Buckets](https://s3.console.aws.amazon.com/s3/buckets?region=eu-central-1) > Your Bucket > Access Points > Access Point alias) 

Configure MySQL-Database in AWS RDS:
1. Login to AWS
2. Navigate to [Create a RDS database](https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1#launch-dbinstance:gdb=false;isHermesCreate=true;s3-import=false)
3. Setup MySQL-Database as follows:
   >  Make sure "Free Tier" is select in Templates

   ![Setup MySQL in AWS RDS](https://github.com/Cloud-Computing-WI3/.github/blob/main/images/profile-management/profile_management-setup-aws-rds-mysql.png?raw=true)
4. Change `USER`, `PASSWORD` and `HOST` key of _DATABASES_ in `core/settings.py` (Line 105) to your previous created credentials
5. Run `python manage.py makemigrations`
6. Run `python manage.py migrate`

Google Cloud Run:
1. Create a branch `cloud`
2. Set `DEBUG` to False in `core/settings.py`
3. Login to Google Cloud and create a new Cloud Run service ([here](https://console.cloud.google.com/run/create))
4. Select "Continuously deploy new revisions from a source repository" and click on "Set up with Cloud Build"
5. Connect your GitHub Repository, select it and click Next
   ![Setup Cloud Run Step #1](https://github.com/Cloud-Computing-WI3/.github/blob/main/images/profile-management/profile_management-setup-cloud-run1.png?raw=true)
6. Select `cloud` as Branch and `Dockerfile` as Build Type and click Save
   ![Setup Cloud Run step #2](https://github.com/Cloud-Computing-WI3/.github/blob/main/images/profile-management/profile_management-setup-cloud-run2.png?raw=true)
7. Set rest of the configuration as follows:
   ![Setup Cloud Run step #2](https://github.com/Cloud-Computing-WI3/.github/blob/main/images/profile-management/profile_management-setup-cloud-run3.png?raw=true)
8. Click Create and wait for deployment to complete

