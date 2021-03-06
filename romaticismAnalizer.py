from urllib import request
import glob
import os.path
import time
import json
import sys
import random

DICTINARY_FILE = "dict.json"
DICTINARY_URL = "https://bundr.net/experimental/dict.json"
DICTINARY_FILE_LIST = "dict.list.json"
DICTINARY_FILE_LIST_LOCAL = "dict.list.local.json"
FRANKENSTEIN_PATH = "frankenstein/"
FRANKENSTEIN_FILE = "frankenstein/Frankenstein Chapter 24.txt"
FRANKENSTEIN_URL = "http://www.gutenberg.org/files/84/84-0.txt"
WAIT_TIME_SEC = 200
DICTINARY_API_JSON = "https://api.dictionaryapi.dev/api/v2/entries/en/"
EMOTIONAL_FILE = "emotional.txt"

class CantAccessServerException(Exception):
    pass

class WordNotFoundException(Exception):
    pass

def main(arg = "Theme", arg2 = EMOTIONAL_FILE, jsFile=None):
    # Get letter / chapter paths
    letterspaths = glob.glob(FRANKENSTEIN_PATH + "*Letter*.txt")
    letterspaths.sort()
    chapterspaths = glob.glob(FRANKENSTEIN_PATH + "*Chapter*.txt")
    chapterspaths.sort()
    waltonpaths = glob.glob(FRANKENSTEIN_PATH + "*Walton*.txt")
    chapterspaths.sort()

    # put text of book in list 
    chaptersletters = []
    for k in letterspaths:
        chaptersletters.append(readfile(k))
    for k in chapterspaths:
        chaptersletters.append(readfile(k))
    for k in waltonpaths:
        chaptersletters.append(readfile(k))

    # Out list
    emotionalTxt = readfile(arg2)
    emotionalList = emotionalTxt.split("\n")

    # Example Usage
    # ====================
    # chaptersletters[0]   => Letter 1
    # chaptersletters[1]   => Letter 2
    # chaptersletters[n-1] => Letter n
    # ...
    # chaptersletters[4]   => Chapter 1
    # chaptersletters[5]   => Chapter 2
    # chaptersletters[n+3] => Chapter n
    # ...
    n = -1
    howmanywords = 0
    whenusedem = {}
    writefile(FRANKENSTEIN_PATH + "Score_" + arg + ".json", "[]")
    for k in chaptersletters:
        n += 1
        words = k.replace("'", "").replace(")", "").replace("(", "").replace("\"", "").replace("-", "").replace("_", "").replace(",", "").replace(".", "").replace("\n", " ").replace(";", "").replace("?", "").replace("—", "").replace("!", "").replace(":", "").split(" ")
        words = list(filter(None, words))

        # Do something with the words... 
        i = 0
        wordused = {}
        wordusedem = {}
        cou = 0
        while i < len(words)-1:
            w = words[i].lower()
            if w in wordused:
                wordused[w] += 1
            else:
                wordused[w] = 1
            # print(i, "/", len(words)-1)
            i += 1
            for e in emotionalList:
                ee = e.lower()
                for eee in [ee, ee + "ful", ee + "fully", ee + "ed", ee + "ing", ee + "edly", ee + "s", ee + "ly", ee + "ness", ee + "ate", ee + "ive", ee + "d"]:
                    if eee.lower() == w:
                        whenusedem[howmanywords] = w
                        cou += 1
                        if w in wordusedem:
                            wordusedem[w] += 1
                        else:
                            wordusedem[w] = 1
                        break
            howmanywords += 1
        out = ""
        if n > 3:
            out = "Chapter_" + str(n-3)
        elif n > 24:
            out = "Walton_" + str(n+1)
        else:
            out = "Letter_" + str(n+1)
        print(out)
        print (cou, "/", len(words), " => score: " + str(cou / len(words) * 100) + "%")
        a = json.loads(readfile(FRANKENSTEIN_PATH + "Score_" + arg + ".json"))
        writefile(FRANKENSTEIN_PATH + "Score_" + arg + ".json", json.dumps(a + [cou / len(words) * 100], indent=3))
        wordused = dict(sorted(wordused.items(), key=lambda item: item[1]))
        wordusedem = dict(sorted(wordusedem.items(), key=lambda item: item[1]))
        writefile(FRANKENSTEIN_PATH + "Word_Used_Count_" + out + ".json", json.dumps(wordused, indent=3))
        writefile(FRANKENSTEIN_PATH + "Word_Used_Wordlist_Count_" + out + ".json", json.dumps(wordusedem, indent=3))
    if jsFile != None:
        a = []
        try:
            a = json.loads(readfile(jsFile))
        except:
            pass
        fs = json.loads(readfile(FRANKENSTEIN_PATH + "Score_" + arg + ".json"))
        rgb = []
        while True:
            rgb = [255,1]
            rgb.append((random.randint(0, 2)*127 + 1)%256)
            random.shuffle(rgb)
            cont = False
            for ka in a:
                rgb2 = ka["borderColor"].replace("rgb(","").replace(")","").split(", ")
                lel = 0
                for i in range(len(rgb)):
                    if rgb[i] == int(rgb2[i]):
                        lel += 1
                if (rgb[1] == int(rgb2[1]) == 255) and rgb[0] != 255 and rgb[2] != 255:
                    cont = True
                if rgb[1] == 1 and rgb[0] == 255 and rgb[2] == 128:
                    cont = True
                if lel == 3:
                    cont = True
            if not cont:
                break
        a.append({
                "label": arg,
                # "backgroundColor": 'rgba(255, 99, 132, 0.05)',
                "backgroundColor": 'rgba(' + str(rgb[0])+ ', ' + str(rgb[1])+', ' + str(rgb[2])+', 0.05)',
                # "hoverBackgroundColor": 'rgba(255, 99, 132)',
                "borderColor": 'rgb(' + str(rgb[0] )+ ', ' + str(rgb[1])+', ' + str(rgb[2])+')',
                # "hoverBorderColor": 'rgb(255, 99, 132)',
                "data": fs
            })
        writefile(jsFile, json.dumps(a,indent=3))
    writefile(FRANKENSTEIN_PATH + "When_Used.json", json.dumps(whenusedem, indent=3))

