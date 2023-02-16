from flask import Flask, render_template
import imageio
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pymongo
from datetime import datetime
import textwrap

from flask import request
from flask import jsonify

app = Flask(__name__)

def sorttime(rev):
    months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr':4,
         'May':5,
         'Jun':6,
         'Jul':7,
         'Aug':8,
         'Sep':9,
         'Oct':10,
         'Nov':11,
         'Dec':12
        }
    for i in range(len(rev)):
        rev[i][0] = str(months[rev[i][0][:3]]) + rev[i][0][3:]
        ml = len(rev[i][0].split(':')[-1])
        if ml ==2:
            rev[i][0] = rev[i][0][:-2]+"0"+rev[i][0][-2:]
        elif ml ==1:
            rev[i][0] = rev[i][0][:-1] + "00" + rev[i][0][-1:]
        rev[i][0] = datetime.strptime(rev[i][0], '%m %d %Y %H:%M:%S:%f')
    # try:
    rev.sort(key=lambda date: date[0])
    # except IndexError:
    #     print(rev[i])
    return rev

# def imageNoHighlight(time, total):
#     temp = total.splitlines(keepends=True)
#     font = ImageFont.truetype("arial.ttf", 16)
#     image_size = (630, 908)
#     image = Image.new("RGB", image_size, (255, 255, 255))
#     draw = ImageDraw.Draw(image)
#     y_text = 18
#     width = 90
#     wraped = []
#     # might still need textwrap
#     for each in temp:
#         wraped.extend(
#             textwrap.wrap(each, width=width, replace_whitespace=False, break_long_words=False, drop_whitespace=False))
#     for line in wraped:
#         draw.text((10, y_text), line, font=font, fill=(0, 0, 0))
#         y_text += 18
#     draw.text((450, 3), time, font=font, fill=(0, 0, 0))
#     # return np.asarray(image)
#     return wraped


def generate(projectID="63dbf50ec6e8254235e3f8e8"):
    conntention_string = 'mongodb://rewarddb:YLpPh8bP5zVDvq2dwm614bta4OXYNi0g9vcMg0FEu1lZwBIT5rSze7LUOdZXh34UGYqGf8jn8cKAACDbm8zvKA==@rewarddb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@rewarddb@'
    DB_NAME = "flaskdb"
    COLLECTION_NAME = "flaskdb.activity"
    client = pymongo.MongoClient(conntention_string)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    if COLLECTION_NAME not in db.list_collection_names():
        # Creates a unsharded collection that uses the DBs shared throughput
        db.command(
            {"customAction": "CreateCollection", "collection": COLLECTION_NAME}
        )
        print("Created collection '{}'.\n".format(COLLECTION_NAME))
    else:
        print("Using collection: '{}'.\n".format(COLLECTION_NAME))

    allProductsQuery = [{"project": projectID}]
    revisions = []
    for each in allProductsQuery:
        # print(each)
        i = 0
        temp = collection.find(each)
        original = ""
        for doc in temp:
            change = []
            if doc['state'] == 0 or doc['state'] == 4:
                change.append(doc['changes'])
            elif doc['state'] == 1:
                change.append(doc['changes'])
            elif doc['state'] == 2:
                change.append(doc['copy'])
            elif doc['state'] == 3:
                change.append(doc['changes'])
                change.append(doc['paste'])
            if i == 0:
                for part in doc["revision"]:
                    if part[0] == 0 or part[0] == -1:
                        original = original + part[1]
                text = original
                revisions.append([doc["timestamp"][4:-33], doc["timestamp"][4:-33], doc["text"], change]) 
            else:
                revisions.append([doc["timestamp"][4:-33], doc["timestamp"][4:-33], doc["text"], change])
            i += 1
        revisions = sorttime(revisions)
    return revisions

class LocalStore:
    def __call__(self, f: callable):
        f.__globals__[self.__class__.__name__] = self
        return f

@app.route('/create', methods=('GET', 'POST'))
@LocalStore()
def create():
    if request.method == 'POST':
        info = request.get_json(force=True)
        print("THIS IS THE REQUEST", info)
        projectID = info["projectID"]
        LocalStore.projectID = projectID
        return { "status": "Updated recent writing actions in doc" }

    elif request.method == 'GET':
        projectID = LocalStore.projectID
        if projectID != '':
            content = generate(projectID)
        else:
            content = generate()
        print(content[0])
        return jsonify(content)

@app.route('/')
def index():
    return render_template('index.html')