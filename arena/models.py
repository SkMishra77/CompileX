from django.db import models

from utils.util import generateProblemId


class ProblemModel(models.Model):
    P_DIFFICIULTY = [
        (0, 'Easy'),
        (1, 'Medium'),
        (2, 'Hard'),
    ]
    p_id = models.CharField(primary_key=True, max_length=64, default=generateProblemId)
    p_title = models.CharField(max_length=100)
    p_content = models.TextField()
    p_author = models.CharField(max_length=32)
    p_likes = models.IntegerField(default=0)
    p_difficulty = models.IntegerField(choices=P_DIFFICIULTY, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class TestCaseModel(models.Model):
    p_id = models.ForeignKey(ProblemModel, on_delete=models.CASCADE)
    input_case = models.TextField()
    output_case = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
