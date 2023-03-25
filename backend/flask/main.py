# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
  

from fastapi import FastAPI
from pydantic import BaseModel
from ast import literal_eval
import os

import langchain
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings



# creating a Flask app
app = Flask(__name__)
  
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/related', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "its up"
        return jsonify({'data': data})
    if(request.method == 'POST'):
  

        temp= request.get_json()
        print(temp)
        vector = temp["ve"]
        ticker = temp["ticker"]

        embeddings = OpenAIEmbeddings(openai_api_key="sk-asafdoesntreallymatteryft652174u1y")
        new_db = FAISS.load_local(str(ticker), embeddings)
        ar = literal_eval(vector)
        docs_and_scores = new_db.similarity_search_by_vector(ar)
        size = len(docs_and_scores)
        data = ""
        for i in range(0,size):
            data+=(docs_and_scores[i].page_content + "\n\n")


        print(data)


        return jsonify({'data': data})
  
  
  
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)