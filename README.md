# PYSYSTEM - Business Management System

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A complete business management system built with Python and Tkinter, following Clean Architecture principles.

## ✨ Features

- **Company Management** - Complete CRUD operations for companies
- **Product Management** - Inventory control with stock tracking  
- **Sales Order Management** - Order creation and item management
- **BrasilAPI Integration** - CEP lookup, CNPJ validation, and bank data
- **Data Persistence** - JSON-based storage system
- **Modern GUI** - Professional Tkinter interface with corporate theme

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/teusdrz/PYSYSTEM.git
   cd PYSYSTEM
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run_system.py
   ```

## 📁 Project Structure

```
PYSYSTEM/
├── src/
│   ├── application/          # Use cases and DTOs
│   │   ├── dtos/            # Data Transfer Objects
│   │   └── use_cases/       # Business logic
│   ├── domain/              # Core business entities
│   │   ├── entities/        # Domain models
│   │   ├── repositories/    # Repository interfaces
│   │   └── services/        # Domain services
│   ├── infrastructure/      # External concerns
│   │   ├── external_services/  # API integrations
│   │   ├── persistence/     # Data storage
│   │   └── report_generators/  # Report services
│   ├── presentation/        # UI layer
│   │   ├── controllers/     # Application controllers
│   │   └── gui/            # Tkinter interface
│   └── shared/             # Common utilities
├── data/                   # JSON data files
├── assets/                # Icons and resources
├── tests/                 # Test suite
└── requirements.txt       # Python dependencies
```

## 🏗️ Architecture

This project follows **Clean Architecture** principles:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and application services  
- **Infrastructure Layer**: External services and data persistence
- **Presentation Layer**: User interface and controllers

## 💻 Usage

### Main Features

1. **Companies**: Manage customer and supplier information
2. **Products**: Track inventory with stock levels and pricing
3. **Sales Orders**: Create orders and manage order items
4. **BrasilAPI**: Automatic address lookup and data validation

### Navigation

- Use the tab interface to switch between different modules
- All forms include validation and error handling
- Data is automatically saved to JSON files in the `data/` directory

## 🧪 Testing

The project includes comprehensive test suites:

```bash
# Run ultra comprehensive tests
python ultra_comprehensive_gui_tests.py

# Run automated GUI tests  
python automated_gui_tests.py
```

**Test Results**: 82.3% success rate (93/113 tests passing)

## 🔧 Configuration

The system uses JSON files for data storage located in the `data/` directory:

- `companies.json` - Company data
- `products.json` - Product catalog  
- `sales_orders.json` - Sales order records

## 📊 API Integration

**BrasilAPI Integration**:
- CEP address lookup
- CNPJ validation  
- Bank information retrieval
- Product categorization suggestions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Matheus Souza**  
- GitHub: [@teusdrz](https://github.com/teusdrz)

## 📈 Status

- ✅ Core functionality implemented
- ✅ GUI interface complete
- ✅ Data persistence working
- ✅ API integration functional
- ⚠️ Minor optimizations pending

---

*Built with ❤️ using Python and Clean Architecture principles*
