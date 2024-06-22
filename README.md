# Todowise
Projecto de integração de sistemas - ESTG Portalegre

Exemplo de utilização

# TotalStock

TotalStock is an inventory management system designed to help users track stock levels, manage items, and handle user roles within a site-based structure.

## Features

- **Search Items**: Search for items in stock.
- **Create Items**: Managers can create new items.
- **Manage Users**: Managers can assign roles and manage user permissions.
- **Stock Management**: Update stock levels, including entry and issuance of stock.
- **Role-Based Access**: Different functionalities are accessible based on user roles (Manager, Staff).

## Installation

### Prerequisites

- Python 3.8 or later
- Django 3.2 or later
- PostgreSQL or another preferred database system

### Setup

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/totalstock.git
    cd totalstock
    ```

2. **Create a virtual environment**:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  
   # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**:

    - Update the `DATABASES` setting in `totalstock/settings.py` with your database configuration.
    - Apply migrations:

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```sh
    python manage.py runserver
    ```

## Usage

1. **Log in as a superuser**: Navigate to `http://127.0.0.1:8000/admin` and log in with the superuser credentials.

2. **Add Sites and Locations**: Add sites and their respective locations through the admin interface.

3. **Add Items**: Managers can add items through the 'Create Item' page.

4. **Manage Users**: Assign roles to users through the 'Manage Users' page. Check the 'Manager' or 'Staff' groups as needed.

5. **Search and Manage Stock**: Use the 'Search Item' functionality to find items in stock, adjust quantities, and manage stock entries and issuance.

## Project Structure

- **totalstock/**: Main application folder
    - **migrations/**: Database migrations
    - **templates/**: HTML templates
    - **static/**: Static files (CSS, JavaScript, images)
    - **views.py**: View functions
    - **models.py**: Database models
    - **forms.py**: Form definitions
    - **urls.py**: URL configurations
    - **admin.py**: Django admin customizations
    - **settings.py**: Django settings

## To do
- **Notification system**: Notification sistem with filters by user hole.
- **MRP/**: Implement minimum resupply point in stock and option to create buy order.
- **Integration with logistics/**: Integrate app with tracking information of bought items and new receivings.
- **SignUp and forgot password implementations/**: Now, these functions are accessible only from the admin portal.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes and push the branch to your fork.
4. Create a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Contact

For questions or suggestions, please open an issue in the repository or contact the project maintainer:

- **GitHub**: [Gabrielbr955](https://github.com/yourusername)
