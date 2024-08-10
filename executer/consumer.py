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

    # async def handle_cpp_code(self, code, user_input):
    #     try:
    #         with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False) as cpp_file:
    #             cpp_file.write(code.encode('utf-8'))
    #             cpp_file_path = cpp_file.name
    #
    #         # Compile the C++ code
    #         executable_path = cpp_file_path[:-4]
    #
    #         compile_process = subprocess.run(
    #             ['g++', cpp_file_path, '-o', executable_path],
    #             capture_output=True,
    #             text=True,
    #             timeout=20
    #         )
    #
    #         if compile_process.returncode != 0:
    #             await self.send_json(response_fun(0, {
    #                 'message': 'error',
    #                 'error': 'Compilation error',
    #                 'details': compile_process.stderr
    #             }))
    #             await self.close()
    #
    #         # Execute the compiled code with input
    #         execution_process = subprocess.run(
    #             [executable_path],
    #             input=user_input,
    #             capture_output=True,
    #             text=True
    #         )
    #
    #         # Send the output of the executed code
    #         await self.send_json(response_fun(1, {
    #             'message': 'Success',
    #             'output': execution_process.stdout,
    #             'error': execution_process.stderr
    #         }))
    #
    #         await self.close()
    #
    #     except TimeoutError:
    #         await self.send_json(response_fun(0, "Took Too Long To Run"))
    #         await self.close()
    #     except Exception as e:
    #         await self.send_json(response_fun(0, "Internal Server Error"))
    #         await self.close()
    #     finally:
    #         # Cleanup temporary files
    #         if os.path.exists(cpp_file_path):
    #             os.remove(cpp_file_path)
    #         if os.path.exists(executable_path):
    #             os.remove(executable_path)

    async def disconnect(self, code):
        print('disconnected', code)
