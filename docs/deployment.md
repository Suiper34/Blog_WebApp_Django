# Deployment Instructions for Codveda Blog Django

This document outlines the steps required to deploy the Blog Django application. Follow these instructions to ensure a successful deployment.

## Prerequisites

Before deploying the application, ensure you have the following:

- A server or cloud platform (e.g. Render, Railway, Heroku, AWS) to host the application.
- Python 3.8+ installed on the server.
- Access to a database (e.g. PostgreSQL, MySQL) if not using SQLite.

## Step 1: Clone the Repository

Clone the project repository to your server:

```bash
git clone https://github.com/Suiper34/Blog_WebApp_Django.git
cd Blog_WebApp_Django
```

## Step 2: Set Up a Virtual Environment

Create and activate a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv\Scripts\activate(Windows) or venv/bin/activate
```

## Step 3: Install Dependencies

Install the required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

Create a `.env` file in the project root and add your environment variables. Example:

```
SECRET_KEY=your_secret_key
DB_URI=your_database_uri
MAIL=your_email
PASSWORD=your_email_password
etc
```

Make sure to replace the placeholders with your actual values.

## Step 5: Database Setup

Run the following commands to apply migrations and create the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 6: Collect Static Files

Collect all static files into a single directory for serving:

```bash
python manage.py collectstatic
```

## Step 7: Configure the Web Server

If using a web server like Gunicorn, WSGI or ASGI, configure it to serve the application. Eg, with Gunicorn:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Step 8: Start the Application

Start your application using the command you configured in Step 7. Ensure it runs in the background or as a service.

## Step 9: Monitor and Maintain

Regularly monitor your application for errors and performance issues. Set up logging and error tracking to help diagnose problems.

## Conclusion

The Blog web application should now be successfully deployed. Visit your domain to see the application in action. For further assistance, refer to the Django documentation or the specific documentation for your hosting provider.
