# myapp/views.py
from pymongo import MongoClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser

import json

from pymongo import MongoClient

class ContractDetailsView(APIView):
    parser_classes = [MultiPartParser, JSONParser]  # Added JSONParser for JSON requests

    def get_collection(self):
        mongo_uri = 'mongodb://localhost:27017/'
        db_name = 'analytical_engine'
        collection_name = 'data_collection'

        client = MongoClient(mongo_uri)
        db = client[db_name]
        return db[collection_name]

    def get(self, request):
        try:
            collection = self.get_collection()
            documents = collection.find({})

            response_data = []

            for doc in documents:
                contract_details = doc.get('contract_details', [])

                agreement_no = doc.get('contract_name', 'N/A')
                effective_date = None
                contract_term = None

                for detail in contract_details:
                    contract_terms = detail.get("Contract Terms", [])

                    for term in contract_terms:
                        if "Effective Date" in term:
                            effective_date = term["Effective Date"]
                        if "Contract Term" in term:
                            contract_term = term["Contract Term"]

                response_data.append({
                    "agreement_no": agreement_no,
                    "effective_date": effective_date,
                    "contract_term": contract_term
                })

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)