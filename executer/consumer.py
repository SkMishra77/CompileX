import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from utils.compilationUtils import compileCpp_async
from utils.responseUtils import response_fun


class PlayGroundCodeExecuterSocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('user Connected')
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            try:
                text_data = json.loads(text_data)
                language = text_data.get('language', 'cpp')
                code = text_data.get('code', None)
                user_input = text_data.get('input', None)

                if not code:
                    await self.send_json(response_fun(0, "Code Not Found"))
                    await self.close()

                if language == 'cpp':
                    result = await compileCpp_async(code, user_input)
                    if result['error']:
                        await self.send_json(response_fun(0, result))
                    else:
                        await self.send_json(response_fun(1, result))
                    await self.close()

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
