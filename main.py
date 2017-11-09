#!/usr/bin/env python3

import sys, getopt, os, time, sqlite3, hashlib
from datetime import datetime
import json
from pprint import pprint
import xml.etree.ElementTree as etree
import urllib.request
import zipfile
import subprocess

def getScriptPath():
        return os.path.dirname(os.path.realpath(sys.argv[0]))

scriptPath = getScriptPath()

PATH_DATABASE = scriptPath + '/data/db.sqlite'
PATH_INDEXJAR = scriptPath + '/data/index.jar'
PATH_INDEXXML = scriptPath + '/data/index.xml'
PATH_APKDIR = scriptPath + '/apks/'
PATH_APKLISTTXT = scriptPath + "/apklist.txt"
PATH_WRAPPERSCRIPT = scriptPath + "/test_apks.sh"
URL_FDROID = "https://f-droid.org/repo/"

IS_TEST = False
TEST_APPLICATION_COUNT = 10

# def init_db(): # Usually does not need to be called anywhere
#   db = sqlite3.connect(PATH_DATABASE)
#   cursor = db.cursor()
#   cursor.execute('''
#       CREATE TABLE users(id INTEGER PRIMARY KEY, state TEXT, hour INTEGER, minute INTEGER)
#   ''')
#   db.commit()
#   db.close()

