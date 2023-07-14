from os import path, system, getenv
import cv2 as cv
import numpy as np
from time import sleep, time
import win32gui, win32con, win32ui
from win32api import SetCursorPos, GetCursorPos, GetAsyncKeyState
import pydirectinput as pd
import urllib3
import urllib.request
import requests
import json

pd.PAUSE = 0
urllib3.disable_warnings()


t = 0.18 #time your computer takes to run through algorithm


#get attack speed
def getAttackSpeed():
    request = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False).text
    data = json.loads(request)
    return data['championStats']['attackSpeed'], data['summonerName']


def getWindup():
    champs = ('Aatrox','Ahri','Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'Aurelion Sol', 'Azir', 'Bard', 'Bel\'Veth', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Cho\'Gath', 'Corki', 'Darius', 'Diana', 'Dr. Mundo', 'Draven', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'K\'Sante', 'Kai\'Sa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Kha\'Zix', 'Kindred', 'Kled', 'Kog\'Maw', 'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'Master Yi', 'Miss Fortune', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu & Willump', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'Rek\'Sai', 'Rell', 'Renata Glasc', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'Tahm  Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Vel\'Koz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Wukong', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra')
    champwindup = (20,21,14,14,31,24,21,20,16,22,21,16,19,25,28,19,24,18,20,20,22,11,21,21,17,16,17,19,16,19,31,14,21,21,17,19,15,26,1,20,26,21,22,20,24,23,18,21,10,16,17,20,17,37,17,35,16,16,20,19,21,21,18,18,17,17,20,23,15,19,16,19,16,25,20,31,25,15,22,15,19,20,31,22,16,23,21,20,24,18,22,20,24,21,16,18,18,23,27,43,19,18,21,17,23,21,16,19,32,19,22,23,18,20,24,25,13,19,18,19,15,17,19,26,17,13,19,22,14,15,21,20,25,21,20,16,18,18,20,21,16,23,17,19,20,31,18,21,18,26,19,23,23,21,16,24,20,16,21,19,17,15)
    sName = getAttackSpeed()[1]
    request = requests.get("https://127.0.0.1:2999/liveclientdata/playerlist", verify=False).text
    data = json.loads(request)
    
    for x in data:
        if x['summonerName'] == sName:
            ch = x['championName']

    return champwindup[champs.index(ch)]/100
    

#get delay between auto attacks
def getDelay(AS,windup):
    TIME = (1/AS)-t
    return TIME*windup, TIME*(1-windup)

#get screenshot
def screenshot():
    w = 1920
    h = 1080
    
    hwnd = win32gui.FindWindow(None, 'winnable')

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h,w,4)


    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    img = img[...,:3]
    img = np.array(img)
    return img

#find matches
def coords():
    image = screenshot()

    path = "image.jpg" #image to detect enemy

    coordinates = []

    #cc img
    enemy_img = cv.imread(path, cv.IMREAD_UNCHANGED)
    
    #do template matching
    result = cv.matchTemplate(image, enemy_img, cv.TM_CCORR_NORMED)

    #filter
    threshold = 0.95 #might have to change
    yloc, xloc = np.where(result >= threshold)

    #fill in coordinates
    for x,y in zip(xloc,yloc):
        coordinates.append([x,y])

    #return
    try:
        return sortedCoords(coordinates)
    except:
        return None

def sortedCoords(originalCoordinates):
    dist = []
    for enemy in originalCoordinates:
        dist += [abs(enemy[0] - 960) + abs(enemy[1] - 540)]

    #Get index of lowest distance
    if len(dist) > 0:
        clE = np.argmin(dist)
        clEC = [originalCoordinates[clE][0], originalCoordinates[clE][1]]
    return clEC



def checkIngame():
    try:
        request = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False).text
        return True
    except:
        return False


#logic
while True:
    ingame = checkIngame()
    while ingame:
        try:
            wu = getWindup()
            while ingame:
                ingame = checkIngame()
                while GetAsyncKeyState(0x20):
                    k = coords()
                    if k == None:
                        pd.keyDown('k') #bind k to player move click
                        pd.keyUp('k')
                    else:
                        try:
                            k = k[0]+60, k[1]+150
                            idk = getAttackSpeed()[0]
                            oPos = GetCursorPos()
                            SetCursorPos((k[0],k[1]))
                            pd.keyDown('l') #bind l to player attack move click
                            pd.keyUp('l')
                            sleep(0.05)
                            SetCursorPos(oPos)
                            sleep(getDelay(idk,wu)[0])
                            pd.keyDown('k')
                            pd.keyUp('k')
                            idk = getAttackSpeed()[0]
                            sleep(getDelay(idk,wu)[1])
                        except:
                            pass
        except:
            pass