import requests

#URL:
# localhost:
#url = "http://127.0.0.1:5000/"
# server:
url = "https://python-nlp-chatbot.herokuapp.com/"

def teachNLP():
    global url
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
        if (requests.get(url+"query/"+newIntent).text == "true\n"):
            print("RenitoBOT: Eh udah ada ternyata, add to my kamus!")
            newData = {
                "newRegexes": newRegexes, 
                "newReplies": newReplies
            }
            requests.put(url+"api/"+newIntent, json=newData)
        else:
            print("RenitoBOT: Adding new kamus!")
            newIntentStrategy = {
                "intent"    :   newIntent,
                "regexes"   :   newRegexes
            }
            newReplyStrategy = {
                "intent"    :   newIntent,
                "replies"   :   newReplies
            }
            newData = [newIntentStrategy, newReplyStrategy]
            print(requests.post(url+"api/intentStrategy", json=newIntentStrategy))
            print(requests.post(url+"api/replyStrategy", json=newReplyStrategy))
        print("RenitoBOT: ok cayank, makasih yaaa :3")
    else:
        print("RenitoBOT: Dasar anak bego gak tau diri")

def viewDatabase():
    return requests.get(url+"view").text
def deleteEntry(intent):
    return requests.delete(url+"query/"+intent)

def main():
    message = ""
    while(message != "exit"):
        message = input(">")
        #localhost debug:
        try:
            if message == "view database":
                print(viewDatabase())
            elif message == "delete entry":
                tempIntent = input("target intent: ")
                print(deleteEntry(tempIntent))
            else:
                respond = requests.get(url+"api/"+message).text
                if respond == "\"ERROR!\"\n":
                    raise Exception("Input not Understood")
                print("RenitoBOT:",respond )
        except:
            teachNLP()
            
        #respond = requests.get("https://python-nlp-chatbot.herokuapp.com/api/"+message).text
        

main()