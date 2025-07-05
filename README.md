# SIRIUS - Strategic Intelligence Relationship & Interactive Universal System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Django 4.2](https://img.shields.io/badge/django-4.2-green.svg)](https://docs.djangoproject.com/en/4.2/)
[![Vue.js 3](https://img.shields.io/badge/vue.js-3.x-brightgreen.svg)](https://vuejs.org/)

> A sophisticated legal structure design and analysis platform for international tax optimization and compliance.

![SIRIUS Interface](https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=SIRIUS+Canvas+Interface)

## 🌟 Overview

SIRIUS is a professional-grade web application that enables legal professionals, tax advisors, and corporate structuring specialists to design, visualize, and analyze complex international legal structures through an intuitive drag-and-drop interface.

### ✨ Key Features

- **🎨 Interactive Canvas**: Drag-and-drop interface for building legal structures
- **💰 Real-time Cost Analysis**: Dynamic pricing with multiple scenarios
- **✅ Compliance Validation**: Instant regulatory checking and conflict detection
- **📄 Professional Reports**: Comprehensive PDF generation with executive summaries
- **🏗️ Template System**: Pre-configured structures for common use cases
- **🔧 Advanced Tools**: Zoom, pan, grid snap, undo/redo functionality

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/carlossilvatbh/sirius-system.git
   cd sirius-system
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python manage.py migrate
   python manage.py populate_initial_data
   ```

5. **Run the application**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open http://localhost:8000/ in your browser
   - Start designing legal structures immediately!

## 🏗️ Architecture

SIRIUS is built with a modern, scalable architecture:

```
Frontend (Vue.js 3 + Tailwind CSS)
           ↕
Backend (Django + Python 3.11)
           ↕
Database (SQLite/PostgreSQL)
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Vue.js 3, Tailwind CSS | Interactive user interface |
| **Backend** | Django 4.2, Python 3.11 | Business logic and API |
| **Database** | SQLite (dev), PostgreSQL (prod) | Data persistence |
| **PDF Generation** | ReportLab | Professional report creation |
| **Canvas** | HTML5 Canvas, Vue.js | Interactive design workspace |

## 📊 Legal Structures

SIRIUS includes 7 professionally researched legal structures:

| Structure | Jurisdiction | Base Cost | Implementation Time |
|-----------|--------------|-----------|-------------------|
| **Bahamas DAO SAC** | Bahamas | $15,000 | 45 days |
| **BTS Vault** | Multiple | $25,000 | 60 days |
| **Fund Token as a Service** | Multiple | $45,000 | 120 days |
| **Nacionalização (CNPJ Brasil)** | Brazil | $5,000 | 60 days |
| **Wyoming Corporation** | Wyoming, USA | $12,000 | 30 days |
| **Wyoming DAO LLC** | Wyoming, USA | $8,000 | 21 days |
| **Wyoming Statutory Foundation** | Wyoming, USA | $35,000 | 90 days |

## 💼 Use Cases

### For Legal Professionals
- Design complex international structures
- Validate regulatory compliance
- Generate client presentations
- Calculate implementation costs

### For Tax Advisors
- Optimize tax structures
- Analyze cross-border implications
- Compare jurisdiction benefits
- Document planning strategies

### For Corporate Specialists
- Structure corporate hierarchies
- Plan asset protection strategies
- Design succession frameworks
- Optimize operational efficiency

## 🎯 Pricing Scenarios

SIRIUS offers three pricing scenarios to match different service levels:

### Basic Scenario (10% margin)
- Base structure costs only
- Self-service implementation
- Ideal for simple structures

### Complete Scenario (15% margin)
- Base costs + consultation + documentation
- Professional service level
- Includes regulatory guidance

### Premium Scenario (20% margin)
- All Complete features + premium support
- White-glove service
- Priority implementation and ongoing support

## 📱 Screenshots

### Main Canvas Interface
![Canvas Interface](https://via.placeholder.com/600x400/4F46E5/FFFFFF?text=Interactive+Canvas)

### Cost Analysis Panel
![Cost Analysis](https://via.placeholder.com/600x400/059669/FFFFFF?text=Real-time+Cost+Analysis)

### PDF Report Generation
![PDF Reports](https://via.placeholder.com/600x400/DC2626/FFFFFF?text=Professional+PDF+Reports)

## 🔧 API Documentation

SIRIUS provides a comprehensive REST API for integration:

### Key Endpoints

- `GET /api/estruturas/` - Retrieve all legal structures
- `GET /api/templates/` - Get pre-configured templates
- `POST /api/calcular-custos/` - Calculate structure costs
- `POST /api/validar-configuracao/` - Validate compliance
- `POST /api/generate-pdf/` - Generate PDF reports

### Example API Usage

```javascript
// Calculate costs for a configuration
const response = await fetch('/api/calcular-custos/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    elementos: [{ estrutura_id: 1, posicao: { x: 100, y: 100 } }],
    cenario: 'complete'
  })
});

const data = await response.json();
console.log(`Total cost: $${data.custo_total}`);
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Load application successfully
- [ ] Display all 7 legal structures
- [ ] Drag structures to canvas
- [ ] Calculate costs in real-time
- [ ] Generate PDF reports
- [ ] Apply pre-configured templates
- [ ] Validate compliance rules

### Running Tests

```bash
# Run Django tests
python manage.py test

# Check code quality
flake8 .

# Security check
bandit -r .
```

## 🚀 Deployment

### Heroku Deployment

```bash
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main
```

### Docker Deployment

```bash
# Build image
docker build -t sirius .

# Run container
docker run -p 8000:8000 sirius
```

See [deploy.md](deploy.md) for detailed deployment instructions.

## 📚 Documentation

- **[Technical Documentation](TECHNICAL_DOCUMENTATION.md)** - Comprehensive technical guide
- **[User Manual](USER_MANUAL.md)** - Complete user guide
- **[Deployment Guide](deploy.md)** - Production deployment instructions
- **[API Reference](TECHNICAL_DOCUMENTATION.md#api-documentation)** - REST API documentation

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/sirius-system.git

# Set up development environment
cd sirius-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run in development mode
python manage.py runserver
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check our comprehensive guides
- **Issues**: Report bugs via [GitHub Issues](https://github.com/carlossilvatbh/sirius-system/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/carlossilvatbh/sirius-system/discussions)

## 🏆 Acknowledgments

- Built with modern web technologies
- Inspired by professional legal structuring needs
- Designed for international compliance requirements
- Developed with security and scalability in mind

## 📈 Roadmap

### Version 1.1 (Q4 2025)
- [ ] Additional jurisdictions (Singapore, Luxembourg)
- [ ] Advanced reporting features
- [ ] Multi-user collaboration
- [ ] API rate limiting

### Version 1.2 (Q1 2026)
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Integration with legal databases
- [ ] Automated compliance monitoring

---

**SIRIUS** - Empowering legal professionals with intelligent structure design tools.

*For questions, support, or business inquiries, please contact us through GitHub Issues.*

