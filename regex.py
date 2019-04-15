#Import Regular Expression Module:
import re,random
#Import noSQL database module:
import pymongo
#Import python web framework:
from flask import Flask
from flask_restful import Api, Resource, reqparse
#other dependencies : dnspython, gunicorn

#setup mongodb:
myclient =pymongo.MongoClient("mongodb+srv://randomguy:test123@vueexpress-miieb.mongodb.net/test?retryWrites=true")
test = myclient.test

nlpData = myclient["NLPStrategy"] #create database
#create collection:
intentStrategyDB = nlpData["intentStrategy"] #intent-expression dict:
replyStrategyDB = nlpData["replyStrategy"] #intent-reply dict:

#initial insert:
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
"""for entry in intentStrategyCursor:
    print(entry)"""
#print (objMongo)
#intentStrategy = [obj.to_mongo() for obj in objMongo]
#print(intentStrategy)
#regex func:

def regexMatch(message):
    for intent in intentStrategyCursor:
        # DEBUGGER: print("test1:" ,intent)
        for regex in intent["regexes"]:
            # DEBUGGER: print("test:" ,regex)
            isMatch = re.match(regex, message)
            if isMatch:
                # DEBUGGER: print("regex matches: ", isMatch.group())
                intentStrategyCursor.rewind()
                return intent["intent"]
        #reset cursor:
    #not matched at all
    intentStrategyCursor.rewind()
    return None

def handleReply(_intent):
    try:
        # DEBUGGER: print("intent is : ",_intent)
        replyDict = replyStrategyDB.find_one({"intent" : _intent})
        return random.choice(replyDict["replies"])
    except:
        teachNLP()
        return "OK. Lanjuts"
    
def teachNLP():
    print("RenitoBOT: Aku gak ngerti lho, kamu mau ngomong apa cayank...")
    proceed = input("RenitoBOT: Ajarin boleh? (y/n) :")
    if proceed.lower() == "y":
        newIntent = input("RenitoBOT: kamu tuh sebenarnya ngomong tentang apa? (intent) :")
        newIntent = newIntent.lower()
        print("RenitoBOT: trus kata kunci-nya apa saja? aku gak bisa mikir nih! (input stops when empty string is received) (regexes)")
        newRegexes = []
        temp = "x"
        while(temp!= ""):
            temp = input()
            if temp != "":
                newRegexes.append("(.*)"+temp.lower()+"(.*)")
        newReplies = []
        print("RenitoBOT: trus kamu mau direply apa saja? (input stops when empty string is received) (reply)")
        temp = "x"
        while(temp!= ""):
            temp = input()
            if temp != "":
                newReplies.append(temp)
        print("RenitoBOT: Ok thank you udah ngajarin aku cayank, sebentar ya aku masukin ke dengkul dlu")
        if (intentStrategyDB.find_one({"intent" : newIntent}) != None):
            print("RenitoBOT: Eh udah ada ternyata, add to my kamus!")
            intentStrategyDB.update_one({'intent': newIntent}, {'$pushAll': {'regexes': newRegexes}})
            replyStrategyDB.update_one({'intent': newIntent}, {'$pushAll': {'replies': newReplies}})
        else:
            print("RenitoBOT: Adding new kamus!")
            intentStrategyDB.insert_one({
                "intent"    :   newIntent,
                "regexes"   :   newRegexes
            })
            replyStrategyDB.insert_one({
                "intent"    :   newIntent,
                "replies"   :   newReplies
            })
        print("RenitoBOT: ok cayank, makasih yaaa :3")
    else:
        print("RenitoBOT: Dasar anak bego gak tau diri")


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
        print("RenitoBOT:", handleReply(regexMatch(message)) )
        

#RUN MAIN PROGRAM:
main()
"""

#setup API:
app = Flask(__name__)
api = Api(app)

class backEnd(Resource):
    def get(self, userInput):
        try:
            return handleReply(regexMatch(userInput)), 200
        except:
            return "ERROR!", 404

api.add_resource(backEnd, "/api/<string:userInput>")
if __name__ == "__main__":
    app.run(debug=False)
#if __name__ == "__main__":
#   app.run()
