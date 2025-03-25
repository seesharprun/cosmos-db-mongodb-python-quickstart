from dotenv import load_dotenv

from pymongo import MongoClient

import os

def getLastRequestCharge(c):
    return c.client_connection.last_response_headers["x-ms-request-charge"]


def runDemo(writeOutput):
    load_dotenv()

    # <create_client>
    connection_string = os.getenv("CONFIGURATION__AZURECOSMOSDB__CONNECTIONSTRING")
    client = MongoClient(connection_string)
    # </create_client>
    
    print(f"ENDPOINT:\t{client.HOST}:{client.PORT}")

    database_name = os.getenv("CONFIGURATION__AZURECOSMOSDB__DATABASENAME", "cosmicworks")
    database = client.get_database(database_name)

    writeOutput(f"Get database:\t{database.id}")

    collection_name = os.getenv("CONFIGURATION__AZURECOSMOSDB__COLLECTIONNAME", "products")
    collection = database.get_collection(collection_name)

    writeOutput(f"Get collection:\t{collection.name}")

    new_document = {
        "_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "category": "gear-surf-surfboards",
        "name": "Yamba Surfboard",
        "quantity": 12,
        "sale": False,
    }

    filter = {
        "_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "category": "gear-surf-surfboards"
    }
    payload = {
        "$set": new_document
    }
    result = collection.update_one(filter, payload, upsert=True);

    if result.acknowledged:
        writeOutput(f"Upserted document:\t{new_document}", isCode=True)

    new_document = {
        "_id": "bbbbbbbb-1111-2222-3333-cccccccccccc",
        "category": "gear-surf-surfboards",
        "name": "Kiama Classic Surfboard",
        "quantity": 4,
        "sale": True,
    }
    
    filter = {
        "_id": "bbbbbbbb-1111-2222-3333-cccccccccccc",
        "category": "gear-surf-surfboards"
    }
    payload = {
        "$set": new_document
    }
    result = collection.update_one(filter, payload, upsert=True);

    if result.acknowledged:
        writeOutput(f"Upserted document:\t{new_document}", isCode=True)

    filter = {
        "_id": "bbbbbbbb-1111-2222-3333-cccccccccccc",
        "category": "gear-surf-surfboards"
    }
    existing_document = collection.find_one(filter)

    writeOutput(f"Read document _id:\t{existing_document['_id']}")
    writeOutput(f"Read document:\t{existing_document}", isCode=True)

    filter = {
        "category": "gear-surf-surfboards"
    }
    matched_documents = collection.find(filter)

    for document in matched_documents:
        writeOutput(f"Found document:\t{document}", isCode=True)
