import re,random
#Import noSQL database module:
import pymongo
#Import python web framework:
from flask import Flask,request
from flask_restful import Api, Resource, reqparse
#Import catch stdout:
from io import StringIO
import sys
#other dependencies : dnspython, gunicorn

#setup mongodb:
myclient =pymongo.MongoClient("mongodb+srv://randomguy:test123@vueexpress-miieb.mongodb.net/test?retryWrites=true")
test = myclient.test

nlpData = myclient["NLPStrategy"] #create database
#create collection:
intentStrategyDB = nlpData["intentStrategy"] #intent-expression dict:
intentStrategyDB2 = nlpData["intentStrategy2"] #intent-expression for KMP&BM dict:
replyStrategyDB = nlpData["replyStrategy"] #intent-reply dict:

intentStrategy2IN1 = {
    "intent"    :   "greet",
    "regexes"   :   ( "halo, siapa namamu?",
                      "kamu siapa?",
                      "selamat pagi" )
}
intentStrategyDB2.insert_one(intentStrategy2IN1)