import imageio
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pymongo
from datetime import datetime
import textwrap
import moviepy.editor as mp

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

def imageNoHighlight(time, total):
    temp = total.splitlines(keepends=True)
    font = ImageFont.truetype("C:\\Windows\\Fonts\\Times.ttf", 16)
    image_size = (630, 908)
    image = Image.new("RGB", image_size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    y_text = 18
    width = 90
    wraped = []
    # might still need textwrap
    for each in temp:
        wraped.extend(
            textwrap.wrap(each, width=width, replace_whitespace=False, break_long_words=False, drop_whitespace=False))
    for line in wraped:
        draw.text((10, y_text), line, font=font, fill=(0, 0, 0))
        y_text += 18
    draw.text((450, 3), time, font=font, fill=(0, 0, 0))
    return np.asarray(image)

def main():
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

    allProductsQuery = [{"project": "63dbf507031f82f53e24056f"},]
    for each in allProductsQuery:
        print(each)
        gif = []
        revisions = []
        i = 0
        temp = collection.find(each)
        original = ""
        for doc in temp:
            if i == 0:
                try:
                    for part in doc["revision"]:
                        if part[0] == 0 or part[0] == -1:
                            original = original + part[1]
                    text = original
                    gif.append(imageNoHighlight(doc["timestamp"][4:-33], "".join(text)))
                    revisions.append([doc["timestamp"][4:-33], doc["timestamp"][4:-33], doc["text"]])
                except:
                    gif.append(imageNoHighlight(doc["timestamp"][4:-33], "".join(doc["text"])))
            else:
                revisions.append([doc["timestamp"][4:-33], doc["timestamp"][4:-33], doc["text"]])
            i += 1
        revisions = sorttime(revisions)
        for snap in revisions:
            gif.append(imageNoHighlight(snap[1],snap[2]))
        #gif.append(imageNoHighlight("".join(text)))
        imageio.mimsave(each["project"]+".gif", gif, "GIF", duration=0.7)
        clip = mp.VideoFileClip(each["project"]+".gif")
        clip.write_videofile(each["project"]+".mp4")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
