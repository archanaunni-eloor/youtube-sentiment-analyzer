import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from textblob import TextBlob
import plotly.express as px
import streamlit as st
API_KEY = st.secrets["YOUTUBE_API_KEY"] 
youtube = build('youtube', 'v3', developerKey=API_KEY)

# --- 2. HELPER FUNCTIONS ---

def search_videos(query, max_results=10):
    """യൂട്യൂബിൽ നിന്ന് വീഡിയോകൾ സെർച്ച് ചെയ്യുന്നു"""
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()
    video_data = []
    for item in response['items']:
        video_data.append({
            'Title': item['snippet']['title'],
            'Video_ID': item['id']['videoId'],
            'Published_At': item['snippet']['publishedAt'],
            'Channel': item['snippet']['channelTitle']
        })
    return pd.DataFrame(video_data)

def get_video_stats(video_ids):
    """വീഡിയോയുടെ ലൈക്ക്, വ്യൂസ് എന്നിവ ശേഖരിക്കുന്നു"""
    request = youtube.videos().list(
        part="statistics",
        id=','.join(video_ids)
    )
    response = request.execute()
    stats = []
    for item in response['items']:
        stats.append({
            'Video_ID': item['id'],
            'Views': int(item['statistics'].get('viewCount', 0)),
            'Likes': int(item['statistics'].get('likeCount', 0)),
            'Comments': int(item['statistics'].get('commentCount', 0))
        })
    return pd.DataFrame(stats)

def get_sentiment(text):
    """ടെക്സ്റ്റിന്റെ സെന്റിമെന്റ് കണ്ടെത്തുന്നു"""
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

def get_video_comments_sentiment(video_id):
    """വീഡിയോ കമന്റുകൾ വിശകലനം ചെയ്ത് സ്കോർ നൽകുന്നു"""
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=50
        )
        response = request.execute()
        sentiments = [get_sentiment(item['snippet']['topLevelComment']['snippet']['textDisplay']) 
                      for item in response['items']]
        
        if sentiments:
            pos_perc = (sentiments.count('Positive') / len(sentiments)) * 100
            return round(pos_perc, 2)
    except:
        return 0
    return 0

# --- 3. STREAMLIT UI ---

st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

st.title("📊 YouTube Sentiment & Engagement Analyzer")
st.markdown("""
With this app, you can perform real-time analysis of YouTube video trends and audience sentiment on any topic.
""")

# Sidebar for Input
st.sidebar.header("Search Parameters")
search_query = st.sidebar.text_input("Enter Topic", "Data Science Malayalam")
video_count = st.sidebar.slider("Number of Videos", 5, 20, 10)

if st.sidebar.button("Run Analysis"):
    with st.spinner('Analyzing YouTube Data...'):
        # Step 1: Search
        df_videos = search_videos(search_query, video_count)
        
        # Step 2: Get Stats
        v_ids = df_videos['Video_ID'].tolist()
        df_stats = get_video_stats(v_ids)
        
        # Merge Data
        final_df = pd.merge(df_videos, df_stats, on='Video_ID')
        
        # Step 3: Sentiment Analysis
        final_df['Positive_Sentiment_%'] = final_df['Video_ID'].apply(get_video_comments_sentiment)
        
        # Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Videos Analyzed", len(final_df))
        col2.metric("Avg Views", int(final_df['Views'].mean()))
        col3.metric("Highest Sentiment Score", f"{final_df['Positive_Sentiment_%'].max()}%")

        # Step 4: Visualization
        st.subheader("Public Sentiment vs Video Engagement")
        fig = px.scatter(final_df, 
                         x="Views", 
                         y="Positive_Sentiment_%",
                         size="Likes", 
                         color="Channel",
                         hover_name="Title",
                         log_x=True,
                         title="Engagement Analysis (Size = Likes)")
        st.plotly_chart(fig, use_container_width=True)

        # Show Data Table
        st.subheader("Raw Data")
        st.dataframe(final_df.sort_values(by='Positive_Sentiment_%', ascending=False))

else:
    st.info("← Please provide a topic in the side box and then click 'Run Analysis'.")
