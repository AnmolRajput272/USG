# Unified Supplier System : Vendor Management

This project is a Django-based backend system for managing vendors, purchase orders, and historical performance metrics.

## Features

- **Vendors Management**: Create, update, retrieve, and delete vendor information, including name, contact details, and address.
- **Purchase Orders Management**: Create, update, retrieve, and delete purchase orders, including order details such as order date, expected delivery date, delivery date, items, quantity, and status.
- **Historical Performance Tracking**: Record and track historical performance metrics for vendors, including on-time delivery rate, quality rating average, average response time, and fulfillment rate.
- **Automatic Generation of Unique Identifiers**: Automatic generation of unique identifiers (purchase order numbers) for each purchase order.
- **API Integration**: Integration with Django REST Framework for building APIs to perform CRUD operations on vendors and purchase orders.
- **Signal Handling**: Signal handling for tracking changes to purchase orders and historical performance metrics, allowing for real-time updates and notifications.

## Installation

1. Clone the repository:

  ```bash
  git clone <repository_url>

2. Install dependencies:

  ```bash
  pip install -r requirements.txt

3. Apply database migrations:

  ```bash
  python manage.py makemigrations
  python manage.py migrate


4. Start the development server:

  ```bash
  python manage.py runserver

## Usage
1. python manage.py createsuperuser
2. Access the Django admin interface at http://localhost:8000/admin/ and use the superuser credentials to log in.
3. Use the Django admin interface to manage vendors, purchase orders, and historical performance metrics.
4. Use the provided APIs to perform CRUD operations on vendors and purchase orders. The API endpoints and their functionalities are documented in the API documentation.

## API documentation
The following APIs are available in this project:

# Vendors
GET /api/vendors/: Retrieve a list of all vendors.
GET /api/vendors/{id}/: Retrieve details of a specific vendor.
POST /api/vendors/: Create a new vendor.
PUT /api/vendors/{id}/: Update details of a specific vendor.
DELETE /api/vendors/{id}/: Delete a specific vendor.

# Purchase Orders
GET /api/purchase_orders/: Retrieve a list of all purchase orders.
GET /api/purchase_orders/{id}/: Retrieve details of a specific purchase order.
POST /api/purchase_orders/: Create a new purchase order.
PUT /api/purchase_orders/{id}/: Update details of a specific purchase order.
DELETE /api/purchase_orders/{id}/: Delete a specific purchase order.

## Future Additions
Integration
Integrate with external systems for data synchronization and automation.
Implement webhooks for real-time updates from external services.
Authentication and Authorization
Implement user authentication using JWT (JSON Web Tokens) for secure API access.
Implement role-based access control to restrict API endpoints based on user roles.
Ensure proper validation and verification of user permissions for sensitive operations.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to adjust the details and sections according to your project's specific requirements. Let me know if you need further customization!
