# My Scheduler

Here is a scheduler made with Djangom celery and Redis. From data in a DynamoDB, it will create custom reports.
Below, you will find:
- How to install the project
- How to create tasks
- A explanation of the different technology that I used
- What can be improved

### Prerequisites

- Redis. A local server should be launch on port 6379. You can change the port in scheduler/celery.py.
- DynamoDB database and Amazon Webservices Credentials.
```
$ cat -e ~/.aws/credentials
[default]$
aws_access_key_id = YOUR_KEY$
aws_secret_access_key = YOUR_ACCESS_KEY$

$ cat -e ~/.aws/config
[default]$
region=us-east-1$
```

### Installing

1) I suggest to create a virtual environment to avoid any interaction with another env.

```
$ virtualenv -p python3 venv

$ source venv/bin/activate
```

2) Install the requirements and Redis:

`$ pip install -r requirements.txt`

3) Run the django server, the celery worker and the celery beat with the following command:

```
$ ./manage.py runserver
$ celery -A scheduler beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
$ celery -A scheduler worker -l info
```

4) Go the admin to manage the tasks:
```
http://localhost:8000/admin/
```

5) You can use the data/fill_db.py to fill your DynamoDB the the events.json file.

## Usage

1) From http://localhost:8000/admin/django_celery_beat/periodictask/
 You can create periodictask based on the two existing task:
 - `build_reports_last_minutes`: from a given positional argument (in minutes), it will create new reports based on 
 the last minutes.
 - `build_reports_from_22_to_25`: It will create reports for the events between June 22nd and 25th
  (based on the events.json)
 
 You can choose the type of schedule (at least one), and the minutes positional argument of mandatory for 
 the `build_reports_last_minutes` task. 

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Authors

* **Chris LERUS**
