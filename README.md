
# Backend Development Task

This project is a robust backend system for an e-commerce platform, designed to facilitate the management of products, user authentication, shopping cart functionalities, and order processing. Built using Django and Django REST Framework, it provides a RESTful API that allows users to interact with the platform efficiently.

### API DOCUMENTATION

[click here to view complete API DOCUMENTATION ](https://documenter.getpostman.com/view/39599042/2sAY55ZxLm)



# Installation Setup

### Prerequisites:
Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine.
- pip (Python package manager) installed.
- Django and Django REST Framework installed.
- SQLite or another database management system instal


#### Step 1: Clone the Repository

#### Step 2: Create a Virtual Environment
It is recommended to create a virtual environment to manage dependencies. You can create one using: 

python -m venv venv

Activate the virtual environment On Windows:

venv\Scripts\activate

#### Step 3 : Install dependencies
Install the required packages using pip. Make sure you have a requirements.txt file in your project. If not, you can create one with the necessary packages:

pip install django djangorestframework djangorestframework-simplejwt

To install from a requirements.txt file:

pip install -r requirements.txt

#### Step 4: Apply Migrations
First, create migration files based on your models by running:

python manage.py makemigrations

Next, apply the migrations to create the necessary database tables and set up the schema:

python manage.py migrate

#### Step 5: Create a Superuser
To access the Django admin panel, create a superuser by running:

python manage.py createsuperuser

#### Step 6: Run the Development Server
Start the Django development server with the command:

python manage.py runserver

#### Step 7: Access the API
You can now access the API endpoints at http://127.0.0.1:8000/api/. Use tools like Postman to test the endpoints:

- POST /api/signup/ - User registration.

- POST /api/signin/ - User login.

- POST /api/addproduct/ - Add products (admin only).

- PUT /api/updateproduct/<int:productId>/ - Update product details (admin only).

- DELETE /api/deleteproduct/<int:productId>/ - Delete a product (admin only).

- GET /api/products/ - Retrieve a list of all products.

- POST /api/cart/add/ - Add a product to the cart.

- PUT /api/cart/update/ - Update cart details.

- DELETE /api/cart/delete/ - Remove a product from the cart.

- GET /api/cart/ - Retrieve the current user's cart.

- POST /api/placeorder/ - Place an order.

- GET /api/getallorders/ - Retrieve all orders (admin only).

- GET /api/orders/customer/<int:customerId>/ - Retrieve orders for a specific customer.


#### Step 8: API Documentation
Refer to the API documentation created using Postman for detailed information about each endpoint, including request and response formats.

[click here to view complete API DOCUMENTATION ](https://documenter.getpostman.com/view/39599042/2sAY55ZxLm)

# Tech Stack Used

The tech stack used in this e-commerce backend project includes the following components:


#### Backend Framework: 
Django: A high-level Python web framework that encourages rapid development and clean, pragmatic design.

Django REST Framework: A powerful toolkit for building Web APIs in Django, providing features like serialization, authentication, and viewsets.

#### Database:
SQLite: A lightweight, file-based database that is used for development and testing. 

#### Authentication:
Django's Built-in Authentication: Utilizes Django's built-in user model for user management.

JWT (JSON Web Tokens): Implemented using djangorestframework-simplejwt for secure token-based authentication.

#### Serialization:
Django REST Framework Serializers: Used to convert complex data types (like querysets and model instances) into native Python data types that can then be easily rendered into JSON or other content types.

#### Permissions:
Custom Permissions: Implemented to restrict access to certain views based on user roles (e.g., admin vs. regular user).

#### API Documentation:
Postman: Used for creating and testing API endpoints, as well as for generating API documentation.

#### Development Tools:
Python: The primary programming language used for developing the backend logic.

Django Admin: Provides an interface for managing the database and content easily.

#### Other Technologies:

Git: Version control system used for tracking changes in the codebase.

GitHub: Used for hosting the project repository and collaboration.




