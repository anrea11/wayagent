import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="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")

ASSISTANT_ID = "asst_wMoF5ChP2bZCsincck9Ksflk"

st.title("Way Babulai_1")


# Chat history save
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    role, content = msg
    st.chat_message(role).write(content)

# User input
user_input = st.chat_input("Асуултаа асуугаарай хө")
if user_input:
    st.session_state.messages.append(("user", user_input))
    st.chat_message("user").write(user_input)

    # --- Create a thread ---
    thread = client.beta.threads.create(
        messages=[{"role": "user", "content": user_input}]
    )

    # --- Run the assistant ---
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # --- Poll until completed ---
    import time
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
        if run_status.status == "completed":
            break
        time.sleep(1)

    # --- Get response messages ---
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    assistant_reply = messages.data[0].content[0].text.value
    st.session_state.messages.append(("assistant", assistant_reply))
    st.chat_message("assistant").write(assistant_reply)

