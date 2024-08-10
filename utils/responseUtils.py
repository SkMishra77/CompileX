from rest_framework import status
from rest_framework.response import Response


def response_fun(*args):
    if args[0] == 1:
        return {'error': False, 'status': 200, 'responseData': args[1]}
    else:
        return {'error': True, 'status': 400, 'responseData': args[1]}


def res_fun(*args, status_code=None):
    if status_code:
        return Response({'error': True, 'message': args[1], 'status_code': status_code})
    if args[0] == 1:
        return Response({'error': False, 'responseData': args[1], 'status_code': status.HTTP_200_OK})
    else:
        return Response(
            {'error': True, 'message': args[1], 'status_code': status.HTTP_400_BAD_REQUEST})
