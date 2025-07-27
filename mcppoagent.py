from typing import List, Dict
import json
from datetime import datetime, timedelta
import random
from mcp.server.fastmcp import FastMCP
from document_generator_tool import DocumentGenerator
from email_monitoring_tool import EmailMonitoringTool
from document_parser_tool import DocumentParser
from financial_tool import FinancialDataTool
from purchase_queue_tool import PurchaseQueueTool
from po_record_tool import PORecordTool
from po_email_generator_tool import POEmailGenerator
from restock_inventory_tool import RestockInventoryTool
from report_file_tool import ReportFileTool
from email_response_tool import EmailResponseGenerator
import os
from dotenv import load_dotenv
# Load environment variables from .env file if present
load_dotenv()
# Print all environment variables (for debugging)
# for key, value in os.environ.items():
#     print(f"{key}={value}")
# Initialize FastMCP server
mcp = FastMCP("potool",port=8099)

# Initialize all tools (no longer inherit from BaseTool)
doc_generator = DocumentGenerator()
email_monitor = EmailMonitoringTool()
doc_parser = DocumentParser()
financial_tool = FinancialDataTool()
purchase_queue = PurchaseQueueTool()
po_record = PORecordTool()
po_email = POEmailGenerator()
inventory_tool = RestockInventoryTool()
report_tool = ReportFileTool()
email_response = EmailResponseGenerator()

print("All tools initialized successfully.")

@mcp.tool()
async def generate_purchase_order(
    supplier_name: str,
    items: List[Dict],
    delivery_date: str = "",
    delivery_address: str = "Default Company Address",
    contact_person: str = "",
    contact_email: str = "",
    special_instructions: str = "",
    po_number: str = ""
) -> str:
    """Generate a PDF purchase order document.

    Args:
        supplier_name: Name of the supplier
        items: List of items with format [{"item_code": "ITM001", "description": "Widget A", "quantity": 100, "unit_price": 25.50, "uom": "pcs", "urgency": "high"}]
        delivery_date: Required delivery date (optional)
        delivery_address: Delivery address (optional)
        contact_person: Supplier contact person (optional)
        contact_email: Supplier contact email (optional)
        special_instructions: Special instructions for the order (optional)
        po_number: Purchase order number (auto-generated if not provided)
    """
    try:
        # Use the document generator to create the PDF PO
        result = doc_generator.create_pdf_purchase_order(
            supplier_name=supplier_name,
            items=items,
            delivery_date=delivery_date,
            delivery_address=delivery_address,
            contact_person=contact_person,
            contact_email=contact_email,
            special_instructions=special_instructions,
            po_number=po_number
        )
        
        return result
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to generate purchase order: {str(e)}",
            "supplier_name": supplier_name
        })

@mcp.tool()
async def generate_latex_po(
    supplier_name: str,
    items: List[Dict],
    delivery_date: str = "",
    delivery_address: str = "Default Company Address",
    contact_person: str = "",
    contact_email: str = "",
    special_instructions: str = "",
    po_number: str = ""
) -> str:
    """Generate a LaTeX purchase order document.

    Args:
        supplier_name: Name of the supplier
        items: List of items with format [{"item_code": "ITM001", "description": "Widget A", "quantity": 100, "unit_price": 25.50, "uom": "pcs", "urgency": "high"}]
        delivery_date: Required delivery date (optional)
        delivery_address: Delivery address (optional)
        contact_person: Supplier contact person (optional)
        contact_email: Supplier contact email (optional)
        special_instructions: Special instructions for the order (optional)
        po_number: Purchase order number (auto-generated if not provided)
    """
    try:
        # Use the document generator to create the LaTeX PO
        result = doc_generator.create_latex_purchase_order(
            supplier_name=supplier_name,
            items=items,
            delivery_date=delivery_date,
            delivery_address=delivery_address,
            contact_person=contact_person,
            contact_email=contact_email,
            special_instructions=special_instructions,
            po_number=po_number
        )
        
        return result
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to generate LaTeX purchase order: {str(e)}",
            "supplier_name": supplier_name
        })

