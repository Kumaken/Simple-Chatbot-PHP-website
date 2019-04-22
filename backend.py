#Import Regular Expression Module:
import re,random
#Import noSQL database module:
import pymongo
#Import python web framework:
from flask import Flask,request
from flask_restful import Api, Resource, reqparse
#Import catch stdout:
from io import StringIO
#urllib2: for url sentences:
from urllib.parse import unquote

import sys
#other dependencies : dnspython, gunicorn

#algorithm inclueds:
#BOYERMORE:
from BoyerMoore import BoyerMooreMatching,BuildLast
from kmp import kmpcall

#setup mongodb:
myclient =pymongo.MongoClient("mongodb+srv://randomguy:test123@vueexpress-miieb.mongodb.net/test?retryWrites=true")
test = myclient.test

nlpData = myclient["NLPStrategy"] #create database
#create collection:
intentStrategyDB = nlpData["intentStrategy"] #intent-expression dict:
intentStrategyDB2 = nlpData["intentStrategy2"] #intent-expression for KMP&BM dict:
replyStrategyDB = nlpData["replyStrategy"] #intent-reply dict:

#initial insert:
"""
intentStrategyIN1 = {
    "intent"    :   "greet",
    "regexes"   :   ( "(.*)halo(.*)",
                      "(.*)hi(.*)",
                      "(.*)hello(.*)" )
}

intentStrategyIN2 = {
    "intent"    :   "farewell",
    "regexes"  :   ( "(.*)bye(.*)",
                      "(.*)dada(.*)",
                      "(.*)selamat tinggal(.*)" )
}

replyStrategyIN1 = {
    "intent"    :   "greet",
    "replies"     :   ( "halo juga cayank",
                      "i miss u so much my baybeh",
                      "halo-in diri lu sendiri sana" )
}

replyStrategyIN2 = {
    "intent"   :   "farewell",
    "replies"  :   ( "dada cayanku",
                      "iiiih baru sebentar udah kangen nih",
                      "pergi lu jink" )
}
"""
#intentStrategyDB.delete_many({})
#replyStrategyDB.delete_many({})
#intentStrategyDB.delete_one({"intent" : "insult"})
#replyStrategyDB.delete_one({"intent" : "insult"})
#intentStrategyDB.insert_one(intentStrategyIN1)
#intentStrategyDB.insert_one(intentStrategyIN2)
#replyStrategyDB.insert_one(replyStrategyIN1)
#replyStrategyDB.insert_one(replyStrategyIN2)

#get the database:
intentStrategyCursor = intentStrategyDB.find() #points to first entry
intentStrategyCursor2 = intentStrategyDB2.find() #points to first entry
"""for entry in intentStrategyCursor:
    print(entry)"""
#print (objMongo)
#intentStrategy = [obj.to_mongo() for obj in objMongo]
#print(intentStrategy)
#regex func:

threshold = 0.9
def stringMatch(message, algoType):
    message = message.replace("%20"," ")
    print("MESSAGE GOTTEN:",message)
    if(algoType == "regex"):
        for intent in intentStrategyCursor:
            # DEBUGGER: print("test1:" ,intent)
            for regex in intent["regexes"]:
                # DEBUGGER: print("test:" ,regex)
                isMatch = re.match(regex, message)
                if isMatch:
                    # DEBUGGER: print("regex matches: ", isMatch.group())
                    intentStrategyCursor.rewind()
                    return intent["intent"]
        intentStrategyCursor.rewind()
    elif(algoType == "bm" or algoType == "kmp"):
        max = [-999,"nullintent"]
        for intent in intentStrategyCursor2:
            # DEBUGGER: print("test1:" ,intent)
            for pattern in intent["patterns"]:
                print("intent:", intent, "test:" ,pattern)
                if(algoType == "bm"):
                    temp = BoyerMooreMatching(message, pattern)
                elif (algoType == "kmp"):
                    temp = kmpcall(message, pattern)
                if temp > max[0]:
                    print( temp , " >< ", max[0])
                    #switch intent & percentage of likeliness:
                    max[0] = temp
                    max[1] = intent["intent"]
        #reset cursor:
        intentStrategyCursor2.rewind()
        #return result:
        if max[0]> 0.9:
            return max[1]
    
    #not matched at all
    return None

