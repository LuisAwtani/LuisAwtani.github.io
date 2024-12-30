import subprocess
import re

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

# Main script
if __name__ == "__main__":
    email_input = input("Enter the email address to add to the mailing list: ").strip()
    result = add_email_to_dynamodb(email_input)
    print(result)