def insertIntoDB(xml_appl):
    appid = xml_appl.attrib.get("id")
    xml_appversions = xml_appl.findall("package")
    
    db = sqlite3.connect(PATH_DATABASE)
    cursor = db.cursor()
    
    for xml_appversion in xml_appversions:
        version = xml_appversion.findall("version")[0].text
        versioncode = xml_appversion.findall("versioncode")[0].text
        # print("*", version, versioncode)

        cursor.execute('''SELECT * FROM apps WHERE appid = ? AND versioncode = ?''', (appid, versioncode)); 
        sql_result = cursor.fetchall()
        # print(sql_result)
        if not sql_result: # List is empty
            # Entry does not exist in db yet, insert as new app
            added = ""
            lastupdated = ""
            name = ""
            summary = ""
            desc = ""
            license = ""
            categories = ""
            category = ""
            source = ""
            tracker = ""
            marketversion = ""
            marketvercode = ""
            antifeatures = ""
            apkname = ""
            srcname = ""
            hash = ""
            hashtype = ""
            size = ""
            sdkver = ""
            targetSdkVersion = ""
            added_version = ""
            sig = ""
            permissions = ""
            nativecode = ""
            result = ""

            timestamp = "1337" # TODO: Which Timestamp do we want to use?

            if xml_appl.findall("added"): added = xml_appl.findall("added")[0].text
            if xml_appl.findall("lastupdated"): lastupdated = xml_appl.findall("lastupdated")[0].text
            if xml_appl.findall("name"): name = xml_appl.findall("name")[0].text
            if xml_appl.findall("summary"): summary = xml_appl.findall("summary")[0].text
            if xml_appl.findall("desc"): desc = xml_appl.findall("desc")[0].text
            if xml_appl.findall("license"): license = xml_appl.findall("license")[0].text
            if xml_appl.findall("categories"): categories = xml_appl.findall("categories")[0].text
            if xml_appl.findall("category"): category = xml_appl.findall("category")[0].text
            if xml_appl.findall("source"): source = xml_appl.findall("source")[0].text
            if xml_appl.findall("tracker"): tracker = xml_appl.findall("tracker")[0].text
            if xml_appl.findall("marketversion"): marketversion = xml_appl.findall("marketversion")[0].text
            if xml_appl.findall("marketvercode"): marketvercode = xml_appl.findall("marketvercode")[0].text
            if xml_appl.findall("antifeatures"): antifeatures = xml_appl.findall("antifeatures")[0].text
            if xml_appversion.findall("apkname"): apkname = xml_appversion.findall("apkname")[0].text
            if xml_appversion.findall("srcname"): srcname = xml_appversion.findall("srcname")[0].text
            if xml_appversion.findall("hash"): hash = xml_appversion.findall("hash")[0].text
            if xml_appversion.findall("hash"): hashtype = xml_appversion.findall("hash")[0].attrib.get("type")
            if xml_appversion.findall("size"): size = xml_appversion.findall("size")[0].text
            if xml_appversion.findall("sdkver"): sdkver = xml_appversion.findall("sdkver")[0].text
            if xml_appversion.findall("targetSdkVersion"): targetSdkVersion = xml_appversion.findall("targetSdkVersion")[0].text
            if xml_appversion.findall("added"): added_version = xml_appversion.findall("added")[0].text
            if xml_appversion.findall("sig"): sig = xml_appversion.findall("sig")[0].text
            if xml_appversion.findall("permissions"): permissions = xml_appversion.findall("permissions")[0].text
            if xml_appversion.findall("nativecode"): nativecode = xml_appversion.findall("nativecode")[0].text
            result = "to-be-tested"

            print("Inserting", name, hash, hashtype)
            
            cursor.execute('''INSERT INTO apps(appid, versioncode, version, added, lastupdated, name, summary, desc, license, categories, category, source, tracker, marketversion, marketvercode, antifeatures, apkname, srcname, hash, hashtype, size, sdkver, targetSdkVersion, added_version, sig, permissions, nativecode)
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                              (appid, versioncode, version, added, lastupdated, name, summary, desc, license, categories, category, source, tracker, marketversion, marketvercode, antifeatures, apkname, srcname, hash, hashtype, size, sdkver, targetSdkVersion, added_version, sig, permissions, nativecode))
            cursor.execute('''INSERT INTO results(appid, versioncode, timestamp, result)
                              VALUES(?, ?, ?, ?)''', 
                              (appid, versioncode, timestamp, result))
            
    db.commit()
    db.close()

def createDatabase():
    if os.path.isfile(PATH_DATABASE):
        print("Database file seems to already exist in", PATH_DATABASE)
        return

    db = sqlite3.connect(PATH_DATABASE)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE "apps" (`appid` TEXT,`version` TEXT,`added` TEXT,
`lastupdated` TEXT,`name` TEXT,`summary` TEXT,`desc` TEXT,`license` TEXT,`categories` TEXT,
`category` TEXT,`source` TEXT,`tracker` TEXT,`marketversion` TEXT,`marketvercode` TEXT,
`antifeatures` TEXT,`versioncode` INTEGER,`apkname` TEXT,`srcname` TEXT,`hash` TEXT,
`hashtype` TEXT,`size` INTEGER,`sdkver` INTEGER,`targetSdkVersion` INTEGER,`added_version` INTEGER,
`sig` TEXT,`permissions` TEXT,`nativecode` TEXT, `available` TEXT, PRIMARY KEY(appid,versioncode))''');
    cursor.execute('''CREATE TABLE "results" (`resultsid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
`appid` TEXT, `versioncode` INTEGER, `timestamp` TEXT, `result` TEXT)''')
    db.commit()
    db.close()

# This method takes the XML and updates the database with new apps
def updateDatabase():
    tree = etree.parse(PATH_INDEXXML)
    root = tree.getroot()
    for application in root.findall("application"):
        print(application.attrib)
        insertIntoDB(application)

def pullIndexXML():
    print("Downloading index.jar ...")
    url = URL_FDROID + "index.jar"
    urllib.request.urlretrieve(url, PATH_INDEXJAR)
    with zipfile.ZipFile(PATH_INDEXJAR, 'r') as zf:
        zf.extract('index.xml', "data/")
    if IS_TEST:
        t = TEST_APPLICATION_COUNT
        print("Selecting first", t, "applications.")
        tree = etree.parse(PATH_INDEXXML)
        root = tree.getroot()
        for application in root.findall("application"):
            t -= 1
            if t < 0:
                root.remove(application)
        tree.write(PATH_INDEXXML)

