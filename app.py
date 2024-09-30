from flask import Flask, render_template, request
from googleapiclient.discovery import build

app = Flask(__name__)

# Thay YOUR_API_KEY bằng API Key của bạn
API_KEY = 'AIzaSyCVUxi32JXtp082wuZI0m3lvwf857g1_os'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Hàm tìm kiếm video trên YouTube
def youtube_search(query, max_results=10):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_data = {
                'videoId': search_result['id']['videoId'],
                'title': search_result['snippet']['title'],
                'description': search_result['snippet']['description'],
                'thumbnail': search_result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
    
    return videos

# Trang chủ
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        videos = youtube_search(query)
        return render_template('index.html', videos=videos)
    return render_template('index.html', videos=None)

if __name__ == '__main__':
    app.run(debug=True)