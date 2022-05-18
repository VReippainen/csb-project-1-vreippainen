# Recipe app for Cyber Security Base 2022: Project 1

## 1. Project purpose

This is a simple recipe app for MOOC course Cyber Security Base 2022: Project 1. Authenticated users can add new recipes to app. The app then fetches the website using the recipe url scrapes recipe data from structured data and generates a dashing recipe site. This app was tested using valio.fi recipes, but should work with any other website (besides k-ruoka.fi), which contains recipes as structured data. More info about structured data can be found here https://developers.google.com/search/docs/advanced/structured-data/intro-structured-data

The application contains various security vulnerabilities partly on purpose. The flaws are marked in the comments using FLAW tag.

## 2. Architecture

The whole application is built using Django framework and uses django templates to render websites on server. The application uses sqlite as database.

## 3. Development environment

### 3.1. Prerequisites

Make sure you have Python 3 and pip installed. This application was implemented using Python 3.10.3 and probably works on other Python 3 versions as well.

I also highly recommend installing venv or pipenv for installing packages locally.

### 3.2. Run tests

Applications contains automated tests, which uses built-in Django testing tools. Tests can be run followingly:

```
python manage.py test
```

### 3.3. Migrations

To create new migrations:
```
python manage.py makemigrations
```

To apply migrations:
```
python manage.py migrate
```

### 3.4. Start the application locally

After cloning the git repository, first install packages from requirements.txt using pip. I highly recommend using venv or pipenv for this.

```
pip install -r requirements.txt
```

Next apply migrations:

```
python manage.py migrate
```

Create an admin user:

```
python manage.py createsuperuser
```

Start the application:
```
python manage.py runserver
```


### 3.5. Access the application locally

Navigate to localhost:8000/recipe. You should be redirected to login page. Login using the recently created admin credentials.

You should now see an empty recipe list. Create new recipe by clicking the "Add recipe" button. Add a title, url and your own comment of the recipe, for example

```
Title: Kaalilaatikko
URL: https://www.valio.fi/reseptit/kaalilaatikko-1/
Comments: Yrjistä, ei enää ikinä
```

Click save. You are now taken to recipe site, where you can see your kaalilaatikko recipe. Click "Back" button to get back to recipe list.