import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode('utf-8')
    try:
        df = preprocessor.preprocess(data)
    except:
        df = preprocessor.preprocess1(data)
    st.dataframe(df)

    #fatch unique users
    user_list = df['users'].unique().tolist()
    try:
        user_list.remove('Group Notifications')
    except:
        pass
    user_list.sort(reverse=True)
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    # States level
    if st.sidebar.checkbox('Show Analysis'):
        num_messages,words ,media, links= helper.fatch_state(selected_user,df)
        tab1, tab2 = st.tabs(["📈 Analysis", "🗃 Summary"])
        today = datetime.datetime.now()
        next_year = today.year + 1
        jan_1 = datetime.date(next_year, 1, 1)
        dec_31 = datetime.date(next_year, 12, 31)

        col1,col2,col3,col4 = tab1.columns(4)
        with col1:
            st.header("Total Message")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Shared Media ")
            st.title(media)

        with col4:
            st.header("Shared links")
            st.title(links)

        # Timeline
        tab1.title("Monthly TimelIne")
        timeline=helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(ax.get_xticks(), rotation=90)
        tab1.pyplot(fig)

        # dailyline
        tab1.title("Daily TimelIne")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(ax.get_xticks(), rotation=90)
        tab1.pyplot(fig)

        # Weekly_activity_map
        tab1.title('Activity Map')
        col1, col2 = tab1.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.weekly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(ax.get_xticks(), rotation=45)
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(ax.get_xticks(), rotation=45)
            st.pyplot(fig)

        tab1.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        tab1.pyplot(fig)

        # fiding busiest user in group(Group Level)
        if selected_user=="Overall":
            tab1.title("Bussy User")
            x, new_df=helper.busy_user(df)
            fig, ax = plt.subplots()
            col1,col2 =tab1.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(ax.get_xticks(), rotation=90)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #wordcloud
        tab1.title('WordCloud')
        df_wc=helper.creat_wordclude(selected_user,df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        tab1.pyplot(fig)

        #most common word
        most_common_user = helper.common_word(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_user[0],most_common_user[1])
        plt.xticks(ax.get_xticks(), rotation=90)

        tab1.title("Most common word")
        tab1.pyplot(fig)

        today = datetime.datetime.now().date()
        d = tab2.date_input(
            "Select Date Range for Summary",
            (today, today),
        )

        summary_text=""
        if tab2.button('Get Summary',key="Summary"):
            date1 = d[0].strftime("%m/%d/%Y")
            date2 = d[1].strftime("%m/%d/%Y")
            date1 = str(date1)
            date2 = str(date2)
            chat=helper.summary(date1,date2,df)
            print("hii")
            summary_text=helper.chat_summary(chat)
            print(summary_text)
            tab2.write(summary_text)





