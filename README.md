# Django Address Book

A modern, responsive Django web application for managing contacts with full CRUD operations and API endpoints.

## Features

- **Full CRUD Operations**: Create, Read, Update, and Delete contacts
- **Responsive Design**: Modern UI with Bootstrap 5 and Font Awesome icons
- **API Endpoints**: RESTful API for AJAX operations
- **Admin Interface**: Django admin panel for contact management
- **Search & Filter**: Advanced filtering and search capabilities
- **Contact Details**: Comprehensive contact information including address, phone, email, and notes
- **Quick Actions**: Direct links to email, call, and map locations

## Technology Stack

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5, Font Awesome 6
- **Database**: SQLite (default), easily configurable for other databases
- **JavaScript**: Vanilla JS for API interactions

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd django-addressbook
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Main application: https://myfirstproject-production-f1f4.up.railway.app/
   - Admin interface: http://127.0.0.1:8000/admin/

## Usage

### Regular Web Interface

1. **View All Contacts**: Navigate to the home page to see all contacts
2. **Add New Contact**: Click "Add New Contact" button
3. **View Contact Details**: Click on a contact card or use the dropdown menu
4. **Edit Contact**: Use the edit button or dropdown menu
5. **Delete Contact**: Use the delete button (with confirmation)

### API Endpoints

The application provides RESTful API endpoints for AJAX operations:

- `GET /contacts/api/contacts/` - List all contacts
- `POST /contacts/api/contacts/create/` - Create a new contact
- `PUT /contacts/api/contacts/{id}/update/` - Update a contact
- `DELETE /contacts/api/contacts/{id}/delete/` - Delete a contact

### API Version (Frontend)

The application includes an "API Version" section that demonstrates AJAX functionality:

1. Click "Show API Version" button on the main page
2. Use "Load Contacts via API" to fetch contacts via AJAX
3. Use "Add Contact via API" to create contacts via AJAX
4. Edit and delete contacts directly from the API interface

## Contact Model

The Contact model includes the following fields:

- **first_name** (required): Contact's first name
- **last_name** (required): Contact's last name
- **email**: Contact's email address
- **phone**: Contact's phone number
- **address**: Full address text
- **city**: City name
- **state**: State/province name
- **zip_code**: ZIP/postal code
- **country**: Country name
- **notes**: Additional notes about the contact
- **created_at**: Timestamp when contact was created
- **updated_at**: Timestamp when contact was last updated

## Project Structure

```
django-addressbook/
├── addressbook_project/     # Main Django project
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── contacts/               # Contacts app
│   ├── models.py          # Contact model
│   ├── views.py           # View functions
│   ├── forms.py           # Contact form
│   ├── admin.py           # Admin configuration
│   ├── urls.py            # App URL patterns
│   └── templates/         # HTML templates
│       └── contacts/
│           ├── base.html              # Base template
│           ├── contact_list.html      # Contact list view
│           ├── contact_detail.html    # Contact detail view
│           ├── contact_form.html      # Add/edit form
│           └── contact_confirm_delete.html  # Delete confirmation
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Features in Detail

### Responsive Design
- Mobile-friendly interface using Bootstrap 5
- Card-based layout for contact display
- Dropdown menus for actions
- Modal dialogs for forms

### API Integration
- CSRF-exempt API endpoints for AJAX calls
- JSON responses for all API operations
- Error handling and success messages
- Real-time updates without page refresh

### User Experience
- Intuitive navigation with clear icons
- Confirmation dialogs for destructive actions
- Form validation with error messages
- Quick action buttons (email, call, map)

### Admin Interface
- Custom admin interface for Contact model
- Filtering and search capabilities
- Organized field sets for better data entry
- Read-only timestamps

## Customization

### Adding New Fields
1. Modify the Contact model in `contacts/models.py`
2. Create and run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Update forms, views, and templates as needed

### Styling
- Modify `contacts/templates/contacts/base.html` for global styles
- Add custom CSS in the `<style>` section
- Update Bootstrap classes for different themes

### API Extensions
- Add new API endpoints in `contacts/views.py`
- Update URL patterns in `contacts/urls.py`
- Extend JavaScript functions in templates

## Deployment

For production deployment:

1. **Update settings.py**:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use a production database (PostgreSQL, MySQL)
   - Set up static file serving

2. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Use a production WSGI server** (Gunicorn, uWSGI)

4. **Set up a reverse proxy** (Nginx, Apache)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository or contact the maintainer. 
