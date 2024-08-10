import json

import aioboto3

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
