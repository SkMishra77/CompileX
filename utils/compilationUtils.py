import asyncio
import json

import aioboto3

from arena.models import TestCaseModel

# Create an async session
session = aioboto3.Session(region_name='ap-south-1')


async def compileCpp_async(code, user_input):
    async with session.client('lambda') as lambda_client:
        payload = {
            "code": code,
            "user_input": user_input
        }
        response = await lambda_client.invoke(
            FunctionName='compileXcpp',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        response_payload = json.loads(await response['Payload'].read())
        return response_payload


async def compileCpp_async_with_testcase(code, user_inputs: TestCaseModel):
    async with session.client('lambda') as lambda_client:
        payload = {
            "code": code,
            "user_input": user_inputs.input_case
        }
        response = await lambda_client.invoke(
            FunctionName='compileXcpp',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        response_payload = json.loads(await response['Payload'].read())
        response_payload.update({
            't_id': user_inputs.id,
            'expected_out': user_inputs.output_case,
            'passed': True if response_payload['error'] == False and user_inputs.output_case.strip(' ').strip('\n') ==
                              response_payload['data']['output'].strip(' ').strip('\n') else False,
            "user_input": user_inputs.input_case
        })
        if user_inputs.is_public is False:
            del response_payload['expected_out']
            del response_payload['user_input']

        if response_payload['data']['exec_time'] > 1:
            response_payload['data'] = {
                'message': 'Took too long to run'
            }
        return response_payload


async def invoke_all_testcase_lambdas(code, payloads):
    tasks = [compileCpp_async_with_testcase(code, payload) for payload in payloads]
    return await asyncio.gather(*tasks)
