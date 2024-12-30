import subprocess
import json
from datetime import datetime

# Generate the current date and time in DDMMYYYYHHMM format
datetime_now = datetime.now().strftime("%d%m%Y%H%M")


def get_and_increment_id():
    # Step 1: Retrieve the current ID value
    try:
        # Run the AWS CLI get-item command to retrieve the current value of the counter
        result = subprocess.run(
            ['aws', 'dynamodb', 'get-item', '--table-name', 'IDCounter', '--key', '{"CounterName": {"S": "ID"}}'],
            capture_output=True, text=True, check=True
        )

        # Parse the response from JSON to extract the current ID
        response_json = json.loads(result.stdout)
        current_id = int(response_json['Item']['Value']['N'])  # Assuming the 'Value' is a number

        print(f"Current ID: {current_id}")

    except subprocess.CalledProcessError as e:
        print(f"Error retrieving item: {e.stderr}")
        return None  # In case of error, return None

    # Step 2: Increment the ID value
    next_id = current_id + 1
    print(f"Next ID to insert: {next_id}")

    # Step 3: Update the ID in the DynamoDB table with the new incremented value
    updated_item = {
        "CounterName": {"S": "ID"},
        "Value": {"N": str(next_id)}  # Convert the incremented ID back to string
    }

    # Convert the updated item to JSON
    updated_item_json = json.dumps(updated_item)

    try:
        # Run the AWS CLI update-item command to increment the ID in the table
        subprocess.run(
            ['aws', 'dynamodb', 'put-item', '--table-name', 'IDCounter', '--item', updated_item_json],
            capture_output=True, text=True, check=True
        )
        print(f"Updated ID to: {next_id}")
        return current_id  # Return the current ID before incrementing
    except subprocess.CalledProcessError as e:
        print(f"Error updating item: {e.stderr}")
        return None




# Function that creates DynamoDB table
def create_table(table_name):
    # Command to create the DynamoDB table
    command = [
        'aws', 'dynamodb', 'create-table',
        '--table-name', table_name,
        '--attribute-definitions', 'AttributeName=ID,AttributeType=S',
        '--key-schema', 'AttributeName=ID,KeyType=HASH',
        '--provisioned-throughput', 'ReadCapacityUnits=5,WriteCapacityUnits=5'
    ]

    # Execute the command using subprocess
    try:
        subprocess.run(command, check=True)
        print("Table created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating the table: {e}")
    return

def delete_table(table_name):
    command = [
    'aws', 'dynamodb', 'delete-table',
    '--table-name', table_name
    ]

    # Execute the command using subprocess
    try:
        subprocess.run(command, check=True)
        print("Table deleted successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while deleting the table: {e}")
    
    return

def list_tables():
    command = ['aws', 'dynamodb', 'list-tables']
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while listing the tables: {e}")
    return

def read_from_table(table_name):
    command = ['aws', 'dynamodb', 'scan', '--table-name', table_name]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while reading the table: {e}")
    return

def write_to_table(table_name):

    idCounter = get_and_increment_id()
    message = str(input("What message would you like to write to the table?: "))
    username = str(input("Which user is writing to the table?: "))

    entry = {
        "ID": {"S": str(idCounter)},
        "Datetime": {"N": datetime_now},
        "Message": {"S": message},
        "Response": {"S": "NULL"},
        "Username": {"S": username}
    }

    item_json = json.dumps(entry)


    command = [
    'aws', 'dynamodb', 'put-item',
    '--table-name', table_name,
    '--item', item_json
    ]
    # Execute the command using subprocess
    try:
        subprocess.run(command, check=True)
        print("Item inserted successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while inserting the item: {e}")
    return



cmd = input("What command would you like to run? \n 1: Write to a table \n 2: Read (scan) from a table \n 3: Delete a table \n 4: Create a table \n 5: List all tables \n")


if cmd == '1':
    table_name = input("What is the name of the table you would like to write to? \n")
    write_to_table(table_name)

elif cmd == '2':
    table_name = input("What is the name of the table you would like to read from? \n")
    read_from_table(table_name)

elif cmd == '3':
    table_name = input("What is the name of the table you would like to delete? \n")
    delete_table(table_name)

elif cmd == '4':
    table_name = input("What is the name of the table you would like to create? \n")
    create_table(table_name)

elif cmd == '5':
    list_tables()