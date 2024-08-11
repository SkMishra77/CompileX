from rest_framework import serializers

from .models import *


class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleModel
        fields = ['b_name', 'start_time', 'end_time']


class LeaderboardEntrySerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    uid = serializers.CharField()
    uid_name = serializers.CharField(max_length=64)
    total_runtime = serializers.FloatField()
    total_testcases_passed = serializers.IntegerField()
