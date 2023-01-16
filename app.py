import streamlit as st
import Preprocessor as prc
import statfetch as sf
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

st.title('CHAT STATISTICS') 
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Kindly upload a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = prc.data_preprocess(data)

    # st.dataframe(df)

    users = df['user'].unique().tolist()
    users.sort()
    users.insert(0,"All")
    name = st.sidebar.selectbox("Analyze", users)

    if st.sidebar.button("Analyze"):
        col1, col2, col3 = st.columns(3)
        message_count,word_count,media_count = sf.stat_fetcher(name,df)

        with col1:
            st.header('Messages')
            st.title(message_count)
        with col2:
            st.header('Words')
            st.title(word_count)
        with col3:
            st.header('Media Shared')
            st.title(media_count)

        # most active users in a group
        if name == 'All':
            st.title('Most Active Users')
            infgrph,percent_df = sf.mostactiveuser(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            
            with col1:
                sns.barplot(x = infgrph.index, y = infgrph.values)
                st.pyplot(fig)
            with col2:
                st.header('Percent data')
                st.dataframe(percent_df)

        ## Word Cloud Generation

        st.title('WordCloud')
        word_cloud = sf.get_wordcloud(name,df)
        fig, ax = plt.subplots()
        ax.imshow(word_cloud)
        plt.grid(None)
        plt.axis('off')
        st.pyplot(fig)

        ## top words used

        st.title('Most Used Words')
        # col1, col2 = st.columns(2)
        
        # with col1:
        #     top_words_used = sf.top_used_words(name,df)
        #     # st.dataframe(top_words_used)
        
        # with col2:
        top_words_used = sf.top_used_words(name,df)
        plt.figure(figsize=(6,6))
        fig,ax = plt.subplots()
        ax.pie(top_words_used['Count'].head(5),labels = top_words_used['Words'].head(5))
        st.pyplot(fig)

        ## Most Emoji Used
        
        st.title('Most Used Emoji')
        col1, col2 = st.columns(2)
        with col1:
            emoji_data = sf.get_emoji(name,df)
            st.dataframe(emoji_data)
        
        with col2:
            plt.figure(figsize = (10,8))
            fig,ax = plt.subplots()
            ax.bar(emoji_data['Emoji'],emoji_data['Count'])
            st.pyplot(fig)



        ## Period monthly
        st.title('Month-Year Chat Analysis')
        month_study = sf.months(name,df)
        fig,ax = plt.subplots()
        ax.bar(month_study['period'],month_study['message'],color = 'blue')
        plt.xticks(rotation = 'vertical')
        plt.grid(False)
        st.pyplot(fig)


        ## Period day wise
        st.title('Day-Month Chat Analysis')
        day_study = sf.days(name,df)
        fig,ax = plt.subplots()
        ax.bar(day_study['period'],day_study['message'],color = 'yellow')
        plt.xticks(rotation = 'vertical')
        ax.grid(False)
        st.pyplot(fig)


        ## Period sole daily
        st.title('Daywise User Activity Analysis')
        weekly_days = sf.weekly_days(name,df)
        fig,ax = plt.subplots()
        ax.bar(weekly_days.index,weekly_days.values,color = 'green')
        plt.xticks(rotation = 'vertical')
        plt.grid(False)
        st.pyplot(fig)


        ## Period sole monthly wise
        st.title('Monthly User Activity Analysis')
        monthly_analysis = sf.monthly_analysis(name,df)
        fig,ax = plt.subplots()
        ax.bar(monthly_analysis.index,monthly_analysis.values,color = 'purple')
        plt.xticks(rotation = 'vertical')
        plt.grid(False)
        st.pyplot(fig)







                 



