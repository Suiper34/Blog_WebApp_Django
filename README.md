# README.md

# Blog Web Application Django

Welcome to the Blog Web App Django project! This is a blog web application built using Django, allowing users to create, read, update, and delete blog posts. It also includes user authentication features for registration and login and password reset.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Deployment](#deployment)

## Features

- User registration and authentication
- Create, edit, and delete blog posts
- Comment on blog posts
- Responsive design with Bootstrap
- Password reset
- Contact form for user inquiries

## Technologies Used

- Django
- Python
- SQLite
- Bootstrap
- CKEditor

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Suiper34/Blog_WebApp_Django.git
   cd Blog_WebApp_Django
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate(Windows) or source venv/bin/activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add your environment variables, such as:

   ```
   SECRET_KEY=your_secret_key
   DB_URI=your_database_uri
   MAIL=your_email@example.com
   PASSWORD=your_email_password
   etc
   ```

5. **Run migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional):**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   You can now access the application at `http://127.0.0.1:8000/`.

## Usage

- Visit the home page to view the 3 latest blog posts.
- Visit the all blogs page to view all blog posts.
- Register for an account or log in to create new posts and comment on existing ones.
- Use the contact form to send inquiries.

## Deployment

For deployment instructions, refer to the `docs/deployment.md` file.
