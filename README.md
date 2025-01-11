# Blog Application

This is a Django-based blog application that allows users to create, read, update, and delete blog posts. The application also includes user authentication and category management.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Features

- User authentication (registration, login, logout)
- Create, read, update, and delete blog posts
- Category management
- JWT-based authentication
- Cloudinary integration for image uploads
- PostgreSQL database

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Aditya-Naresh/User-Blog-Management-server.git
    cd blog-application
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    Create a [.env] file in the [blog](blog) directory with the following content:

    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    CLOUDINARY_CLOUD_NAME=your_cloud_name
    CLOUDINARY_API_KEY=your_api_key
    CLOUDINARY_API_SECRET=your_api_secret
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your_email
    EMAIL_HOST_PASSWORD=your_email_password
    FRONTEND_URL=http://localhost:5173
    DB_URL=postgresql://your_db_user:your_db_password@your_db_host/your_db_name
    ```

5. Apply the migrations:

    ```sh
    python manage.py migrate
    ```

6. Create a superuser:

    ```sh
    python manage.py createsuperuser
    ```

7. Run the development server:

    ```sh
    python manage.py runserver
    ```

## Usage

- Access the admin panel at `http://localhost:8000/admin/` to manage users and blog posts.
- Use the API endpoints to interact with the application.

