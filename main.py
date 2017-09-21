import sys
import os
import time
import sqlite3
from datetime import datetime
import json
from pprint import pprint
import xml.etree.ElementTree as etree
import urllib.request
import zipfile

def getScriptPath():
        return os.path.dirname(os.path.realpath(sys.argv[0]))

scriptPath = getScriptPath()

PATH_DATABASE = scriptPath + '/data/db.sqlite'
PATH_INDEXJAR = scriptPath + '/data/index.jar'
PATH_INDEXXML = scriptPath + '/data/index.xml'
PATH_APKDIR = scriptPath + '/apks/'
URL_FDROID = "https://f-droid.org/repo/"

# def init_db(): # Usually does not need to be called anywhere
# 	db = sqlite3.connect(PATH_DATABASE)
# 	cursor = db.cursor()
# 	cursor.execute('''
# 		CREATE TABLE users(id INTEGER PRIMARY KEY, state TEXT, hour INTEGER, minute INTEGER)
# 	''')
# 	db.commit()
# 	db.close()

def insertIntoDB(xml_appl):
	appid = xml_appl.attrib.get("id")
	xml_appversions = xml_appl.findall("package")
	
	db = sqlite3.connect(scriptPath + '/data/db.sqlite')
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



# This method takes the XML and updates the database with new apps
def updateDatabase():
	tree = etree.parse(PATH_INDEXXML)
	root = tree.getroot()
	for i in range(len(root)):
		print(root[i].attrib, len(root[i]))
		insertIntoDB(root[i])

def pullIndexXML():
	print("Downloading index.jar …")
	url = "https://f-droid.org/repo/index.jar"
	# urllib.request.urlretrieve(url, PATH_INDEXJAR)
	with zipfile.ZipFile(PATH_INDEXJAR, 'r') as zf:
	    zf.extract('index.xml', "data/")

def getTableFromDB(table = "apks"):
	db = sqlite3.connect(scriptPath + '/data/db.sqlite')
	cursor = db.cursor()
	cursor.execute('''SELECT * FROM apps'''); 
	apks = cursor.fetchall()
	db.commit()
	db.close()
	return apks;

def setValueInDB(appid, versioncode, key, value):
	db = sqlite3.connect(scriptPath + '/data/db.sqlite')
	cursor = db.cursor()
	cursor.execute('''UPDATE apps SET ? = ?
		              WHERE appid = ? AND versioncode = ?''', (key, value, appid, versioncode))
	db.commit()
	db.close()

def downloadAPKs():
	print("Downloading apks …")
	apks = getTableFromDB("apks")
	for apk in apks:
		appid = apk[0]
		versioncode = apk[1]
		apkName = apk[16]
		available = apk[27]
		apkDirFull = PATH_APKDIR + apkName
		if not os.path.isfile(apkDirFull) and available is not "no":
			print("Need to download " + apkName)
			url = "https://f-droid.org/repo/" + apkName
			try:
				urllib.request.urlretrieve(url, apkDirFull)
			except urllib.error.HTTPError as e:
				print(e)
				if e.code == 404:
					setValueInDB(appid, versioncode, "available", "no")
					continue
			setValueInDB(appid, versioncode, "available", "yes")

def main():
	pullIndexXML()
	updateDatabase()
	downloadAPKs()
	# TODO: Move apks into a to-test directory (?)
	# TODO: Call worker script to test apks
	# TODO: ...

if __name__ == '__main__':
	main()