@mcp.tool()
async def validate_po_items(items: List[Dict]) -> str:
    """Validate purchase order items format.

    Args:
        items: List of items to validate
    """
    try:
        doc_generator._validate_items_format(items)
        
        # Calculate totals for validation
        total_quantity = sum(item.get('quantity', 0) for item in items)
        total_value = sum(item.get('quantity', 0) * item.get('unit_price', 0) for item in items)
        
        return json.dumps({
            "status": "success",
            "message": "Items validation passed",
            "items_count": len(items),
            "total_quantity": total_quantity,
            "total_value": total_value,
            "items": items
        })
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Items validation failed: {str(e)}",
            "items_count": len(items) if items else 0
        })

@mcp.tool()
async def create_sample_po_data(
    item_count: int = 3,
    supplier_name: str = "ABC Suppliers Ltd"
) -> str:
    """Create sample purchase order data for testing.

    Args:
        item_count: Number of sample items to create (default: 3)
        supplier_name: Name of the supplier (default: "ABC Suppliers Ltd")
    """
    try:
        # Sample item data
        sample_items = [
            {"code": "WDG001", "desc": "Industrial Widget Type A", "base_price": 25.50},
            {"code": "BLT002", "desc": "High-Strength Bolt M10x50", "base_price": 3.75},
            {"code": "PLT003", "desc": "Steel Plate 300x200x10mm", "base_price": 45.00},
            {"code": "GER004", "desc": "Precision Gear Assembly", "base_price": 120.00},
            {"code": "SPR005", "desc": "Heavy Duty Spring Unit", "base_price": 18.25},
            {"code": "BRG006", "desc": "Ball Bearing 6205-2RS", "base_price": 12.50},
            {"code": "CBL007", "desc": "Control Cable 5m", "base_price": 35.00},
            {"code": "VLV008", "desc": "Hydraulic Valve Assembly", "base_price": 85.75}
        ]
        
        # Generate random items
        selected_items = random.sample(sample_items, min(item_count, len(sample_items)))
        
        items = []
        for item in selected_items:
            urgency = random.choice(["low", "medium", "high"])
            quantity = random.randint(10, 200)
            price_variation = random.uniform(0.9, 1.1)  # ±10% price variation
            unit_price = round(item["base_price"] * price_variation, 2)
            
            items.append({
                "item_code": item["code"],
                "description": item["desc"],
                "quantity": quantity,
                "unit_price": unit_price,
                "uom": "pcs",
                "urgency": urgency
            })
        
        # Generate delivery date (7-30 days from now)
        delivery_date = (datetime.now() + timedelta(days=random.randint(7, 30))).strftime('%Y-%m-%d')
        
        sample_data = {
            "supplier_name": supplier_name,
            "items": items,
            "delivery_date": delivery_date,
            "contact_person": "John Smith",
            "contact_email": "john.smith@abcsuppliers.com",
            "special_instructions": "Handle with care. Deliver during business hours only.",
            "delivery_address": "Warehouse B, Industrial District, City"
        }
        
        return json.dumps({
            "status": "success",
            "message": f"Sample PO data created with {len(items)} items",
            "sample_data": sample_data,
            "total_value": sum(item["quantity"] * item["unit_price"] for item in items)
        })
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to create sample data: {str(e)}"
        })

# Email Monitoring Tool
@mcp.tool()
async def fetch_emails() -> str:
    """Fetch unread emails with attachments from Gmail inbox.
    
    Returns:
        JSON string with emails that have attachments, including sender, subject, body, and attachment paths
    """
    return email_monitor.fetch_emails()

# Document Parser Tool  
@mcp.tool()
async def parse_document(file_path: str, action: str = "extract_po_data") -> str:
    """Parse documents and extract structured purchase order data.
    
    Args:
        file_path: Path to document file
        action: Type of action (extract_po_data)
    """
    return doc_parser.parse_document(file_path, action)

# Financial Data Tool
@mcp.tool()
async def get_financial_data(query_type: str, amount: float = 0.0) -> str:
    """Get financial data and approval status.
    
    Args:
        query_type: Type of query ('approval_limits' or 'procurement_budget')
        amount: Amount for approval validation and budget check
    """
    return financial_tool.get_financial_data(query_type, amount)

