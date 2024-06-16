import sqlite3
import time
import numpy as np
import random

sqliteConnection = sqlite3.connect('pre.db')
cursor = sqliteConnection.cursor()


def createDataBase():
    # SQL create a table in the database
    sql_command = """CREATE TABLE decisions ( 
    lineHA INTEGER,
    lineHB INTEGER,
    lineHC INTEGER,
    lineHD INTEGER,
    lineVA INTEGER,
    lineVB INTEGER,
    lineVC INTEGER,
    lineVD INTEGER,
    modelSelected INTEGER, 
    date INTEGER);"""

    cursor.execute(sql_command)


def insertDecision(listPoints, model):
    valuesString = False
    now = time.strftime("%Y%m%d_%H%M%S")
    for l in listPoints:
        if valuesString:
            valuesString = f"{valuesString}, '{l}'"
        else:
            valuesString = f"'{l}'"
    try:
        cursor.execute(
            f"INSERT INTO listasBorrar VALUES ('{valuesString}', '{now}', {model})")
    except:
        print('Error inserting values in DB.')
    sqliteConnection.commit()


def getDecision(listPoints):
    models = {'heart': ['01a', '01b', '01c'], 'ellipse': ['02a', '02b', '02c'], 'rectangle': ['03a', '03b', '03c'], 'square': [
        '04a', '04b', '04c'], 'circle': ['05a', '05b', '05c'], 'rhomb': ['06a', '06b', '06c'], }
    modelsItems = ['heart', 'ellipse',
                   'rectangle', 'square', 'circle', 'rhomb']
    mainDecision = getMainDecision(listPoints)
    indexMain = modelsItems.index(mainDecision)
    indexItemElse = random.randint(0, 5)
    while indexMain == indexItemElse:
        indexItemElse = random.randint(0, 5)
    indexElementElse = random.randint(0, 2)
    otherElement = models[modelsItems[indexItemElse]][indexElementElse]
    result = models[mainDecision]
    result.append(otherElement)
    return result


def getMainDecision(listPoints):
    if listPoints['pTop'].y > listPoints['pAr'].y:
        print('Model heart')
        return 'heart'
    else:
        longCross = False
        horizM, horizA, horizB, horizC, horizD, vertMain, vertL, vertR = getRatios(
            listPoints)
        diferenceCross = abs(vertMain - horizM)
        if diferenceCross < 0.2:
            longCross = True
        diferenceH_AM = abs(horizA - horizM)
        if diferenceH_AM < 0.1:
            mediumHoriz = (horizA + horizM) / 2.0
            diference_VH = abs(horizM - vertMain)
            if diference_VH < 0.2:
                print('Model square')
                return 'square'
            else:
                print('Model rectangle')
                return 'rectangle'
        else:
            if longCross:
                pointA = pointOnLine(
                    listPoints['pTop'], listPoints['pMr'], listPoints['pAr'])
                pointB = pointOnLine(
                    listPoints['pTop'], listPoints['pMr'], listPoints['pBr'])
                if pointA and pointB:
                    print('Model rhomb')
                    return 'rhomb'
                else:
                    print('Model ellipse')
                    return 'ellipse'
            else:
                print('Model circle')
                return 'circle'


def pointOnLine(vectorA, vectorB, point):
    # Ecuación línea  (x-x1)/(y-y1)=(x2-x1)/(y2-y1)
    # (x-x1)=(x2-x1)(y-y1)/(y2-y1)
    # x=((x2-x1)(y-y1)/(y2-y1))+x1
    x = ((vectorB.x-vectorA.x)(point.y-vectorA.y)/(vectorB.y-vectorA.y))+vectorA.x
    diferenceX = abs(point.x - x)
    if diferenceX < 0.1:
        return True
    else:
        return False


def getRatios(marks):
    print(marks)
    pTop = np.array([marks['pTop'].x, marks['pTop'].y, marks['pTop'].z])
    pDown = np.array([marks['pDown'].x, marks['pDown'].y, marks['pDown'].z])
    pMr = np.array([marks['pMr'].x, marks['pMr'].y, marks['pMr'].z])
    pMl = np.array([marks['pMl'].x, marks['pMl'].y, marks['pMl'].z])
    pAr = np.array([marks['pAr'].x, marks['pAr'].y, marks['pAr'].z])
    pAl = np.array([marks['pAl'].x, marks['pAl'].y, marks['pAl'].z])
    pBr = np.array([marks['pBr'].x, marks['pBr'].y, marks['pBr'].z])
    pBl = np.array([marks['pBl'].x, marks['pBl'].y, marks['pBl'].z])
    pCr = np.array([marks['pCr'].x, marks['pCr'].y, marks['pCr'].z])
    pCl = np.array([marks['pCl'].x, marks['pCl'].y, marks['pCl'].z])
    pDr = np.array([marks['pDr'].x, marks['pDr'].y, marks['pDr'].z])
    pDl = np.array([marks['pDl'].x, marks['pDl'].y, marks['pDl'].z])
    #vA = np.array([marks[0].x, marks[0].y, marks[0].z,marks[4].x, marks[4].y, marks[4].z])
    #magA = math.sqrt(sum(pow(element, 2) for element in vA))
    horizM = np.linalg.norm(pMr - pMl)
    horizA = np.linalg.norm(pAr - pAl)
    horizB = np.linalg.norm(pBr - pBl)
    horizC = np.linalg.norm(pCr - pCl)
    horizD = np.linalg.norm(pDr - pDl)
    vertMain = np.linalg.norm(pTop - pDown)
    vertL = np.linalg.norm(pCr - pCl)
    vertR = np.linalg.norm(pAr - pCr)
    #magB = math.sqrt(sum(pow(element, 2) for element in vB))
    #magC = math.sqrt(sum(pow(element, 2) for element in vC))
    #magD = math.sqrt(sum(pow(element, 2) for element in vD))
    resultA = np.inner(pTop, pDown)
    resultB = np.inner(pBr, pBl)
    resultC = np.inner(pCr, pCl)
    #print(resultA, resultB, resultC, resultD)
    print(horizA, horizB, horizC, horizD)
    print(vertMain, vertL, vertR)
    return horizM, horizA, horizB, horizC, horizD, vertMain, vertL, vertR


# createDataBase()
# close the connection
sqliteConnection.close()
