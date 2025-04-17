import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file: ")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #fetch unique users

    userList = df['users'].unique().tolist()
    userList.remove('group Notification')
    userList.sort()
    userList.insert(0,"Overall")
    selectedUser = st.sidebar.selectbox("Show Analysis wrt: ", userList)

    if st.sidebar.button("Show Analysis"):
        numMsgs, numWords, numMedia, numLinks = helper.fetch_stats(selectedUser, df)
        st.title('Top Statistics')
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


        # montly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthlyTimeline(selectedUser, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.dailyTimeline(selectedUser, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # activity map

        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busyDay = helper.weekActivityMap(selectedUser, df)
            fig, ax = plt.subplots()
            ax.bar(busyDay.index, busyDay.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            busyMonth = helper.monthActivityMap(selectedUser, df)
            fig, ax = plt.subplots()
            ax.bar(busyMonth.index, busyMonth.values, color='green')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        # finding the busiest user
        if selectedUser == 'Overall':
            st.title("Most Busy Users")
            x, newDf = helper.mostBusyUsers(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(newDf)
        
        # word cloud
        st.title("Word Cloud")
        df_wc = helper.createWordCloud(selectedUser, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words
        st.title("Most Common words")
        mostCommonDf = helper.mostCommonWords(selectedUser, df)
        fig, ax = plt.subplots()
        ax.barh(mostCommonDf[0], mostCommonDf[1])
        st.pyplot(fig)

        # emoji analysis
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        emojiDf = helper.emojiHelper(selectedUser, df)
        with col1:
            st.dataframe(emojiDf)
        with col2:
            fig = px.pie(emojiDf.head(10), values=1, names=0)
            st.plotly_chart(fig)
        
        st.title("Weekly Activity Map")
        userHeatMap = helper.dailyActivityMap(selectedUser, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(userHeatMap)
        st.pyplot(fig)
       