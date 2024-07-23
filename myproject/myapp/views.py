from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import json

class ContractDetailsView(APIView):
    def get(self, request):
        try:
            # Connect to MongoDB
            client = MongoClient('mongodb://localhost:27017/')
            db = client['analytical_engine']  # Replace with your database name
            collection = db['data_collection']  # Replace with your collection name

            # Fetch all documents from the collection
            documents = collection.find({})

            # Prepare the response list
            response_data = []

            for doc in documents:
                contract_details = doc.get('contract_details', [])

                # Extract relevant information
                agreement_no = doc.get('contract_name', 'N/A')  # Assuming contract_name is agreement_no
                effective_date = None
                contract_term = None

                # Iterate over contract_details to find desired fields
                for detail in contract_details:
                    contract_terms = detail.get("Contract Terms", [])

                    for term in contract_terms:
                        if "Effective Date" in term:
                            effective_date = term["Effective Date"]
                        if "Contract Term" in term:
                            contract_term = term["Contract Term"]

                # Append extracted data to response list
                response_data.append({
                    "agreement_no": agreement_no,
                    "effective_date": effective_date,
                    "contract_term": contract_term
                })

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
