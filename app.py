import streamlit as st
import preprocessor, helper

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file: ")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique users

    userList = df['users'].unique().tolist()
    userList.remove('group Notification')
    userList.sort()
    userList.insert(0,"Overall")
    selectedUser = st.sidebar.selectbox("Show Analysis wrt: ", userList)

    if st.sidebar.button("Show Analysis"):
        numMsgs, numWords, numMedia, numLinks = helper.fetch_stats(selectedUser, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages  ")
            st.title(numMsgs)
        with col2:
            st.header("Total Words")
            st.title(numWords)
        with col3:
            st.header("Media Shared")
            st.title(numMedia)
        with col4:
            st.header("Links Shared")
            st.title(numLinks)