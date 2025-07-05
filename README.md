# SIRIUS - Strategic Intelligence Relationship & Interactive Universal System

## Overview

SIRIUS is a comprehensive web-based software solution designed for the visual assembly of digital legal structures. The system provides an intuitive interface for configuring, visualizing, and pricing complex legal structures, specifically tailored for corporate structures and international tax planning.

## Features

### Core Functionality
- **Visual Drag-and-Drop Canvas**: Interactive interface for assembling legal structures
- **Real-time Validation**: Intelligent validation system with contextual alerts
- **Dynamic Pricing**: Multi-scenario cost calculation (Basic, Complete, Premium)
- **Template System**: Pre-configured templates organized by industry sector
- **Document Generation**: Professional PDF generation with detailed reports
- **Tax Impact Analysis**: Comprehensive tax implications for multiple jurisdictions

### Supported Legal Structures
1. **Digital Offshore Basic** (BDAO SAC + Wyoming DAO LLC)
2. **BTS Vault** (Basket Token Standard ERC-721)
3. **Decentralized Legacy Token** (Wyoming Statutory Foundation)
4. **Wyoming Corporations**
5. **Nationalization** (Brazil CNPJ)
6. **Fund Token as a Service**

## Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **Database**: SQLite (development) / PostgreSQL (production)
- **Language**: Python 3.11+

### Frontend
- **Framework**: Vue.js 3 (CDN)
- **Styling**: Tailwind CSS
- **Canvas**: Vue Flow for drag-and-drop functionality
- **PDF Generation**: html2canvas + jsPDF

### Additional Libraries
- **Whitenoise**: Static file serving
- **Gunicorn**: WSGI HTTP Server
- **Pillow**: Image processing

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/sirius-system.git
   cd sirius-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load initial data**
   ```bash
   python manage.py loaddata initial_structures.json
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main Canvas: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/

## Project Structure

```
sirius-system/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                  # SQLite database (development)
├── sirius_project/             # Django project settings
│   ├── __init__.py
│   ├── settings.py             # Main configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI configuration
├── estruturas_app/             # Main application
│   ├── models.py               # Data models
│   ├── views.py                # View functions
│   ├── urls.py                 # App URL routing
│   ├── admin.py                # Admin configuration
│   └── migrations/             # Database migrations
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── canvas.html             # Main canvas interface
│   └── admin_estruturas.html   # Admin interface
├── static/                     # Static files
│   ├── css/
│   │   └── style.css           # Custom styles
│   ├── js/
│   │   ├── vue.min.js          # Vue.js library
│   │   ├── vue-flow.min.js     # Vue Flow library
│   │   └── app.js              # Main application logic
│   └── images/                 # Image assets
└── docs/                       # Documentation
    ├── technical-spec.md       # Technical specification
    └── user-manual.md          # User manual
```

## Usage

### Basic Workflow

1. **Access the Canvas**: Navigate to the main interface
2. **Select Structures**: Choose from the library of legal structures
3. **Drag and Drop**: Place structures on the canvas
4. **Configure Connections**: Establish relationships between structures
5. **Review Validation**: Check real-time validation alerts
6. **Calculate Costs**: Review pricing in different scenarios
7. **Generate Documents**: Export professional PDF reports
8. **Save Templates**: Store configurations for future use

### Key Features

#### Drag-and-Drop Interface
- Intuitive visual assembly of legal structures
- Smart connection system with validation
- Zoom and pan capabilities
- Undo/redo functionality

#### Real-time Validation
- Compatibility checking between structures
- Jurisdiction-specific alerts
- Tax implication warnings
- Compliance requirement notifications

#### Pricing Scenarios
- **Basic**: Essential setup costs only
- **Complete**: Full operational requirements
- **Premium**: Includes strategic consulting

#### Template System
- Industry-specific pre-configurations
- Technology sector templates
- Real estate investment structures
- Trading optimization setups
- Family office configurations

## API Endpoints

### Structure Management
- `GET /estruturas/` - List all available structures
- `GET /estrutura/<id>/` - Get specific structure details

### Validation
- `POST /validar/` - Validate current configuration

### Templates
- `GET /templates/` - List available templates
- `POST /salvar-template/` - Save new template
- `GET /template/<id>/` - Load specific template

### Document Generation
- `POST /gerar-pdf/` - Generate PDF report

## Development

### Running Tests
```bash
python manage.py test
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

### Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

## Deployment

### Production Settings
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up PostgreSQL database
4. Configure static file serving
5. Set up HTTPS

### Environment Variables
```bash
export SECRET_KEY="your-secret-key"
export DEBUG=False
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
```

### Using Gunicorn
```bash
gunicorn sirius_project.wsgi:application --bind 0.0.0.0:8000
```

## Contributing

### Development Guidelines
1. Follow PEP 8 style guidelines
2. Write comprehensive tests
3. Update documentation
4. Use meaningful commit messages

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Code review and merge

## Legal Structures Documentation

### Digital Offshore Basic
Combines Bahamas DAO SAC with Wyoming DAO LLC for comprehensive international tax optimization.

### BTS Vault
Blockchain-based asset protection using ERC-721 standard with wallet-as-a-token functionality.

### Decentralized Legacy Token
Wyoming Statutory Foundation providing advanced asset protection and succession planning.

### Wyoming Corporations
Versatile corporate structures for various business purposes and tax optimization strategies.

### Nationalization
Process for obtaining Brazilian CNPJ for foreign corporations.

### Fund Token as a Service
Investment fund structures using Digital Offshore framework.

## Support

### Documentation
- Technical Specification: `/docs/technical-spec.md`
- User Manual: `/docs/user-manual.md`
- API Documentation: `/docs/api.md`

### Contact
- Email: support@sirius-system.com
- Documentation: https://docs.sirius-system.com
- Issues: https://github.com/your-username/sirius-system/issues

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 1.0.0 (2025-01-07)
- Initial release
- Core drag-and-drop functionality
- Real-time validation system
- Multi-scenario pricing
- PDF generation
- Template management
- Six legal structure types

## Acknowledgments

- Django community for the excellent framework
- Vue.js team for the reactive frontend framework
- Legal experts who provided structure specifications
- Beta testers and early adopters

