from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient

class DataView(APIView):
    def get(self, request):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['analytical_engine']
        collection = db['data_collection']
        data = list(collection.find({}))
        client.close()

        for item in data:
            item['_id'] = str(item['_id'])

        return Response(data, status=status.HTTP_200_OK)

# Create your views here.
