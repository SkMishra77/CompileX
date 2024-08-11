import uuid

from arena.models import *


class BattleModel(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    b_name = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.b_name} {self.start_time} {self.end_time}'


class UserModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    room_id = models.ForeignKey(BattleModel, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProblemBattleModel(models.Model):
    room_id = models.ForeignKey(BattleModel, on_delete=models.CASCADE)
    p_id = models.ForeignKey(ProblemModel, on_delete=models.CASCADE)


class SubmissionBattleModel(models.Model):
    uid = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    room_id = models.ForeignKey(BattleModel, on_delete=models.CASCADE)
    problem_id = models.ForeignKey(ProblemModel, on_delete=models.CASCADE)
    finished_at = models.DateTimeField()
    total_runtime = models.FloatField()
    testcase_passed = models.IntegerField(default=0)
