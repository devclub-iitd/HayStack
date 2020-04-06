from elasticsearch import Elasticsearch
from flask import Flask, request, redirect, render_template, url_for
from .config import Config
from .forms import SearchForm


es = Elasticsearch([{'port':'localhost', 'port':9200}])
app = Flask(__name__)
app.config.from_object(Config)

def search(query):
    results = es.search(index='webpages', doc_type='_doc', body={
        'size':10,
        'query':{
            'match':{'content':query
                }
            },
        'highlight':{
            'order':'score',
            'number_of_fragments':3,
            'fields':{
                'content':{}
                }
            }
        })['hits']['hits']

    filtered = []
    for res in results:
        filtered.append({
            'title':res['_source']['title'],
            'url': res['_source']['url'], 
            'highlight': '...'.join(res['highlight']['content'])
            })

    return filtered

@app.route('/', methods=['GET', 'POST'])
def magnet():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('needles', query=form.query.data))
    return render_template('base.html', title='HayStack', form=form)

@app.route('/needles')
def needles():
    query = request.args['query']
    needles = search(query)
    return render_template('results.html', title='HayStack', needles=needles)
