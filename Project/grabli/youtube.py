from googleapiclient.discovery import build

def get_video_details(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    video_details = {}
    if "items" in response and len(response["items"]) > 0:
        item = response["items"][0]["snippet"]
        video_details = {
            "title": item["title"],
            "author": item["channelTitle"],
            "description": item["description"],
            "thumbnail": item["thumbnails"]["high"]["url"]
        }
    return video_details

def get_video_comments(video_id, api_key, max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comment_data = {
                "author": comment["authorDisplayName"],
                "text": comment["textDisplay"],
                "published_at": comment["publishedAt"],
                "likes": comment["likeCount"],
                "replies": []
            }
            if "replies" in item:
                for reply in item["replies"]["comments"]:
                    reply_snippet = reply["snippet"]
                    comment_data["replies"].append({
                        "author": reply_snippet["authorDisplayName"],
                        "text": reply_snippet["textDisplay"],
                        "published_at": reply_snippet["publishedAt"],
                        "likes": reply_snippet["likeCount"]
                    })
            comments.append(comment_data)
        request = youtube.commentThreads().list_next(request, response)
    return comments


