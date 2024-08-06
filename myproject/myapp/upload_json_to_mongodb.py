import os
import json
from pymongo import MongoClient

# Path to your directory containing JSON files
json_directory = r"C:\Users\DELL\Desktop\Analytical Engine\project\JSON"  # Update this to your specific directory

# MongoDB connection details
mongo_uri = 'mongodb://localhost:27017/'
db_name = 'analytical_engine'
collection_name = 'data_collection'

def connect_to_mongo():
    """
    Connect to MongoDB and return the database and collection instances.
    """
    try:
        # Create a MongoDB client
        client = MongoClient(mongo_uri)
        # Access the database
        db = client[db_name]
        # Access the collection
        collection = db[collection_name]
        return collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def upload_json_files(directory, collection):
    """
    Upload JSON files from a specified directory to a MongoDB collection.
    
    :param directory: The directory containing JSON files.
    :param collection: The MongoDB collection to which data will be uploaded.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    # Load JSON data
                    data = json.load(file)
                    # Insert data into MongoDB
                    if isinstance(data, list):
                        collection.insert_many(data)
                        print(f"Uploaded list data from {filename} successfully.")
                    else:
                        collection.insert_one(data)
                        print(f"Uploaded single document from {filename} successfully.")
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON from {filename}: {e}")
            except Exception as e:
                print(f"Error uploading data from {filename}: {e}")

def main():
    # Connect to MongoDB
    collection = connect_to_mongo()
    if collection is None:
        print("Failed to connect to MongoDB. Exiting.")
        return

    # Upload JSON files to MongoDB
    upload_json_files(json_directory, collection)

if __name__ == '__main__':
    main()
