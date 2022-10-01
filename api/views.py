import json
import requests
from datetime import datetime
from rest_framework.exceptions import bad_request
from rest_framework.response import Response
from rest_framework.views import APIView


class Api(APIView):
    def get(self, request, format=None):
        r = requests.get('https://mc3nt37jj5.execute-api.sa-east-1.amazonaws.com/default/hourth_desafio')
        data = {}

        init_date = None
        finish_date = None
        if request.query_params.get('init_date') and request.query_params.get('finish_date'):
            try:
                init_date = datetime.strptime(request.query_params.get('init_date'), '%Y-%m-%d')
                finish_date = datetime.strptime(request.query_params.get('finish_date'), '%Y-%m-%d')
            except ValueError:
                return bad_request(request, "Valores invalidos")

        for x in json.loads(r.text):
            date = datetime.strptime(x["consult_date"], '%Y-%m-%d')
            if init_date is None or finish_date is None or init_date <= date <= finish_date:
                if x["product_url"] in data:
                    if x["consult_date"] in data[x["product_url"]]:
                        data[x["product_url"]][x["consult_date"]] += x["vendas_no_dia"]
                    else:
                        data[x["product_url"]][x["consult_date"]] = x["vendas_no_dia"]
                    data[x["product_url"]]["total_sales"] += x["vendas_no_dia"]
                else:
                    data[x["product_url"]] = {
                        "product_url__image": x["product_url__image"],
                        "product_url": x["product_url"],
                        "product_url__created_at": x["product_url__created_at"],
                        "total_sales": x["vendas_no_dia"],
                        x["consult_date"]: x["vendas_no_dia"]
                    }

        new_data = []
        for x, y in data.items():
            new_data.append(y)
        return Response(new_data)
