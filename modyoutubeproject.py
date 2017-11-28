# dependencies
import isodate
import requests
from hammock import Hammock as GendreAPI
from textblob import TextBlob
from string import punctuation
import re
from nltk.corpus import stopwords
from pandas import DataFrame
import matplotlib.pyplot as plt
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['modyoutubeproject']
collection = db['commentaires']

# YouTube api key
api_key = "AIzaSyDt0lPqnHIgW8wcEI_Xzt5ifdYRAivn2og"

# Gender API
gendre = GendreAPI("http://api.namsor.com/onomastics/api/json/gendre")

# Video id
VIDEO_ID = "mn6Ia5e_suY"

# Max Results
MAX_RESULT = "10"

# get all info of videos
video_info = []

# get all comments
video_comments = []

# get all comments replies
video_comments_replies = []

# Google API
url_video_comments = "https://www.googleapis.com/youtube/v3/commentThreads?key=%s&textFormat=plainText&part=snippet,replies&videoId=%s&maxResults=%s" % (
    api_key,
    VIDEO_ID,
    MAX_RESULT)
url_video_info = "https://www.googleapis.com/youtube/v3/videos?key=%s&part=snippet,contentDetails,statistics&id=%s&maxResults=%s" % (
    api_key,
    VIDEO_ID,
    MAX_RESULT)

# get Data
video_info = requests.get(url_video_info).json()
video_comments = requests.get(url_video_comments).json()

for i in range(0, len(video_info["items"])):
    video_item = video_info["items"]
    try:
        snippet = video_item[i]["snippet"]
        contentDetails = video_item[i]["contentDetails"]
        statistics = video_item[i]["statistics"]
    except:
        continue

snippet_c = list()
snippet_c_replies = list()

for i in range(0, len(video_comments["items"])):
    video_comment_item = video_comments["items"]
    try:
        snippet_c.append(video_comment_item[i]["snippet"])
        snippet_c_replies.append(video_comment_item[i]["replies"]["comments"])
    except:
        continue


def nettoyer_la_phrase(phrase):
    phrase = re.sub(r"(?:\@|https?\://)\S+|\n+", "", phrase.lower())
    sent = TextBlob(phrase)
    sent.correct()
    clean = ""
    for sentence in sent.sentences:
        words = sentence.words
        words = [''.join(c for c in s if c not in punctuation) for s in words]
        words = [s for s in words if s]
        clean += " ".join(words)
        clean += ". "
    return clean


def commentaire_vers_mongodb():
    commentaires = list()
    for snippet_c_user in snippet_c:
        commentaires.append(snippet_c_user["topLevelComment"]["snippet"]["textDisplay"])
    commentaires = (nettoyer_la_phrase(p) for p in commentaires)
    for commentaire in commentaires:
        comment = {"comment": commentaire}
        collection.insert(comment)


def commentaire_de_mongodb():
    col = db.get_collection("commentaires")
    for document in col.find({}):
        print(document['comment'])


