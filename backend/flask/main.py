# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request, render_template
  

from pydantic import BaseModel
from ast import literal_eval
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


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

        embeddings = OpenAIEmbeddings(openai.api_key)
        print(str(ticker))
        new_db = FAISS.load_local(str(ticker), embeddings)
        ar = literal_eval(vector)
        docs_and_scores = new_db.similarity_search_by_vector(ar)
        size = len(docs_and_scores)
        data = ""
        for i in range(0,size):
            data+=(docs_and_scores[i].page_content + "\n\n")


        print(data)


        return jsonify({'data': data})

def relatedwords(ticker, vembeddings):
    
    embeddings = OpenAIEmbeddings()
    print(str(ticker))
    new_db = FAISS.load_local(ticker, embeddings)
        # ar = literal_eval(vector)
    docs_and_scores = new_db.similarity_search_by_vector(vembeddings)
    size = len(docs_and_scores)
    data = ""
    for i in range(0,size):
        data+=(docs_and_scores[i].page_content + "\n\n")


    print(data)


    return data
  

def completion(context):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0,
    messages=[
        {
          "role": "system",
          "content": "You are a financial assistant that VERY ACCURATELY and CONCISELY answers queries using publicly filled annual reports of publicly traded companies. Use the CONTEXT provided to form your answer. Keep your answer under 5 sentences. Be accurate, helpful, concise, and clear, while performing accurate mathematical calculations."
        },
        {
          "role": "user",
          "content": context
        }
    ]
    )

    return (completion.choices[0].message["content"])



def embeddingsgenerate(embeddingsof):
    
    embeddings = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=embeddingsof
    )
    return embeddings["data"][0]["embedding"]


@app.route('/generate_embeddings', methods= ['GET', 'POST'])
def get_embeddings():
    if(request.method == 'GET'):
  
        data = "its up"
        return jsonify({'data': data})
    if(request.method == 'POST'):
        data = request.get_json()
        texts = data['texts']
        embeddings = openai.Encodings.create(texts)
        return jsonify({'embeddings': embeddings})



@app.route('/<path_name>',methods=['GET', 'POST'])
def answer_question(path_name):

    urlforprice = ("https://s.tradingview.com/embed-widget/symbol-info/?locale=en&colorTheme=dark&symbol=BSE:"+path_name)
    if request.method == 'POST':
        # User submitted a question, so process it and get an answer from OpenAI
        question = request.form['question']
        # openai_api_key = request.form['openai_api_key']
        prompt = f"{question}"

        embeddings_recieved = embeddingsgenerate(question)

        context = relatedwords(path_name, embeddings_recieved)

        questionforgpt = "CONTEXT\n\n" + context + "\nQUESTION\n" + prompt

        answerfromgpt = completion(questionforgpt)
        print(answerfromgpt)
        
        return render_template('chat.html', path_name=path_name, questionasked=prompt, urlforprice=urlforprice, embeddings_recieved = context, answer_received = answerfromgpt)

    else:
        answer = "not yet used"
        # Render the answer on an HTML template
        return render_template('chat.html', path_name=path_name, answer=answer,urlforprice=urlforprice)
  

@app.route('/',methods=['GET'])
def homepage():
    return render_template('home.html')


# driver function
if __name__ == '__main__':
  
    app.run(debug = True)