def handleReply(_intent):
    # DEBUGGER: print("intent is : ",_intent)
    replyDict = replyStrategyDB.find_one({"intent" : _intent})
    return random.choice(replyDict["replies"])


#DRIVER:
"""
def main():
    message = ""
    while(message != "exit"):
        #app.run(debug=True)
        
        #for entry in intentStrategyCursor:
            #print(entry) 
        #intentStrategyCursor.rewind()
        message = input(">")
        print("RenitoBOT:", handleReply(stringMatch(message)) )
        

#RUN MAIN PROGRAM:
main()
"""

#setup API:
app = Flask(__name__) #encapsulation IS NECESSARY
api = Api(app)

class backEnd(Resource):
    def get(self, userInput, algoType):
        """
        try:
            
        except:
            return "ERROR!", 404"""
    
        return handleReply(stringMatch(userInput, algoType)), 200

    def post(self, userInput, algoType):
        #try:
        data = request.get_json()
        print(data)
        if userInput == "intentStrategy":
            print("inserted intent")
            intentStrategyDB.insert_one(data)
        elif userInput == "intentStrategy2":
            intentStrategyDB2.insert_one(data)
        else: #replyStrategy
            print("inserted reply")
            if replyStrategyDB.find_one({"intent" : data["intent"]}) != None:
                for reply in data["replies"]:
                    replyStrategyDB.update_one({'intent': data["intent"]}, {'$push': {'replies': reply }}, upsert=True)
            else:
                replyStrategyDB.insert_one(data)
            
        return "POST success", 200
        #except:
        #return "eh?!", 404
    
    def put(self, userInput, algoType):
        #try:
        if algoType == "regex":
            newRegexes = request.json["newRegexes"]
            for regex in newRegexes:
                intentStrategyDB.update_one({'intent': userInput}, {'$push': {'regexes': regex }}, upsert=True)
            newReplies = request.json["newReplies"]
            for reply in newReplies:
                replyStrategyDB.update_one({'intent': userInput}, {'$push': {'replies': reply }}, upsert=True)
        else:
            newPatterns = request.json["newPatterns"]
            for pattern in newPatterns:
                intentStrategyDB2.update_one({'intent': userInput}, {'$push': {'patterns': pattern }}, upsert=True)
            newReplies = request.json["newReplies"]
            for reply in newReplies:
                replyStrategyDB.update_one({'intent': userInput}, {'$push': {'replies': reply }}, upsert=True)
            """except:
            return "eh?!", 404"""


class queryDatabase(Resource):
    def get(self, userInput):
        try:
            found = intentStrategyDB.find_one({"intent" : userInput}) != None
            return found, 200
        except:
            return "ERROR!", 404

    def delete(self, userInput):
        try:
            intentStrategyDB.delete_one({"intent" : userInput})
            replyStrategyDB.delete_one({"intent" : userInput})
            return "DONE", 200
        except:
            return "ERROR!", 404

class viewDatabase(Resource):
    def get(self):
        #old_stdout = sys.stdout
        #sys.stdout = mystdout = StringIO() #capture stdout to mystdout
        cur1 = intentStrategyDB.find()
        for entry in cur1:
            print(entry)
            print()
        print("\n-------------------------------------\n") 
        cur2 = replyStrategyDB.find()
        for entry in cur2:
            print(entry)
            print()
        print("\n-------------------------------------\n") 
        cur3 = intentStrategyDB2.find()
        for entry in cur3:
            print(entry)
            print()
        #sys.stdout = old_stdout #restore stdout
        #return mystdout.getvalue(), 200
        return "DONE", 200

api.add_resource(backEnd, "/api/<string:algoType>/<string:userInput>")
api.add_resource(queryDatabase, "/query/<string:userInput>")
api.add_resource(viewDatabase, "/view")
# LOCALHOST:    
#app.run(debug=True)
#LESSON : if __name __ == "__main__" IS MANDATORY or else you will get address already used error on heroku (cause already run on gunicorn)
# test url unquoting:
# print( unquote("/api/regex/crush%20you"))
if __name__ == "__main__":
    app.run(debug=False) 

