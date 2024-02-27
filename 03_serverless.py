import json
import boto3


# AWS Lambda의 메인 핸들러 함수
# event는 이벤트 데이터를 담고 있으며, context는 런타임 정보를 담음
def lambda_handler(event, context):
    # 받은 이벤트를 로깅
    print(f"Received event: {event}")

    # boto3 라이브러리 버전을 확인
    boto3_version = boto3.__version__
    print(f"boto3 version: {boto3_version}")

    try:
        # HTTP GET 요청을 확인
        if event["requestContext"]["http"]["method"] == "GET":
            return generate_response(None, "GET 요청을 처리했습니다.")

        # Bedrock Runtime 서비스 클라이언트를 생성
        bedrock_runtime = boto3.client(
            service_name="bedrock-runtime", region_name="us-east-1"
        )

        # 이벤트에서 'body'를 추출하고 JSON으로 변환
        request_body = json.loads(event.get("body"))
        prompt = (
            request_body.get("prompt")
            if "prompt" in request_body
            else "Amazon Bedrock이 뭐야? 3문장 이내로 답변해"
        )

        # 처리할 프롬프트를 로깅
        print(f"Processing prompt: {prompt}")

        # Bedrock Runtime에 전송할 요청 파라미터 세팅
        # https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html
        body = json.dumps({
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "temperature": 0,
            "top_p": 0.01,
            "max_tokens_to_sample": 1000,
        })

        # Bedrock Runtime 모델을 호출하고, 응답 받기
        response = bedrock_runtime.invoke_model(body=body, modelId="anthropic.claude-v2")
        response_body = json.loads(response.get("body").read())
        model_response = response_body["completion"]

        # 모델의 응답을 로깅, 클라이언트에 반환
        print(f"Model response: {model_response}")
        return generate_response(None, model_response)
    except Exception as e:
        # 예외가 발생하면 에러 메시지를 반환
        return generate_response(e, "Error occurred!")


# 응답 생성 함수
# err가 None이면 성공, 그렇지 않으면 에러 메시지를 반환
def generate_response(err, res):
    if err:
        print(f"!!!!!!!!!!!!{err, res}")

    return {
        "statusCode": "400" if err else "200",
        "body": json.dumps(res, ensure_ascii=False),
        "headers": {"Content-Type": "application/json"},
    }
