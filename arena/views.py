from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from CompileX.custom_paginator import CustomPaginator
from utils.responseUtils import res_fun
from .serializer import *


class ArenaViewSet(ViewSet):

    @action(detail=False, methods=['POST'])
    def add_problem(self, request):
        data = request.data
        serializer = ProblemCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return res_fun(1, "Successfully added problem.")

    @action(detail=False, methods=['GET'])
    def get_problem(self, request):
        obj = ProblemModel.objects.filter(
            is_battle=False
        ).order_by('-created_at')
        paginator = CustomPaginator()
        result_page = paginator.paginate_queryset(obj, request)
        serializer = ProblemGetSerializer(result_page, many=True)
        data = paginator.get_paginated_response(serializer.data).data
        return res_fun(1, data)

    @action(detail=False, methods=['GET'])
    def get_problem_by_id(self, request):
        p_id = request.query_params.get('p_id')
        if not p_id:
            return res_fun(1, "Problem ID is required")

        obj = ProblemModel.objects.filter(id=p_id).first()
        if not obj:
            return res_fun(1, "Problem not found")

        data = ProblemGetAllSerializer(obj).data
        return res_fun(1, data)

    @action(detail=False, methods=['PUT'])
    def update_problem(self, request):
        p_id = request.data.get('p_id')
        if p_id is None:
            return res_fun(0, "Problem ID is missing")

        obj = ProblemModel.objects.filter(pk=p_id).first()
        if obj is None:
            return res_fun(0, "Problem does not exist")

        data = request.data
        serializer = ProblemUpdateSerializer(obj, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return res_fun(1, 'Problem Updated Successfully')

    @action(detail=False, methods=['DELETE'])
    def delete_problem(self, request):
        p_id = request.data.get('p_id')
        if p_id is None:
            return res_fun(0, "Problem ID is missing")

        obj = ProblemModel.objects.filter(pk=p_id).first()
        if obj is None:
            return res_fun(0, "Problem does not exist")
        obj.delete()
        return res_fun(1, "Problem Deleted Successfully")

    @action(detail=False, methods=['POST'])
    def add_testcase(self, request):
        data = request.data
        serializer = TestCaseCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return res_fun(1, "Successfully added testcase.")

    @action(detail=False, methods=['GET'])
    def get_testcase(self, request):
        p_id = request.query_params.get('pid')
        if p_id is None:
            return res_fun(0, "Problem ID is missing")

        obj = TestCaseModel.objects.filter(
            p_id=p_id,
            is_public=True
        )

        data = TestCaseViewSerializer(obj, many=True).data
        return res_fun(1, data)

    @action(detail=False, methods=['DELETE'])
    def delete_testcase(self, request):
        t_id = request.data.get('id')
        if t_id is None:
            return res_fun(0, "TestCase ID is missing")

        obj = TestCaseModel.objects.filter(pk=t_id).first()
        if obj is None:
            return res_fun(0, "TestCase does not exist")
        obj.delete()
        return res_fun(1, "TestCase Deleted Successfully")
