# Educational website for submitting projects

django project for submitting and reviewing tasks or assessments in college, school, see [LinkedIn post](https://www.linkedin.com/posts/amr-emam-0b5255231_projectsassignment-activity-7093684020135247872-K32Q?utm_source=share&utm_medium=member_desktop).

## how to run
* clone the repository
* create virtual environment (if you want)
    virtualenv [virtualenv name]
* download indepencies
```
pip install -r requirements.txt
```
* make migrataions, migrate to database, and run the servers with these commands
```
python manage.py makemigrations
```

```
python manage.py migrate
```

```
python manage.py runserver
```
* have fun :)
