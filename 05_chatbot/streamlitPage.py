import streamlit as st  # Streamlit 라이브러리 임포트하여 웹 앱 생성
import requests  # HTTP 요청 생성을 위한 requests 라이브러리 임포트
import json  # JSON 파싱

# AWS Lambda 함수 URL 엔드포인트 정의
ENDPOINT_LAMBDA_URL = "YOUR LAMBDA FUNCTION URL"

# 웹 앱 제목 설정
st.title("Chatbot powered by Bedrock")

# 세션 상태에 메시지 없으면 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 세션 상태에 저장된 메시지 순회하며 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # 채팅 메시지 버블 생성
        st.markdown(message["content"])  # 메시지 내용 마크다운으로 렌더링

# 사용자로부터 입력 받음
if prompt := st.chat_input("Message Bedrock..."):
    # 사용자 메시지 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):  # 사용자 메시지 채팅 메시지 버블 생성
        st.markdown(prompt)  # 사용자 메시지 표시

    with st.chat_message("assistant"):  # 보조 메시지 채팅 메시지 버블 생성
        with st.spinner("Thinking..."):  # 처리 중 스피너 표시
            # Lambda 함수에 POST 요청 보냄
            response_raw = requests.post(ENDPOINT_LAMBDA_URL, json={"prompt": prompt})
            print(f"raw: {response_raw}")  # 디버깅을 위한 원시 응답 출력
            response_json = response_raw.json()  # 응답 JSON으로 파싱
            print(f"json: {response_json}")  # 디버깅을 위한 JSON 응답 출력
            # model_output = response_json.get("output")
            model_output = response_raw.json(); # 모델 출력 추출
            print(model_output)  # 모델 출력 출력

        st.write(model_output)  # 모델 출력 표시

    # 보조 응답 세션 상태에 추가
    st.session_state.messages.append({"role": "assistant", "content": model_output})
