# SIRIUS - Technical Documentation

## Strategic Intelligence Relationship & Interactive Universal System

**Version:** 1.0.0  
**Author:** Manus AI Development Team  
**Date:** July 2025  
**License:** MIT  

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Installation Guide](#installation-guide)
5. [API Documentation](#api-documentation)
6. [Frontend Components](#frontend-components)
7. [Database Schema](#database-schema)
8. [Business Logic](#business-logic)
9. [Security Considerations](#security-considerations)
10. [Performance Optimization](#performance-optimization)
11. [Testing Strategy](#testing-strategy)
12. [Deployment Guide](#deployment-guide)
13. [Troubleshooting](#troubleshooting)
14. [Contributing](#contributing)

---

## System Overview

SIRIUS is a sophisticated legal structure design and analysis platform that enables users to create, visualize, and analyze complex international legal structures through an intuitive drag-and-drop interface. The system provides real-time cost calculations, compliance validation, and professional PDF report generation.

### Key Features

- **Interactive Canvas**: Drag-and-drop interface for building legal structures
- **Real-time Validation**: Instant compliance checking and conflict detection
- **Cost Analysis**: Dynamic pricing with multiple scenarios (Basic, Complete, Premium)
- **Professional Reports**: Comprehensive PDF generation with executive summaries
- **Template System**: Pre-configured structures for common use cases
- **Advanced Canvas Tools**: Zoom, pan, grid snap, undo/redo functionality

### Target Users

- Legal professionals specializing in international structures
- Tax advisors and consultants
- Family office managers
- Corporate structuring specialists
- Compliance officers

---

## Architecture

SIRIUS follows a modern web application architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Vue.js 3)    │◄──►│   (Django)      │◄──►│   (SQLite)      │
│   Tailwind CSS  │    │   Python 3.11   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Component Architecture

- **Presentation Layer**: Vue.js 3 with Tailwind CSS for responsive UI
- **Business Logic Layer**: Django views and models handling core functionality
- **Data Access Layer**: Django ORM with SQLite database
- **Integration Layer**: RESTful APIs for frontend-backend communication

---

## Technology Stack

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 4.2.7 | Web framework and ORM |
| Python | 3.11.0 | Core programming language |
| ReportLab | 4.0.7 | PDF generation |
| Pillow | 10.1.0 | Image processing |
| WhiteNoise | 6.6.0 | Static file serving |
| Gunicorn | 21.2.0 | WSGI HTTP Server |

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Vue.js | 3.x | Progressive JavaScript framework |
| Tailwind CSS | 3.x | Utility-first CSS framework |
| html2canvas | 1.4.1 | Canvas screenshot capture |

### Development Tools

- Git for version control
- GitHub for repository hosting
- SQLite for development database
- Django Admin for data management

---

## Installation Guide

### Prerequisites

- Python 3.11 or higher
- Git
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/carlossilvatbh/sirius-system.git
   cd sirius-system
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py populate_initial_data
   ```

5. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access Application**
   - Main Application: http://localhost:8000/
   - Admin Interface: http://localhost:8000/admin/

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
Currently using Django's CSRF protection. All POST requests require CSRF token.

### Endpoints

#### 1. Get Legal Structures
```http
GET /api/estruturas/
```

**Response:**
```json
[
  {
    "id": 1,
    "codigo": "BDAO_SAC",
    "nome": "Bahamas DAO SAC",
    "descricao": "Segregated Account Company in Bahamas...",
    "custo_base": 15000.00,
    "tempo_implementacao": 45,
    "jurisdicao": "Bahamas",
    "categoria": "DAO",
    "ativo": true
  }
]
```

#### 2. Get Templates
```http
GET /api/templates/
```

**Response:**
```json
[
  {
    "id": 1,
    "nome": "Tech Startup Basic",
    "descricao": "Basic structure for technology startups...",
    "configuracao": {...},
    "ativo": true
  }
]
```

#### 3. Calculate Costs
```http
POST /api/calcular-custos/
```

**Request Body:**
```json
{
  "elementos": [
    {
      "estrutura_id": 1,
      "posicao": {"x": 100, "y": 100}
    }
  ],
  "cenario": "complete"
}
```

**Response:**
```json
{
  "custo_total": 17250.00,
  "breakdown": {
    "base_cost": 15000.00,
    "consultoria": 1500.00,
    "documentacao": 500.00,
    "margem": 250.00
  },
  "tempo_total": 45
}
```

#### 4. Validate Configuration
```http
POST /api/validar-configuracao/
```

**Request Body:**
```json
{
  "elementos": [
    {
      "estrutura_id": 1,
      "posicao": {"x": 100, "y": 100}
    }
  ]
}
```

**Response:**
```json
{
  "valido": true,
  "alertas": [
    {
      "tipo": "INFO",
      "mensagem": "Structure complies with US regulations",
      "jurisdicao": "US"
    }
  ]
}
```

#### 5. Generate PDF Report
```http
POST /api/generate-pdf/
```

**Request Body:**
```json
{
  "configuration": {
    "name": "Custom Configuration",
    "elementos": [...],
    "custo_total": 17250.00,
    "tempo_total": 45
  },
  "canvas_image": "data:image/png;base64,..."
}
```

**Response:** Binary PDF file download

---

## Frontend Components

### Vue.js Application Structure

The frontend is built as a single-page application using Vue.js 3 with the Composition API pattern.

#### Main Components

1. **SiriusApp** - Root application component
2. **StructureLibrary** - Sidebar with draggable structures
3. **Canvas** - Main design area with drag-and-drop functionality
4. **ControlPanel** - Tools and actions (undo, redo, grid, etc.)
5. **CostPanel** - Real-time cost calculations and scenarios
6. **ValidationPanel** - Compliance alerts and warnings

#### Key Features Implementation

**Drag and Drop System:**
```javascript
// Simplified drag implementation
onDragStart(event, structure) {
  event.dataTransfer.setData('application/json', JSON.stringify(structure));
}

onDrop(event) {
  const structure = JSON.parse(event.dataTransfer.getData('application/json'));
  this.addToCanvas(structure, { x: event.offsetX, y: event.offsetY });
}
```

**Real-time Cost Calculation:**
```javascript
async calcularTotais() {
  const response = await fetch('/api/calcular-custos/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      elementos: this.elementosCanvas,
      cenario: this.cenarioSelecionado
    })
  });
  const data = await response.json();
  this.custoTotal = data.custo_total;
  this.analiseDetalhada = data.breakdown;
}
```

---

## Database Schema

### Core Models

#### Estrutura (Legal Structure)
```python
class Estrutura(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    custo_base = models.DecimalField(max_digits=12, decimal_places=2)
    tempo_implementacao = models.IntegerField()  # days
    jurisdicao = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### RegraValidacao (Validation Rules)
```python
class RegraValidacao(models.Model):
    estrutura_origem = models.ForeignKey(Estrutura, on_delete=models.CASCADE)
    estrutura_destino = models.ForeignKey(Estrutura, on_delete=models.CASCADE)
    tipo_relacao = models.CharField(max_length=50)
    compativel = models.BooleanField()
    observacoes = models.TextField(blank=True)
```

#### Template (Pre-configured Structures)
```python
class Template(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    configuracao = models.JSONField()
    publico_alvo = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
```

#### ConfiguracaoSalva (Saved Configurations)
```python
class ConfiguracaoSalva(models.Model):
    nome = models.CharField(max_length=200)
    configuracao = models.JSONField()
    custo_total = models.DecimalField(max_digits=12, decimal_places=2)
    tempo_total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Database Relationships

```
Estrutura (1) ←→ (N) RegraValidacao ←→ (1) Estrutura
Estrutura (N) ←→ (N) Template (via JSONField)
ConfiguracaoSalva (1) ←→ (N) Estrutura (via JSONField)
```

---

## Business Logic

### Cost Calculation Engine

The system implements a sophisticated cost calculation engine with three pricing scenarios:

#### Pricing Scenarios

1. **Basic Scenario** (10% margin)
   - Base structure costs only
   - Minimal markup for basic service

2. **Complete Scenario** (15% margin)
   - Base costs + consultation fees
   - Documentation and filing fees
   - Standard service level

3. **Premium Scenario** (20% margin)
   - All Complete features
   - Premium consultation and support
   - Priority processing and dedicated account management

#### Cost Calculation Formula

```python
def calculate_total_cost(structures, scenario):
    base_cost = sum(s.custo_base for s in structures)
    
    if scenario == 'basic':
        return base_cost * 1.10
    elif scenario == 'complete':
        consultoria = base_cost * 0.10
        documentacao = len(structures) * 500
        return (base_cost + consultoria + documentacao) * 1.15
    elif scenario == 'premium':
        consultoria = base_cost * 0.15
        documentacao = len(structures) * 750
        suporte = base_cost * 0.05
        return (base_cost + consultoria + documentacao + suporte) * 1.20
```

### Validation Engine

The validation system checks for:

1. **Jurisdictional Compatibility**: Ensures structures can legally coexist
2. **Regulatory Compliance**: Validates against known regulatory requirements
3. **Tax Optimization**: Identifies potential tax conflicts or opportunities
4. **Operational Feasibility**: Checks for practical implementation issues

#### Validation Levels

- **INFO**: Informational notices and recommendations
- **WARNING**: Potential issues that should be reviewed
- **ERROR**: Critical conflicts that must be resolved

---

## Security Considerations

### CSRF Protection
All state-changing operations are protected by Django's CSRF middleware.

### Input Validation
- All user inputs are validated and sanitized
- JSON payloads are validated against expected schemas
- File uploads (if any) are restricted by type and size

### Data Privacy
- No personally identifiable information is stored without explicit consent
- Configuration data is associated with sessions, not users
- PDF reports contain only structure information, no personal data

### Access Control
- Admin interface requires authentication
- API endpoints use session-based authentication
- Rate limiting should be implemented for production use

---

## Performance Optimization

### Frontend Optimizations

1. **Lazy Loading**: Components loaded on demand
2. **Debounced Calculations**: Cost calculations debounced to prevent excessive API calls
3. **Efficient DOM Updates**: Vue.js reactivity system minimizes DOM manipulation
4. **Image Optimization**: Canvas screenshots optimized for PDF generation

### Backend Optimizations

1. **Database Queries**: Optimized with select_related and prefetch_related
2. **Caching**: Static data cached in memory
3. **PDF Generation**: Asynchronous processing for large reports
4. **Static Files**: Served efficiently with WhiteNoise

### Database Optimizations

```python
# Optimized query examples
structures = Estrutura.objects.select_related('categoria').filter(ativo=True)
templates = Template.objects.prefetch_related('estruturas').filter(ativo=True)
```

---

## Testing Strategy

### Manual Testing Checklist

#### Core Functionality
- [ ] Load application successfully
- [ ] Display all 7 legal structures in sidebar
- [ ] Drag structures to canvas
- [ ] Calculate costs in real-time
- [ ] Switch between pricing scenarios
- [ ] Generate PDF reports
- [ ] Apply pre-configured templates

#### Advanced Features
- [ ] Undo/Redo operations
- [ ] Grid snap functionality
- [ ] Zoom and pan canvas
- [ ] Save and load configurations
- [ ] Validation alerts display correctly

#### Cross-browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

#### Responsive Design
- [ ] Desktop (1920x1080)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

### Automated Testing

Future implementations should include:

1. **Unit Tests**: Django model and view testing
2. **Integration Tests**: API endpoint testing
3. **Frontend Tests**: Vue.js component testing
4. **End-to-End Tests**: Full user workflow testing

---

## Deployment Guide

### Production Environment Setup

#### Requirements
- Python 3.11+
- PostgreSQL (recommended for production)
- Redis (for caching)
- Nginx (reverse proxy)
- SSL certificate

#### Environment Configuration

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/sirius_db
REDIS_URL=redis://localhost:6379/0
```

#### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "sirius_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /app/staticfiles/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Troubleshooting

### Common Issues

#### 1. Structures Not Loading
**Symptoms**: Empty sidebar, no structures visible
**Causes**: 
- Database not populated
- API endpoint errors
- JavaScript errors

**Solutions**:
```bash
# Repopulate database
python manage.py populate_initial_data

# Check API endpoints
curl http://localhost:8000/api/estruturas/

# Check browser console for JavaScript errors
```

#### 2. PDF Generation Fails
**Symptoms**: No PDF download, error messages
**Causes**:
- Missing reportlab dependency
- Canvas capture issues
- Server memory limitations

**Solutions**:
```bash
# Reinstall reportlab
pip install --upgrade reportlab

# Check server logs
python manage.py runserver --verbosity=2
```

#### 3. Canvas Performance Issues
**Symptoms**: Slow drag-and-drop, laggy interactions
**Causes**:
- Too many elements on canvas
- Browser performance limitations
- Memory leaks

**Solutions**:
- Limit canvas elements
- Clear browser cache
- Use Chrome DevTools to identify performance bottlenecks

### Debug Mode

Enable debug mode for detailed error information:

```python
# settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Commit with descriptive messages
5. Push to your fork: `git push origin feature/new-feature`
6. Create a Pull Request

### Code Standards

#### Python/Django
- Follow PEP 8 style guidelines
- Use Django best practices
- Write docstrings for all functions and classes
- Maintain test coverage above 80%

#### JavaScript/Vue.js
- Use ES6+ features
- Follow Vue.js style guide
- Use meaningful variable and function names
- Comment complex logic

#### CSS/Tailwind
- Use Tailwind utility classes
- Avoid custom CSS when possible
- Maintain responsive design principles

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types: feat, fix, docs, style, refactor, test, chore

Examples:
```
feat(canvas): add grid snap functionality
fix(api): resolve cost calculation edge case
docs(readme): update installation instructions
```

---

## Conclusion

SIRIUS represents a comprehensive solution for legal structure design and analysis, combining modern web technologies with sophisticated business logic to deliver a professional-grade application. The system's modular architecture, comprehensive API, and intuitive interface make it suitable for both individual practitioners and enterprise deployments.

For additional support or questions, please refer to the GitHub repository issues section or contact the development team.

---

**Document Version**: 1.0.0  
**Last Updated**: July 2025  
**Next Review**: October 2025