# Purchase Queue Tool
@mcp.tool()
async def manage_purchase_queue(action: str, request_data: Dict = None, request_id: str = None) -> str:
    """Manage purchase request queue operations.
    
    Args:
        action: Action to perform ('add_to_queue', 'get_pending', 'mark_completed', 'get_status')
        request_data: Purchase request data (for add_to_queue action)
        request_id: Request ID (for mark_completed action)
    """
    return purchase_queue.manage_queue(action, request_data, request_id)

# PO Record Tool
@mcp.tool()
async def manage_po_records(action: str, extracted_data: Dict = None, po_data: Dict = None, order_id: str = None) -> str:
    """Execute PO record management actions.
    
    Args:
        action: Action to perform ('record_extracted_orders', 'record_single_po', 'get_order_status')
        extracted_data: Extracted data containing orders and metadata
        po_data: Single PO data for record_single_po action
        order_id: Order ID for get_order_status action
    """
    return po_record.manage_po_records(action, extracted_data, po_data, order_id)

# PO Email Generator Tool
@mcp.tool()
async def generate_po_email(
    action: str = "send_po_email",
    supplier_email: str = "",
    supplier_name: str = "",
    po_number: str = "",
    po_data: Dict = {},
    po_file_path: str = "",
    delivery_date: str = "",
    special_instructions: str = "",
    cc_emails: List[str] = [],
    urgent: bool = False
) -> str:
    """Generate and send purchase order emails to suppliers.
    
    Args:
        action: Action to perform (send_po_email, create_email_draft)
        supplier_email: Email address of the supplier
        supplier_name: Name of the supplier
        po_number: Purchase Order number
        po_data: Purchase order data dictionary
        po_file_path: Path to PDF purchase order file
        delivery_date: Expected delivery date
        special_instructions: Special instructions
        cc_emails: List of CC email addresses
        urgent: Mark as urgent priority
    """
    return po_email.generate_po_email(
        action, supplier_email, supplier_name, po_number, po_data, 
        po_file_path, delivery_date, special_instructions, cc_emails, urgent
    )

# Inventory Tool
@mcp.tool()
async def analyze_inventory(analysis_type: str, category: str = "", urgency_level: str = "all") -> str:
    """Analyze inventory and get restock information.
    
    Args:
        analysis_type: Type of analysis ('restock_needed' or 'inventory_status')
        category: Filter by category (optional)
        urgency_level: Filter by urgency level ('critical', 'high', 'medium', 'all')
    """
    return inventory_tool.analyze_inventory(analysis_type, category, urgency_level)

# Report File Tool
@mcp.tool()
async def save_report(
    file_path: str,
    data: str,
    append: bool = False,
    create_dirs: bool = True,
    add_timestamp: bool = False,
    encoding: str = "utf-8"
) -> str:
    """Save data to a text file.
    
    Args:
        file_path: Path where the file should be saved
        data: String data to save
        append: Whether to append to existing file or overwrite
        create_dirs: Whether to create directories if they don't exist
        add_timestamp: Whether to add timestamp to the data
        encoding: File encoding (default: utf-8)
    """
    return report_tool.save_report(file_path, data, append, create_dirs, add_timestamp, encoding)

# Email Response Tool
@mcp.tool()
async def send_response_email(
    subject: str,
    body: str,
    recipient_email: str,
    recipient_name: str = "",
    po_number: str = "",
    urgent: bool = False
) -> str:
    """Send an email response with custom subject and body.
    
    Args:
        subject: Email subject line
        body: Email body content
        recipient_email: Recipient email address
        recipient_name: Recipient name (optional)
        po_number: Purchase order number (optional)
        urgent: Mark email as urgent/high priority (optional)
    """
    return email_response.send_response_email(subject, body, recipient_email, recipient_name, po_number, urgent)
# print(mcp.list_tools())

if __name__ == "__main__":
    # Initialize and run the server
    
    print("Starting FastMCP server...")
    mcp.run(transport='streamable-http')