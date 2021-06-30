# qarzapp

## Description
A basic Django admin based application, designed to serve as a system for managing Qarz e Hasana and donations.


## Running Locally

Make sure you have Python 3.8 [installed locally](https://docs.python-guide.org/starting/installation/). 
To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/razibaig/qarzapp.git
$ cd qarzapp

$ python3 -m venv qarzenv
$ pip install -r requirements.txt

$ python manage.py migrate

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku main

$ heroku run python manage.py migrate
$ heroku open
```

Your app should now be running on the herokuapp.com url.

## Documentation

You can create a superuser for admin usage through the following command:

```sh
$ heroku run python manage.py createsuperuser
```

Note: You will be asked to enter the username and password in the prompts (these will be the admin user credentials).

After you have created the super user, you can visit the django admin page (e.g.):

- https://qarz.herokuapp.com/admin/ 

You can login using the credentials created earlier to access the application.

`Application Details:`

- `Qarz Users:` These can be created by the admin user which will serve as the entities availing the donation/loan facilities.

- `Transactions:` These contain the details of actual donations/loans offered to the qarz users. Transactions can be of 3 types: Donation, Loan or Return. 

- `Reports:` These can be created by the admin user to see the aggregated information of donations and/or loans taken by each user before the given date. 

- `Overall Reports:` These can be created by the admin to see the overall statistics of the system including total donations received, total loans given, total pending loans and current balance amount in the system till the given date. 

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
