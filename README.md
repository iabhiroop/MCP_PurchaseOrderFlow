# MCP Purchase Order Agent

A comprehensive Model Context Protocol (MCP) server for automated purchase order management, processing, and workflow automation. This server provides a complete suite of tools for handling purchase orders from email monitoring to document generation and database management.

![MCP](https://img.shields.io/badge/MCP-Compatible-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

### Core Capabilities
- **📧 Email Monitoring**: Automatically fetch and process purchase orders from Gmail
- **📄 Document Processing**: OCR and AI-powered extraction of purchase order data from PDFs
- **📝 Document Generation**: Create professional PDF purchase orders using LaTeX
- **📦 Inventory Management**: Track stock levels and identify restock needs
- **💰 Financial Validation**: Automated approval workflows and budget checking
- **🗄️ Database Management**: Store and retrieve purchase order records in MongoDB
- **✉️ Email Automation**: Send professional purchase order emails with attachments
- **📋 Queue Management**: Manage purchase request workflows
- **📊 Report Generation**: Create and save inventory and status reports

### Available Tools
1. **generate_purchase_order** - Generate PDF purchase order documents
2. **generate_latex_po** - Generate LaTeX purchase order documents
3. **validate_po_items** - Validate purchase order items format
4. **create_sample_po_data** - Create sample purchase order data for testing
5. **fetch_emails** - Fetch unread emails with attachments from Gmail
6. **parse_document** - Parse documents and extract structured purchase order data
7. **get_financial_data** - Get financial data and approval status
8. **manage_purchase_queue** - Manage purchase request queue operations
9. **manage_po_records** - Execute PO record management actions
10. **generate_po_email** - Generate and send purchase order emails to suppliers
11. **analyze_inventory** - Analyze inventory and get restock information
12. **save_report** - Save data to text files
13. **send_response_email** - Send email responses with custom subject and body

## 📋 Prerequisites

- **Python 3.11+**
- **MongoDB** (running on localhost:27017)
- **LaTeX distribution** (for PDF generation)
- **Gmail account** with app-specific password
- **Google AI API key** (for document processing)

## 🛠️ Installation

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd mcppoagent

# Create virtual environment (recommended)
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### 3. Environment Configuration
Create a `.env` file in the project root:

```env
# Gmail Configuration
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-specific-password

# Google AI Configuration
GOOGLE_API_KEY=your-google-ai-api-key

# MongoDB Configuration (optional, defaults shown)
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=purchase_orders

# Server Configuration
MCP_SERVER_PORT=8099
TRANSPORT_MODE=stdio  # Options: stdio, sse, streamable-http

# Company Information
COMPANY_NAME=Your Company Name
COMPANY_ADDRESS=Your Company Address
COMPANY_EMAIL=company@example.com
```

### 4. External Dependencies

#### MongoDB Setup
```bash
# Install MongoDB Community Edition
# Visit: https://www.mongodb.com/try/download/community

# Start MongoDB service
# Windows: Start as Windows Service
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

#### LaTeX Setup
```bash
# Windows (MiKTeX)
# Download from: https://miktex.org/download

# macOS (MacTeX)
brew install --cask mactex

# Ubuntu/Debian
sudo apt-get install texlive-full

# Arch Linux
sudo pacman -S texlive-most
```

## 🚀 Usage

### Running the MCP Server

#### Option 1: Standard I/O Transport (Default)
```bash
python mcppoagent.py
```

#### Option 2: SSE Transport (HTTP)
```bash
# Set environment variable
export TRANSPORT_MODE=sse
python mcppoagent.py
```

#### Option 3: StreamableHTTP Transport
```bash
# Set environment variable
export TRANSPORT_MODE=streamable-http
python mcppoagent.py
```

### Connecting to MCP Clients

#### Claude Desktop Integration
Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "potool": {
      "command": "python",
      "args": ["path/to/mcppoagent/mcppoagent.py"],
      "env": {
        "GMAIL_EMAIL": "your-email@gmail.com",
        "GMAIL_APP_PASSWORD": "your-app-password",
        "GOOGLE_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### Other MCP Clients
For HTTP-based transports, connect to:
- **SSE**: `http://localhost:8099/sse`
- **StreamableHTTP**: `http://localhost:8099`

## 📖 Tool Documentation

### Email & Document Processing

#### `fetch_emails()`
Fetches unread emails with attachments from Gmail inbox.
```python
# Returns JSON with emails containing attachments
result = await fetch_emails()
```

#### `parse_document(file_path, action="extract_po_data")`
Parses documents and extracts structured purchase order data.
```python
# Extract PO data from PDF
result = await parse_document("/path/to/po.pdf", "extract_po_data")
```

### Purchase Order Generation

#### `generate_purchase_order(supplier_name, items, **kwargs)`
Generates PDF purchase order documents.
```python
items = [
    {
        "item_code": "ITM001",
        "description": "Widget A",
        "quantity": 100,
        "unit_price": 25.50,
        "uom": "pcs",
        "urgency": "high"
    }
]
result = await generate_purchase_order("ABC Suppliers", items)
```

#### `generate_latex_po(supplier_name, items, **kwargs)`
Generates LaTeX purchase order documents.
```python
result = await generate_latex_po(
    "ABC Suppliers",
    items,
    delivery_date="2025-08-15",
    contact_email="supplier@example.com"
)
```

### Inventory & Financial Management

#### `analyze_inventory(analysis_type, category="", urgency_level="all")`
Analyzes inventory and provides restock information.
```python
# Check items needing restock
result = await analyze_inventory("restock_needed", urgency_level="critical")
```

#### `get_financial_data(query_type, amount=0.0)`
Gets financial data and approval status.
```python
# Check approval limits
result = await get_financial_data("approval_limits", 5000.0)
```

### Queue & Record Management

#### `manage_purchase_queue(action, request_data=None, request_id=None)`
Manages purchase request queue operations.
```python
# Add to queue
result = await manage_purchase_queue("add_to_queue", request_data)

# Get pending requests
result = await manage_purchase_queue("get_pending")
```

#### `manage_po_records(action, **kwargs)`
Manages PO record database operations.
```python
# Record a single PO
result = await manage_po_records("record_single_po", po_data=po_data)
```

### Email Communication

#### `generate_po_email(action, supplier_email, supplier_name, **kwargs)`
Generates and sends purchase order emails.
```python
result = await generate_po_email(
    "send_po_email",
    "supplier@example.com",
    "ABC Suppliers",
    po_number="PO-001",
    po_file_path="/path/to/po.pdf"
)
```

#### `send_response_email(subject, body, recipient_email, **kwargs)`
Sends custom email responses.
```python
result = await send_response_email(
    "PO Confirmation",
    "Your purchase order has been received.",
    "supplier@example.com"
)
```

### Utilities

#### `validate_po_items(items)`
Validates purchase order items format.
```python
result = await validate_po_items(items)
```

#### `create_sample_po_data(item_count=3, supplier_name="ABC Suppliers")`
Creates sample purchase order data for testing.
```python
result = await create_sample_po_data(5, "Test Supplier")
```

#### `save_report(file_path, data, **kwargs)`
Saves data to text files.
```python
result = await save_report("/path/to/report.txt", report_data, append=True)
```

## 🔧 Configuration Options

### Server Configuration
- **Port**: Set via `port` parameter in FastMCP constructor (default: 8099)
- **Transport**: Configure via `TRANSPORT_MODE` environment variable
- **Debug**: Enable debug mode for development

### Email Configuration
- **Gmail Integration**: Requires app-specific password
- **Email Templates**: Customizable email templates for different scenarios
- **Attachment Handling**: Automatic PDF attachment processing

### Database Configuration
- **MongoDB**: Default connection to localhost:27017
- **Collections**: Automatic collection creation for PO records
- **Indexing**: Optimized indexes for query performance

### Document Processing
- **OCR Engine**: PaddleOCR for text extraction
- **AI Processing**: Google Generative AI for data extraction
- **LaTeX**: Full LaTeX document generation support

## 🛡️ Security Considerations

- **Environment Variables**: Store sensitive data in `.env` file
- **Gmail App Passwords**: Use app-specific passwords, not account passwords
- **API Keys**: Secure storage of Google AI API keys
- **Database Access**: Configure MongoDB authentication in production
- **File Permissions**: Ensure proper file system permissions

## 🧪 Testing

### Sample Data Generation
```python
# Generate test data
result = await create_sample_po_data(3, "Test Supplier")

# Validate generated items
result = await validate_po_items(sample_items)
```

### Manual Testing
```python
# Test email fetching
emails = await fetch_emails()

# Test document parsing
parsed = await parse_document("test_po.pdf")

# Test PO generation
po = await generate_purchase_order("Test Corp", sample_items)
```

## 🐛 Troubleshooting

### Common Issues

#### MongoDB Connection Errors
```bash
# Check MongoDB status
mongosh --eval "db.adminCommand('ismaster')"

# Restart MongoDB service
sudo systemctl restart mongod
```

#### Gmail Authentication Errors
- Verify app-specific password is correct
- Ensure 2FA is enabled on Gmail account
- Check GMAIL_EMAIL and GMAIL_APP_PASSWORD environment variables

#### LaTeX Compilation Errors
```bash
# Test LaTeX installation
pdflatex --version

# Install missing packages (MiKTeX)
miktex packages install <package-name>
```

#### OCR Processing Issues
- Ensure sufficient system memory for PaddleOCR
- Verify image/PDF file accessibility
- Check Google AI API key validity

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 API Reference

### Response Format
All tools return JSON-formatted strings with consistent structure:

```json
{
  "status": "success|error",
  "message": "Descriptive message",
  "data": { /* Tool-specific data */ },
  "metadata": { /* Additional information */ }
}
```

### Error Handling
- **Validation Errors**: Detailed field-level validation messages
- **System Errors**: Graceful error handling with user-friendly messages
- **Retry Logic**: Automatic retries for transient failures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Commit changes: `git commit -am 'Add new feature'`
5. Push to branch: `git push origin feature/new-feature`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

## 🔄 Version History

- **v0.1.0**: Initial release with core PO management features
- Features: Email monitoring, document processing, PO generation, inventory management

---

**Note**: This MCP server is designed to work with Model Context Protocol clients. Ensure your client supports MCP specification v0.1.0 or later.