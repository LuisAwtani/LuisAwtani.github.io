import subprocess
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Function to validate the email address
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Function to add email to DynamoDB using AWS CLI
def add_email_to_dynamodb(email):
    # Validate the email address
    if not is_valid_email(email):
        return "Invalid email address format."
    
    try:
        # Prepare the AWS CLI command
        command = [
            "aws", "dynamodb", "put-item",
            "--table-name", "mailingList",
            "--item", f'{{"email": {{"S": "{email}"}}}}',
            "--condition-expression", "attribute_not_exists(email)"
        ]
        
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            return "Email added successfully."
        else:
            error_output = result.stderr
            if "ConditionalCheckFailedException" in error_output:
                return "This email is already in the mailing list."
            return f"An error occurred: {error_output.strip()}"
    
    except FileNotFoundError:
        return "AWS CLI is not installed or not available in the system path."
    
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

class SubscribeHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        email = data.get('email')
        
        if not email:
            self.send_error(400, "Email is required")
            return
            
        result = add_email_to_dynamodb(email)
        
        self.send_response(200 if "successfully" in result else 400)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'message' if "successfully" in result else 'error': result}
        self.wfile.write(json.dumps(response).encode())

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SubscribeHandler)
    print(f'Starting subscription server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
