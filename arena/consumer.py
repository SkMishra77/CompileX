import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from utils.compilationUtils import invoke_all_testcase_lambdas
from utils.responseUtils import response_fun
from .models import TestCaseModel


class ArenaCodeExecuterSocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('user Connected')
        await self.accept()

    @database_sync_to_async
    def get_test_cases(self, p_id):
        return list(TestCaseModel.objects.filter(p_id=p_id))

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            try:
                text_data = json.loads(text_data)
                language = text_data.get('language', 'cpp')
                code = text_data.get('code', None)
                p_id = text_data.get('p_id', None)

                if not code:
                    await self.send_json(response_fun(0, "Code Not Found"))
                    await self.close()

                test_cases = await self.get_test_cases(p_id)

                if not test_cases:
                    await self.send_json(response_fun(0, "No Test Case Found"))
                    await self.close()

                if language == 'cpp':
                    result = await invoke_all_testcase_lambdas(code, test_cases)
                    await self.send_json(response_fun(1, result))

                else:
                    await self.send_json(response_fun(0, 'Unsupported language'))

                await self.close()

            except json.JSONDecodeError:
                await self.send_json(response_fun(0, 'Invalid JSON'))
                await self.close()
        else:
            await self.send_json(response_fun(0, "Unprocessable Entity"))
            await self.close()

    async def disconnect(self, code):
        print('disconnected', code)
