import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Sum, F, Window
from django.db.models.functions import Rank
from django.utils import timezone
from utils.compilationUtils import invoke_all_testcase_lambdas
from utils.responseUtils import response_fun
from .models import *
from .serializers import LeaderboardEntrySerializer


class BattleCodeExecuterSocketConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.room_id = None

    async def connect(self):
        print('User connected')
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'room_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    @database_sync_to_async
    def get_test_cases(self, p_id):
        return list(TestCaseModel.objects.filter(p_id=p_id))

    async def create_submit_entry(self, p_id, uid, room_id, tc_passed, t_runtime):
        p_id = await ProblemModel.objects.filter(p_id=p_id).afirst()
        uid = await UserModel.objects.filter(pk=uid).afirst()
        room = await BattleModel.objects.filter(pk=room_id).afirst()

        obj = await SubmissionBattleModel.objects.filter(
            problem_id=p_id,
            uid=uid,
            room_id=room,
        ).afirst()

        if obj is None:
            await SubmissionBattleModel.objects.acreate(
                problem_id=p_id,
                uid=uid,
                room_id=room,
                total_runtime=t_runtime,
                testcase_passed=tc_passed,
                finished_at=timezone.now(),
            )
        else:
            if obj.testcase_passed < tc_passed:
                obj.testcase_passed = tc_passed
                obj.total_runtime = t_runtime
                await obj.asave()
            elif obj.total_runtime >= t_runtime:
                obj.total_runtime = t_runtime
                await obj.asave()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            try:
                text_data = json.loads(text_data)
                language = text_data.get('language', 'cpp')
                code = text_data.get('code', None)
                p_id = text_data.get('p_id', None)
                uid = text_data.get('uid', None)
                event_type = text_data.get('event', None)

                if event_type == 'leaderboard':
                    result = await self.calculate_leaderboard()
                    await self.send_leaderboard_update({'leaderboard': result})
                    return

                if not uid:
                    await self.send_json(response_fun(0, "User Id Not Found"))
                    return await self.close()

                if not code:
                    await self.send_json(response_fun(0, "Code Not Found"))
                    return await self.close()

                test_cases = await self.get_test_cases(p_id)
                test_cases_count = len(test_cases)

                if not test_cases:
                    await self.send_json(response_fun(0, "No Test Case Found"))
                    return await self.close()

                if language == 'cpp':
                    result = await invoke_all_testcase_lambdas(code, test_cases)
                    await self.safe_send_json({
                        'error': False, 'status': 200,
                        'responseData': result,
                        'event': 'runner'
                    })

                    tc_passed = 0
                    run_time = 0
                    for i in result:
                        if i['passed']:
                            tc_passed += 1
                            run_time += i['data']['exec_time']

                    await self.create_submit_entry(p_id, uid, self.room_id, tc_passed, run_time)
                    leaderboard = await self.calculate_leaderboard()

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'send_leaderboard_update',
                            'leaderboard': leaderboard,
                        }
                    )

                else:
                    await self.send_json(response_fun(0, 'Unsupported language'))

            except json.JSONDecodeError:
                await self.send_json(response_fun(0, 'Invalid JSON'))
                await self.close()
        else:
            await self.send_json(response_fun(0, "Unprocessable Entity"))
            await self.close()

    @database_sync_to_async
    def calculate_leaderboard(self):
        results = (
            SubmissionBattleModel.objects
            .filter(room_id=self.room_id)  # Filter by specific room
            .values('uid', 'uid__name')  # Group by user ID but include the name in the result
            .annotate(
                total_runtime=Sum('total_runtime'),
                total_testcases_passed=Sum('testcase_passed')
            )
            .annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=[F('total_testcases_passed').desc(), F('total_runtime').asc()]
                )
            )
            .order_by('rank')  # Order by rank
        )
        return LeaderboardEntrySerializer(results, many=True).data

    async def send_leaderboard_update(self, event):
        leaderboard = event['leaderboard']

        # Send leaderboard update to WebSocket
        await self.safe_send_json({
            'error': False,
            'responseData': leaderboard,
            'event': 'leaderboard',
            "status": 200,
        })

    async def safe_send_json(self, content):
        """Send data if the connection is still open."""
        if self.scope["client"]:
            try:
                await self.send_json(content)
            except Exception as e:
                print(f"Error sending data: {e}")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('Disconnected', code)
