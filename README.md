## Amar Boi - online bookshop
Amar Boi is an online bookshop API developed using Django Rest Framework (DRF). It integrates user management, JWT for secure authentication, and django_filters for advanced filtering capabilities. Utilizing nested routers, it organizes various endpoints for seamless navigation. The API supports comprehensive models, including Category, Author, Publication, Book, Order, OrderItem, Customer, Review, Cart, and CartItem. This setup ensures a robust and scalable system, facilitating efficient management of books, orders, and customer interactions, delivering a streamlined and engaging user experience.

## Features
- User management
- JWT for secure authentication
- Advanced filtering with django_filters
- Nested routers for organized endpoints
- Comprehensive models for a full-fledged online bookshop
## Requirements
- Django (4.2, 5.0)
- Python (3.8, 3.9, 3.10, 3.11, 3.12)
## Installation
### 1. Clone the repository
```sh
git clone https://github.com/anmabrar/amar_boi.git
cd amar_boi
```
### 2. Install Pipenv
If you don't have pipenv installed, you can install it using pip:
```sh
pip install pipenv
```
### 3. Install Dependencies
Use pipenv to install the required dependencies:
```sh
pipenv install
```
### 4. Activate the Virtual Environment
Activate the virtual environment created by pipenv:
```sh
pipenv shell
```
### 5. Apply Migrations
Run the following command to apply database migrations:
```sh
python manage.py migrate
```
### 6. Create a Superuser
Create a superuser to access the Django admin interface:
```sh
python manage.py createsuperuser
```
Follow the prompts to set up the superuser credentials.
### 7. Run the Development Server 
Start the Django development server:
```sh
python manage.py runserver
```
## Usage
- Access the admin interface at http://127.0.0.1:8000/admin/ using the superuser credentials.
- Create users, projects, and tasks through the admin interface or implement the frontend as needed.
## Contributing
If you want to contribute to this project, please fork the repository and submit a pull request. We welcome all improvements, whether they are code improvements, bug fixes, or documentation enhancements.
## API Documentation
- `http://127.0.0.1:8000/swagger/` 
- `http://127.0.0.1:8000/redoc/` 

## Additional Notes

-  **Database Configuration**: If you need to use a different database (other than SQLite), make sure to update the `DATABASES` setting in the `settings.py` file.
-  **Static Files**: If you are serving static files, ensure you have set up the static files directory and collected static files using:
   ```bash
   python manage.py collectstatic
    ```
## Additional packages
  - rest_framework
  - rest_framework_simplejwt
  - drf-nested-routers
  - django_filters
  - drf_yasg
  - debug_toolbar

## Swegger Documentation preview
![screencapture-127-0-0-1-8000-swagger-2024-06-26-08_34_24](https://github.com/anmabrar/amar_boi/assets/86479721/bcd72ac5-709d-4fcd-a856-5732358e20cc)
