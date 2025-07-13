"""
Purchase Queue Management Tool

This tool manages a queue of validated purchase requests, allowing the purchase validation agent
to store approved requests and the purchase order agent to retrieve and process them.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

class PurchaseQueueTool:
    """Tool for managing purchase request queue operations"""
    
    def __init__(self):
        self.name = "PurchaseQueueTool"
        self.description = (
            "Manages a queue of validated purchase requests with complete supplier and line item details. "
            "Supports adding validated requests to the queue, retrieving pending requests for processing, "
            "and marking requests as completed. "
            "\n\nExpected data format for 'add_to_queue' action:"
            "\n{"
            "\n  'supplier_name': 'Supplier Company Name',"
            "\n  'supplier_contact': {"
            "\n    'contact_person': 'Contact Name',"
            "\n    'email': 'supplier@email.com'"
            "\n  },"
            "\n  'line_items': ["
            "\n    {"
            "\n      'item_code': 'ITM001',"
            "\n      'description': 'Item description',"
            "\n      'quantity': 100,"
            "\n      'unit_price': 25.50,"
            "\n      'uom': 'pcs',"
            "\n      'urgency': 'high',"
            "\n      'budget_code': 'DEPT001',"
            "\n      'estimated_total': 2550.00"
            "\n    }"
            "\n  ],"
            "\n  'delivery_requirements': {"
            "\n    'delivery_date': 'YYYY-MM-DD',"
            "\n    'delivery_address': 'Complete address',"
            "\n    'special_instructions': 'Any special requirements'"
            "\n  },"
            "\n  'budget_validation': {"
            "\n    'approved': true,"
            "\n    'budget_available': 50000.00,"
            "\n    'estimated_cost': 2550.00"
            "\n  },"
            "\n  'priority': 'high',"
            "\n  'request_date': 'YYYY-MM-DD',"
            "\n  'validated_by': 'Validator Name'"
            "\n}"
            "\n\nActions: 'add_to_queue', 'get_pending', 'mark_completed', 'get_status'"
        )
        
        # Get the project root directory (where the main script runs)
        project_root = os.getcwd()
        self.queue_file = os.path.join(project_root, "data", "purchase_queue.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
        # Initialize queue file if it doesn't exist
        if not os.path.exists(self.queue_file):
            self._initialize_queue()

    def _initialize_queue(self):
        """Initialize an empty queue file"""
        initial_data = {
            "pending_requests": [],
            "completed_requests": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        }
        with open(self.queue_file, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def _load_queue(self) -> Dict[str, Any]:
        """Load the current queue data"""
        try:
            with open(self.queue_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_queue()
            with open(self.queue_file, 'r') as f:
                return json.load(f)

    def _save_queue(self, data: Dict[str, Any]):
        """Save queue data to file"""
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.queue_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _generate_request_id(self) -> str:
        """Generate a unique request ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"PQ_{timestamp}"

    def manage_queue(self, action: str, request_data: Optional[Dict[str, Any]] = None, 
                    request_id: Optional[str] = None) -> str:
        """
        Execute queue management operations
        
        Args:
            action: Action to perform ('add_to_queue', 'get_pending', 'mark_completed', 'get_status')
            request_data: Purchase request data (for add_to_queue action)
            request_id: Request ID (for mark_completed action)
        """
        try:
            if action == "add_to_queue":
                return self._add_to_queue(request_data)
            elif action == "get_pending":
                return self._get_pending_requests()
            elif action == "mark_completed":
                return self._mark_completed(request_id)
            elif action == "get_status":
                return self._get_queue_status()
            else:
                return f"Error: Unknown action '{action}'. Available actions: add_to_queue, get_pending, mark_completed, get_status"
                
        except Exception as e:
            return f"Error in PurchaseQueueTool: {str(e)}"

    def _add_to_queue(self, request_data: Dict[str, Any]) -> str:
        """Add a validated purchase request to the queue"""
        if not request_data:
            return "Error: No request data provided"

        queue_data = self._load_queue()
        request_id = self._generate_request_id()
        
        queue_item = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "validation_data": request_data,
            "created_by": "purchase_validation_agent"
        }
        
        queue_data["pending_requests"].append(queue_item)
        self._save_queue(queue_data)
        
        return f"✅ Purchase request {request_id} added to queue successfully. Total pending requests: {len(queue_data['pending_requests'])}"

    def _get_pending_requests(self) -> str:
        """Retrieve all pending purchase requests"""
        queue_data = self._load_queue()
        pending = queue_data.get("pending_requests", [])
        
        if not pending:
            return "📋 No pending purchase requests in queue."
        
        result = f"📋 Found {len(pending)} pending purchase request(s):\n\n"
        
        for request in pending:
            result += f"🔹 Request ID: {request['request_id']}\n"
            result += f"   Timestamp: {request['timestamp']}\n"
            result += f"   Status: {request['status']}\n"
            
            # Extract key information from validation data
            validation_data = request.get("validation_data", {})
            if validation_data:
                result += "   Validation Summary:\n"
                if "budget_status" in validation_data:
                    result += f"     - Budget Status: {validation_data['budget_status']}\n"
                if "total_cost" in validation_data:
                    result += f"     - Total Cost: ${validation_data.get('total_cost', 'N/A')}\n"
                if "supplier_count" in validation_data:
                    result += f"     - Suppliers: {validation_data['supplier_count']}\n"
                if "priority_items" in validation_data:
                    result += f"     - Critical Items: {validation_data['priority_items']}\n"
            
            result += "\n"
        
        return result

    def _mark_completed(self, request_id: str) -> str:
        """Mark a request as completed"""
        if not request_id:
            return "Error: No request ID provided"

        queue_data = self._load_queue()
        pending_requests = queue_data.get("pending_requests", [])
        completed_requests = queue_data.get("completed_requests", [])
        
        # Find and move the request
        for i, request in enumerate(pending_requests):
            if request["request_id"] == request_id:
                # Mark as completed and move to completed list
                request["status"] = "completed"
                request["completed_at"] = datetime.now().isoformat()
                request["processed_by"] = "purchase_order_agent"
                
                completed_requests.append(request)
                pending_requests.pop(i)
                
                queue_data["pending_requests"] = pending_requests
                queue_data["completed_requests"] = completed_requests
                self._save_queue(queue_data)
                
                return f"✅ Request {request_id} marked as completed. Remaining pending: {len(pending_requests)}"
        
        return f"❌ Request {request_id} not found in pending requests"

    def _get_queue_status(self) -> str:
        """Get overall queue status"""
        queue_data = self._load_queue()
        pending_count = len(queue_data.get("pending_requests", []))
        completed_count = len(queue_data.get("completed_requests", []))
        
        result = "📊 Purchase Queue Status:\n"
        result += f"   Pending Requests: {pending_count}\n"
        result += f"   Completed Requests: {completed_count}\n"
        result += f"   Last Updated: {queue_data.get('metadata', {}).get('last_updated', 'N/A')}\n"
        
        return result

if __name__ == "__main__":
    # Test the tool
    tool = PurchaseQueueTool()
    
    # Test adding a request
    test_request = {
        "supplier_name": "Test Supplier",
        "total_cost": 1000.00,
        "budget_status": "approved",
        "supplier_count": 1,
        "priority_items": 2
    }
    
    print(tool.manage_queue("add_to_queue", request_data=test_request))
    print(tool.manage_queue("get_pending"))
    print(tool.manage_queue("get_status"))
