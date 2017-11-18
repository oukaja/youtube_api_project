# dependencies
import isodate
import requests

# YouTube api key
api_key = "AIzaSyDt0lPqnHIgW8wcEI_Xzt5ifdYRAivn2og"

# Video id
VIDEO_ID = "_4CmV4HUnPA"

# Max Results
MAX_RESULT = "50"

# get all info of videos
video_info = []

# get all comments
video_comments = []

# Google API
url_video_comments = "https://www.googleapis.com/youtube/v3/commentThreads?key=%s&textFormat=plainText&part=snippet&videoId=%s&maxResults=%s" % (
    api_key,
    VIDEO_ID,
    MAX_RESULT)
# url_video_info = "https://www.googleapis.com/youtube/v3/videos?key=%s&part=snippet,contentDetails,statistics&id=%s&maxResults=%s" % (
#     api_key,
#     VIDEO_ID,
#     MAX_RESULT)

# get Data
# video_info = requests.get(url_video_info).json()
video_comments = requests.get(url_video_comments).json()

# for i in range(0, len(video_info["items"])):
#     video_item = video_info["items"]
#     try:
#         snippet = video_item[i]["snippet"]
#         contentDetails = video_item[i]["contentDetails"]
#         statistics = video_item[i]["statistics"]
#     except:
#         continue

snippet_c = list()

for i in range(0, len(video_comments["items"])):
    video_comment_item = video_comments["items"]
    try:
        snippet_c.append(video_comment_item[i]["snippet"]["topLevelComment"])
    except:
        continue

print(snippet_c[1])

# # snippet
# print("-------------------------------------------------------------------")
# print("snippet attributs")
# print("channel Id : " + snippet["channelId"])
# print("published At : " + snippet["publishedAt"])
# print("title : " + snippet["title"])
# print("description : " + snippet["description"])
# print("channel Title : " + snippet["channelTitle"])
# print("category Id : " + snippet["categoryId"])
# print("tags : ")
# for tag in snippet["tags"]:
#     print("\t" + tag)
# print("-------------------------------------------------------------------")
#
# # contentDetails
# print("-------------------------------------------------------------------")
# print("contentDetails attributs")
# print("duration : " + str(isodate.parse_duration(contentDetails["duration"])))
# print("dimension : " + contentDetails["dimension"])
# print("-------------------------------------------------------------------")
#
# # statistics
# print("-------------------------------------------------------------------")
# print("statistics attributs")
# print("viewCount : " + statistics["viewCount"])
# print("likeCount : " + statistics["likeCount"])
# print("dislikeCount : " + statistics["dislikeCount"])
# print("commentCount : " + statistics["commentCount"])
# print("-------------------------------------------------------------------")

# snippet comment
print("-------------------------------------------------------------------")
print("snippet comments")
print("\t-------------------------------------------------------------------")
for snippet_c_user in snippet_c:
    print("\tauthorDisplayName : " + snippet_c_user["snippet"]["authorDisplayName"])
    print("\tauthorProfileImageUrl : " + snippet_c_user["snippet"]["authorProfileImageUrl"])
    print("\tauthorChannelUrl : " + snippet_c_user["snippet"]["authorChannelUrl"])
    print("\tauthorChannelId : " + snippet_c_user["snippet"]["authorChannelId"]["value"])
    print("\ttextDisplay : " + snippet_c_user["snippet"]["textDisplay"])
    print("\ttextOriginal : " + snippet_c_user["snippet"]["textOriginal"])
    print("\tlikeCount : " + str(snippet_c_user["snippet"]["likeCount"]))
    print("\tpublishedAt : " + snippet_c_user["snippet"]["publishedAt"])
    print("\t-------------------------------------------------------------------")
print("-------------------------------------------------------------------")

# create a dataframe from the data
