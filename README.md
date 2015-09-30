Northwestern Course Data API
============================
This repository includes the code that serves API requests and allows users to manage their keys.

Documentation
-------------

[Browse API documentation online and apply for keys at developer.asg.northwestern.edu](http://developer.asg.northwestern.edu)

Working on the API
------------------

You'll need [pip](https://pip.pypa.io/en/stable/installing/) and
[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html).
Then clone the repo, create a virtualenv, and install dependencies:

```
git clone git@github.com:northwesternapis/server.git api
cd api
mkvirtualenv api
pip install -r requirements.txt
```

You might need to install some packages using your system's package manager.
After this, you'll need to install postgres and set up a user and database for
the api. Create a file called `local_settings.py` in the server/ directory with
a SECRET_KEY variable that's a random string and a DATABASES variable for
Django. This is a decent
[guide](http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-posgresql-for-django)
for doing this.

Environment variables
---------------------
- `NUWS_TEST_USERNAME`
- `NUWS_TEST_PASSWORD`
- `NUWS_PROD_USERNAME`
- `NUWS_PROD_PASSWORD`

These variables contain the usernames and passwords for the databases in which Northwestern stores course data.

- `NU_LDAP_URL`
- `NU_LDAP_PASSWORD`

The resource location and application password that enables the API to authenticate NetIDs and passwords.