def video_info_comments():
    # snippet
    print("-------------------------------------------------------------------")
    print("snippet attributs")
    print("channel Id : " + snippet["channelId"])
    print("published At : " + snippet["publishedAt"])
    print("title : " + snippet["title"])
    print("description : " + snippet["description"])
    print("channel Title : " + snippet["channelTitle"])
    print("category Id : " + snippet["categoryId"])
    print("tags : ")
    for tag in snippet["tags"]:
        print("\t" + tag)
    print("-------------------------------------------------------------------")

    # contentDetails
    print("-------------------------------------------------------------------")
    print("contentDetails attributs")
    print("duration : " + str(isodate.parse_duration(contentDetails["duration"])))
    print("dimension : " + contentDetails["dimension"])
    print("-------------------------------------------------------------------")

    # statistics
    print("-------------------------------------------------------------------")
    print("statistics attributs")
    print("viewCount : " + statistics["viewCount"])
    print("likeCount : " + statistics["likeCount"])
    print("dislikeCount : " + statistics["dislikeCount"])
    print("commentCount : " + statistics["commentCount"])
    print("-------------------------------------------------------------------")

    # snippet comment
    print("-------------------------------------------------------------------")
    print("snippet comments")
    print("\t-------------------------------------------------------------------")
    for snippet_c_user in snippet_c:
        print("\tauthorDisplayName : " + snippet_c_user["topLevelComment"]["snippet"]["authorDisplayName"])
        print("\tauthorProfileImageUrl : " + snippet_c_user["topLevelComment"]["snippet"]["authorProfileImageUrl"])
        print("\tauthorChannelUrl : " + snippet_c_user["topLevelComment"]["snippet"]["authorChannelUrl"])
        print("\tauthorChannelId : " + snippet_c_user["topLevelComment"]["snippet"]["authorChannelId"]["value"])
        print("\ttextDisplay : " + snippet_c_user["topLevelComment"]["snippet"]["textDisplay"])
        print("\ttextOriginal : " + snippet_c_user["topLevelComment"]["snippet"]["textOriginal"])
        print("\tlikeCount : " + str(snippet_c_user["topLevelComment"]["snippet"]["likeCount"]))
        print("\tpublishedAt : " + snippet_c_user["topLevelComment"]["snippet"]["publishedAt"])
        print("\tcanReply : " + str(snippet_c_user["canReply"]))
        print("\ttotalReplyCount : " + str(snippet_c_user["totalReplyCount"]))
        print("\tisPublic : " + str(snippet_c_user["isPublic"]))
        print("\t-------------------------------------------------------------------")
    print("\t\t-------------------------------------------------------------------")

    for k in range(snippet_c_replies.__len__()):
        reply = snippet_c_replies[k][0]
        print("\t\tauthorDisplayName : " + reply["snippet"]["authorDisplayName"])
        print("\t\tauthorProfileImageUrl : " + reply["snippet"]["authorProfileImageUrl"])
        print("\t\tauthorChannelUrl : " + reply["snippet"]["authorChannelUrl"])
        print("\t\tauthorChannelId : " + reply["snippet"]["authorChannelId"]["value"])
        print("\t\ttextDisplay : " + reply["snippet"]["textDisplay"])
        print("\t\ttextOriginal : " + reply["snippet"]["textOriginal"])
        print("\t\tlikeCount : " + str(reply["snippet"]["likeCount"]))
        print("\t\tpublishedAt : " + reply["snippet"]["publishedAt"])
        print("\t\tupdatedAt : " + reply["snippet"]["publishedAt"])
        print("\t\t-------------------------------------------------------------------")
    print("-------------------------------------------------------------------")


# Q1
def nombre_de_commentaire():
    print("nombre de commentaire : " + statistics["commentCount"])


# Q2
def commentaire_le_plus_populaire_du_premier_Q1():
    likecount = 0
    commentaire = ""
    for snippet_c_user in snippet_c:
        if snippet_c_user["topLevelComment"]["snippet"]["likeCount"] > likecount:
            likecount = snippet_c_user["topLevelComment"]["snippet"]["likeCount"]
            commentaire = snippet_c_user["topLevelComment"]["snippet"]["textDisplay"]
    print("Nombre de j'aime : " + str(likecount))
    print("Texte  : " + commentaire)


# Q3
def dix_termes_les_plus_frequent():
    commentaires = list()
    for snippet_c_user in snippet_c:
        commentaires.append(snippet_c_user["topLevelComment"]["snippet"]["textDisplay"])
    commentaires = (nettoyer_la_phrase(p) for p in commentaires)
    commentaires_dans_une_ligne = TextBlob(' '.join(commentaires))
    # print(commentaires_dans_une_ligne.noun_phrases)
    feature_count = dict()
    for phrase in commentaires_dans_une_ligne.noun_phrases:
        count = 0
        for word in phrase.split():
            if word not in stopwords.words('english'):
                count += commentaires_dans_une_ligne.words.count(word)
        # print(phrase + ": " + str(count))
        feature_count[phrase] = count
    df = DataFrame().from_dict(list(feature_count.items()))
    df.columns = ['termes', 'frequence']
    df.sort_values('frequence', ascending=False, inplace=True)
    plt.style.use('ggplot')
    df.head(n=10).plot(x='termes', y='frequence', kind='bar')
    plt.show()


