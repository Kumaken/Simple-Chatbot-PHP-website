#Import Regular Expression Module:
import re,random

#intent-expression dict:
intentStrategy = {
    "greet"     :   ( "(.*)halo(.*)",
                      "(.*)hi(.*)",
                      "(.*)hello(.*)" ),
    "farewell"  :   ( "(.*)bye(.*)",
                      "(.*)dada(.*)",
                      "(.*)selamat tinggal(.*)" )
}

replyStrategy = {
    "greet"     :   ( "halo juga cayank",
                      "i miss u so much my baybeh",
                      "halo-in diri lu sendiri sana" ),
    "farewell"  :   ( "dada cayanku",
                      "iiiih baru sebentar udah kangen nih",
                      "pergi lu jink" )
}

#regex func:
def regexMatch(message):
    for intent in intentStrategy.keys():
        for regex in intentStrategy[intent]:
            isMatch = re.match(regex, message)
            if isMatch:
                print("regex matches: ", isMatch.group())
                intentResult = intent
                return intentResult
    #not matched at all
    return None

def handleReply(intent):
    return random.choice(replyStrategy[intent])

#DRIVER:
message = ""
while(message != "exit"):
    message = input(">")
    print("RenitoBOT:", handleReply(regexMatch(message)) )
    

   