def getTableFromDB(table = "apks"):
    db = sqlite3.connect(PATH_DATABASE)
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM apps'''); 
    apks = cursor.fetchall()
    db.commit()
    db.close()
    return apks;

def setAvailableValueInDB(appid, versioncode, value):
    db = sqlite3.connect(PATH_DATABASE)
    cursor = db.cursor()
    cursor.execute('''UPDATE apps SET available = ?
                      WHERE appid = ? AND versioncode = ?''', (value, appid, versioncode))
    db.commit()
    db.close()

# Downloads an APK
# Returns True if successful, False otherwise
def downloadAPK(url, targetDir, appid, versioncode):
    try:
        urllib.request.urlretrieve(url, targetDir)
        return True
    except urllib.error.HTTPError as e:
        print(e)
        if e.code == 404:
            setAvailableValueInDB(appid, versioncode, "no")
            return False

def downloadAPKs():
    print("Downloading apks ...")
    apks = getTableFromDB("apks")

    for apk in apks:
        appid = apk[0]
        versioncode = apk[1]
        apkName = apk[16]
        available = apk[27]
        apkDirFull = PATH_APKDIR + apkName
        hash_DB = apk[18]

        if not os.path.isfile(apkDirFull) and available != "no":
            print("Need to download " + apkName)
            url = URL_FDROID + apkName
            if not downloadAPK(url, apkDirFull, appid, versioncode): continue
            setAvailableValueInDB(appid, versioncode, "yes")

        if sha256_checksum(apkDirFull) != hash_DB:
            print("Hashes for", apkDirFull, "do not match! Retrying ...", hash_calc, hash_DB)
            downloadAPK(url, apkDirFull, appid, versioncode)
            if sha256_checksum(apkDirFull) != hash_DB:
                print("Hashes still do not match, skipping this app!")
                setAvailableValueInDB(appid, versioncode, "no")
                os.remove(apkDirFull)

def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def prepareFuzzing():
    with open(PATH_APKLISTTXT, "w") as f:
        f.write("")
    
    apkList = getListToTest()
    for apk in apkList:
        apkPath = PATH_APKDIR + apk[0]
        print(apkPath)
        with open(PATH_APKLISTTXT, "a") as f:
            f.write(apkPath + "\n")

def getListToTest():
    db = sqlite3.connect(PATH_DATABASE)
    cursor = db.cursor()
    cursor.execute('''SELECT apps.apkname FROM apps LEFT JOIN results ON apps.appid = results.appid AND apps.versioncode = results.versioncode WHERE results.result IS NULL OR results.result = "to-be-tested";''')
    apkList = cursor.fetchall()
    db.commit()
    db.close()
    return apkList

def callWrapperScript():
    subprocess.call([PATH_WRAPPERSCRIPT])

def printHelp():
    print("-t | --test      Use a test environment")
    print("-h | --help      You are looking at it")

def silentremove(filename):
    try:
        os.remove(filename)
    except FileNotFoundError as e:
        pass

def setupTestEnvironment():
    print("Using test environment.")
    global IS_TEST
    IS_TEST = True
    silentremove(PATH_DATABASE)
    silentremove(PATH_INDEXJAR)
    silentremove(PATH_INDEXXML)

def main(argv):
    try:
          opts, args = getopt.getopt(argv,"ht",["help","test"])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printHelp()
            sys.exit()
        elif opt in ("-t", "--test"):
            setupTestEnvironment()
    # elif opt in ("-o", "--ofile"):
    #   outputfile = arg

    pullIndexXML()
    createDatabase()
    updateDatabase()
    downloadAPKs()
    prepareFuzzing()
    # callWrapperScript()
    # TODO: Move apks into a to-test directory (?)
    # TODO: Call worker script to test apks
    # TODO: ...

if __name__ == '__main__':
    main(sys.argv[1:])
