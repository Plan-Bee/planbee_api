from rest_framework.response import Response
from rest_framework.decorators import api_view
from services_classes import mariadb_connector as mdb_connector


@api_view(['GET'])
def get_honeypi_data(request):
    mariadb_connector_obj = mdb_connector.MariaDBConnector()

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    response = mariadb_connector_obj.get_honeypi_data(start_date, end_date)
    mariadb_connector_obj.close_connection()

    return Response(response)
