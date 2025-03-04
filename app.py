import streamlit as st
def main():
    st.title("Chatbot")
    if "history" not in st.session_state:
        st.session_state["history"] = []

    from chain import handle_chat, createAgent
    st.sidebar.title("Chatbot")
    st.sidebar.write("This is a chatbot that can answer questions based on a given context. You can enter url for rag here.")
    url=st.sidebar.text_input("Enter your url:", key="url")
    with st.spinner("Loading"):
        if st.sidebar.button("Submit"):
            app,config=createAgent(url)
            st.session_state["history"] = []
            st.session_state["app"]=app
            st.session_state["config"]=config
            st.sidebar.success("Chatbot is ready to use.")
            
    # Function to handle message sending
    def send_message():
        if st.session_state.user_input:
            user_message = st.session_state.user_input
            if user_message.lower()=="quit" or user_message.lower()=="exit":
                st.session_state["history"].append(("You", user_message))
                st.session_state["history"].append(("CT", "Goodbye!"))
                st.markdown(f"<div style='text-align: right;'><b>You:</b> {user_message}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align: left;'><b>CT:</b> Goodbye!</div>", unsafe_allow_html=True)
                st.stop()
            app=st.session_state["app"]
            config=st.session_state["config"]
            with st.spinner("Generating"):
                response = handle_chat(user_message,app,config)
            st.session_state["history"].append(("You", user_message))
            st.session_state["history"].append(("CT", response))
            st.session_state.user_input = ""

    user_input = st.text_input(
        "Enter your message:", key="user_input", on_change=send_message
    )

    for idx, (user, message) in enumerate(reversed(st.session_state["history"])):
        if user == "You":
            st.markdown(f"<div style='text-align: right;'><b>You:</b> {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left;'><b>CT:</b> {message}</div>", unsafe_allow_html=True)
    st.divider()

if __name__=="__main__":
    main()
