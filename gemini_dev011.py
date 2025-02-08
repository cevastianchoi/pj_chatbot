import google.generativeai as genai
import streamlit as st

api_key = st.secrets["chatbot_key"]
genai.configure(api_key)

st.title("Turtle Gym chatbot")

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

model = load_model()

if "chat_session" not in st.session_state:
    # 채팅 세션 초기화(챗 시작)
    st.session_state["chat_session"] = model.start_chat(history=[]) 
    
# 이전 챗 내용 표시, content
for content in st.session_state.chat_session.history:
    # 사용자와 gemini 응답 구분
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)
        
if prompt := st.chat_input("메시지를 입력하세요. :"):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("ai"):
        message_placeholder = st.empty()
        # 전체 메시지
        full_response = ""
        # 글자를 타이핑하듯이 출력하는 기능
        with st.spinner("메시지 답변 처리 중 입니다."):
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            for chunk in response:
                #각각의 답변들을 모아서 하나로 만듬
                full_response += chunk.text
                #세션을 유지하면서 답변을 하는 과정
                message_placeholder.markdown(full_response)


