
![Logo](https://avatars.githubusercontent.com/u/117459812?s=200&v=4)
#   Newsify - Profile Management Service
This service implements a REST interface for user management.
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
3. Create an initial super-user account to configure profile-management by running `python manage.py createsuperuser` and follow the steps
4. Start development service by running `python manage.py runserver`
5. Visit http://127.0.0.1:8000/admin/socialaccount/socialapp/, login with the previous created super-user account
6. Add social app e.g. Google OAuth as follows:
![Add Social App](https://github.com/Cloud-Computing-WI3/.github/blob/main/images/profile-management/profile_management_add-social-app.png?raw=true)
7. Make sure to add http://127.0.0.1:8000/accounts/google/login/callback/ as authorized Redirect URI in your [Google OAuth2](https://console.cloud.google.com/apis/credentials)  

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