class dictionary:
    def __init__(self, dict_path):
        self.words = {}
        self.locallist = []
        self.onlinelist = []
        self.dict_path = dict_path
        if not os.path.isfile(dict_path):
            a = open(dict_path, 'a')
            print("downloading dict.json ...")
            data = getwebcontent(DICTINARY_URL)
            a.write(data)
            a.close()
        self.loadfromfile()

    def loadfromfile(self):
        data = readfile(self.dict_path)
        self.words = json.loads(data)

    def save(self):
        data = json.dumps(self.words, indent=3)
        writefile(self.dict_path, data)

    def getword(self, wordString):
        wordString = wordString.lower()
        url = DICTINARY_API_JSON + wordString
        out = None
        if wordString in self.words:
            out = self.words[wordString]
        else:
            out = []
            try:
                web = getwebcontent(url)
                for k in json.loads(web)[0]["meanings"]:
                    out.append(k["partOfSpeech"])
            except request.HTTPError as e:
                if e.getcode() != 404:
                    raise CantAccessServerException("Can't access server")
            except Exception:
                pass
            self.words[wordString] = out
        if len(out) < 1:
            raise WordNotFoundException("Word not found")
        return out

def getwebcontent(url):
    bit = request.urlopen(url).read()
    return bit.decode(encoding='utf-8')

def writefile(filename, data):
    f = open(filename, "w")
    f.write(data)
    f.close()

def readfile(filename):
    f = open(filename, "r")
    out = f.read()
    f.close()
    return out

if __name__ == "__main__":
    arg = ""
    if len(sys.argv) > 3:
        arg = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
    main(arg, arg2, arg3)
