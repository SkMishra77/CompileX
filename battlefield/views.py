from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from arena.serializer import *
from utils.responseUtils import res_fun
from .serializers import *


class BattleViewSet(ViewSet):

    @action(detail=False, methods=['POST'])
    def create_room(self, request):
        obj = None
        data = request.data
        serializer = BattleSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
        return res_fun(1, {
            'roomId': obj.pk,
        })

    @transaction.atomic
    @action(detail=False, methods=['POST'])
    def add_problem(self, request):
        obj = None
        data = request.data
        room_id = data.get('room_id')
        if room_id is None:
            return res_fun(0, "Room Id not found")

        data.update({
            'is_battle': True
        })
        serializer = ProblemCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()

        room_obj = BattleModel.objects.get(pk=room_id)

        ProblemBattleModel(room_id=room_obj, p_id=obj).save()
        return res_fun(1, {
            'p_id': obj.pk
        })

    @action(detail=False, methods=['GET'])
    def get_problem_by_room(self, request):
        room_id = request.query_params.get('room_id')
        if room_id is None:
            return res_fun(0, "Room Id Missing")

        room_obj: BattleModel = BattleModel.objects.filter(pk=room_id).first()
        if room_obj is None:
            return res_fun(0, "Room not found")

        if room_obj.start_time > timezone.now() or room_obj.end_time < timezone.now():
            return res_fun(0, "Battle Haven't Started or Ended")

        all_problem = ProblemBattleModel.objects.filter(room_id=room_id)
        problems_obj = [i.p_id for i in all_problem]
        data = ProblemGetAllSerializer(problems_obj, many=True).data
        return res_fun(1, data)

    @action(detail=False, methods=['POST'])
    def get_user_id(self, request):
        name = request.data.get('name')
        room_id = request.data.get('room_id')
        if name is None or room_id is None:
            return res_fun(0, "User name or roomId not found")
        room_obj = BattleModel.objects.get(pk=room_id)
        obj = UserModel(name=name, room_id=room_obj)
        obj.save()
        return res_fun(1, {
            'user_id': obj.pk
        })
