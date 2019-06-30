# My Scheduler

Here is a scheduler made with Djangom celery and Redis. From data in a DynamoDB, it will create custom reports.
Below, you will find:
- How to install the project
- How to create tasks
- My approach
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

## My approach

### Tasks
- Considering the assignment, I knew that I had to do a scheduler and avoid the old cron jobs.
- Django / Celery was the obvious solution. I needed another tool to handle the "easily customisable" issue. I decided 
to use django celery beat which work perfectly.

#### Queue
- I used redis instead of rabbitmq mostly because I already know Redis.

### DB
- Boto for the AWS client was a no-brainer.
- Concerning the tables, I choose the request-id as primary key for the events since it's different each time. But I 
had to create a uuid for the Visitor report table.
- I thought about creating an index for the dates to improve Events queries. But it would increase the writing time 
for each event entry. We don't want that.

## Improvements
Tasks
- If I had the time, I would have try to use [airflow](https://airflow.apache.org/) which is a more complete tool and 
can be combined with.
- I am not a fan of the positional argument for the minutes tasks. I would use Airflow or find another way for it.

Tests
- I need to add test for every section including mocking the AWS requests.

Deployment
- I want to dockerize it.


## Authors

* **Chris LERUS**
