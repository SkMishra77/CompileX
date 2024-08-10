from rest_framework import serializers

from .models import ProblemModel, TestCaseModel


class ProblemCreationSerializer(serializers.ModelSerializer):
    p_title = serializers.CharField()
    p_content = serializers.CharField()
    p_author = serializers.CharField()

    class Meta:
        model = ProblemModel
        fields = ['p_title', 'p_content', 'p_author', 'p_difficulty']


class ProblemGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemModel
        fields = ['p_id', 'p_title', 'p_author', 'p_difficulty']


class ProblemGetAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemModel
        fields = ['p_id', 'p_title', 'p_author', 'p_difficulty', 'p_content']


class ProblemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemModel
        fields = ['p_likes', 'p_difficulty']


class TestCaseCreationSerializer(serializers.ModelSerializer):
    input_case = serializers.CharField()
    output_case = serializers.CharField()

    class Meta:
        model = TestCaseModel
        fields = ['p_id', 'input_case', 'output_case', 'is_public']


class TestCaseViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseModel
        fields = ['input_case', 'output_case', 'is_public', 'id']
