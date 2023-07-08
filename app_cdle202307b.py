# 以下を「cdle15_app.py」に書き込み
import streamlit as st
import openai
# import secret_keys  # 外部ファイルにAPI keyを格納

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントです。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
#      model = "gpt-4",
        model = "gpt-3.5-turbo",
        messages = messages,
#      temperature = 2.0
#      temperature = 1.5
        temperature = 1.0
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("ChatGPT アプリ")
st.image("cdle15_app_photo.png")
st.write(" ◤◢◤◢　個人情報や機密情報は入力しないでください　◤◢◤◢  ")

user_input = st.text_input("▼ プロンプトを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🔷 "
        if message["role"]=="assistant":
            speaker="🤖 "

        st.write(speaker + ": " + message["content"])
