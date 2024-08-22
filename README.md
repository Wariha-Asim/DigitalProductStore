# DigitalProductStore
DigitalProductStore is a powerful Django-based e-commerce platform designed to deliver a comprehensive online shopping experience. It combines robust product management features with secure user authentication and an intuitive admin panel, making it an ideal choice for deploying scalable online stores.

# Features
Product Management: Seamlessly view, add, update, and delete products.
User Authentication: Secure user registration, login, and password reset functionalities.
Admin Panel: Comprehensive tools for managing products, user accounts, and orders.
Shopping Cart: Users can easily add products to their cart and proceed to checkout.
Order Processing: Efficient handling of user orders and transactions.
Key Technologies
Django: The web framework used to build the project.
MySQL: The database system for storing product and user data.
SMTP: Email configuration for user notifications and password management.
# Installation
Clone the Repository:


git clone https://github.com/Wariha-Asim/DigitalProductStore.git
cd DigitalProductStore
Set Up Virtual Environment:


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

pip install -r requirements.txt
Configure Database:

Update DATABASES settings in settings.py with your database credentials.
Apply Migrations:

python manage.py migrate
Create Superuser:

python manage.py createsuperuser
Run the Server:


python manage.py runserver
Access the Application:

Open your browser and navigate to http://127.0.0.1:8000 to view the store.
Access the admin panel at http://127.0.0.1:8000/admin.
Usage
Product Management: Admins can manage products through the admin interface.
User Interaction: Users can register, log in, and reset their passwords.
Shopping: Users can browse products, add them to their cart, and complete purchases.
# Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.



# Acknowledgements
Django documentation
MySQL community
Open-source libraries and tools