# Q4
def frequence_par_terme_en_entree(terme=" "):
    commentaires = list()
    for snippet_c_user in snippet_c:
        commentaires.append(snippet_c_user["topLevelComment"]["snippet"]["textDisplay"])
    commentaires = (nettoyer_la_phrase(p) for p in commentaires)
    commentaires_dans_une_ligne = TextBlob(' '.join(commentaires))
    # print(commentaires_dans_une_ligne.noun_phrases)
    feature_count = dict()
    for phrase in commentaires_dans_une_ligne.noun_phrases:
        count = 0
        for word in phrase.split():
            if word not in stopwords.words('english'):
                count += commentaires_dans_une_ligne.words.count(word)
        # print(phrase + ": " + str(count))
        feature_count[phrase] = count
    df = DataFrame().from_dict(list(feature_count.items()))
    df.columns = ['termes', 'frequence']
    df.sort_values('frequence', ascending=False, inplace=True)
    freq = 0
    for index, row in df.iterrows():
        # print(row["termes"], row["frequence"])
        if row["termes"] == terme or row["termes"] in terme or terme in row["termes"]:
            # print(row["termes"], row["frequence"])
            freq += int(row["frequence"])
    print("fréquence dans le dataset traité ", str(freq))
    print("moyenne cette expression est citée dans un commentaire " + str(freq / int(MAX_RESULT)))


# Q5
def proba_conditionnel_A_sachant_B(A="", B=""):
    # on considere que A et B sont deux evenements independants
    commentaires = list()
    for snippet_c_user in snippet_c:
        commentaires.append(snippet_c_user["topLevelComment"]["snippet"]["textDisplay"])
    commentaires = (nettoyer_la_phrase(p) for p in commentaires)
    commentaires_dans_une_ligne = TextBlob(' '.join(commentaires))
    # print(commentaires_dans_une_ligne.noun_phrases)
    feature_count = dict()
    for phrase in commentaires_dans_une_ligne.noun_phrases:
        count = 0
        for word in phrase.split():
            if word not in stopwords.words('english'):
                count += commentaires_dans_une_ligne.words.count(word)
        # print(phrase + ": " + str(count))
        feature_count[phrase] = count
    df = DataFrame().from_dict(list(feature_count.items()))
    df.columns = ['termes', 'frequence']
    df.sort_values('frequence', ascending=False, inplace=True)
    # print(df.items)
    freq_A = 0
    for index, row in df.iterrows():
        if row["termes"] == A or row["termes"] in A or A in row["termes"]:
            freq_A += int(row["frequence"])
    freq_B = 0
    for index, row in df.iterrows():
        if row["termes"] == B or row["termes"] in B or B in row["termes"]:
            freq_B += int(row["frequence"])
    if freq_A == 0:
        print("proba de B sachant A vaut : ", str("{0:.2f}".format(freq_B / df.size)))
    else:
        # print("proba de B", str("{0:.2f}".format(freq_B / df.size)))
        prob_AB = (freq_B / df.size) * (freq_A / df.size)
        print("proba de B sachant A vaut : ", str("{0:.2f}".format(prob_AB / (freq_A / df.size))))


# Q6
def pourcentage_sexe():
    f = 0
    u = 0
    m = 0
    reel = 0
    for snippet_c_user in snippet_c:
        result = ''.join(
            [i for i in nettoyer_la_phrase(snippet_c_user["topLevelComment"]["snippet"]["authorDisplayName"]) if
             not i.isdigit()])
        # print(result.split(" ", 1)[0] + " " + result.split(" ", 1)[1].replace(" ", "").replace(".", ""))
        resp = gendre(result.split(" ", 1)[0], result.split(" ", 1)[1].replace(" ", "").replace(".", "")).GET()
        # print(resp.json().get('gender'))
        if resp.json().get('gender') == "female":
            f += 1
        elif resp.json().get('gender') == "unknown":
            u += 1
        else:
            m += 1
    reel = f + m - u
    pourcentage = float("{0:.2f}".format((f / (int(MAX_RESULT) - u)) * 100))
    print("pourcentage des commentaires publiés par les femmes : " + str(pourcentage) + "%")
    print("pourcentage des commentaires publiés par les hommes : " + str(100 - pourcentage) + "%")


if __name__ == "__main__":
    # nombre_de_commentaire()
    # commentaire_le_plus_populaire_du_premier_Q1()
    # dix_termes_les_plus_frequent()
    # frequence_par_terme_en_entree(terme="new youtube channelfor")
    # pourcentage_sexe()
    # commentaire_vers_mongodb()
    # commentaire_de_mongodb()
    proba_conditionnel_A_sachant_B(A="youtube", B="videos")
    # print(1)
