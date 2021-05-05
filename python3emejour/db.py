# -*- coding: iso-8859-15 -*-
import flask
from flask import redirect, url_for, request, jsonify
import sqlite3
import json
from hashlib import sha256
from datetime import datetime


app = flask.Flask(__name__)
app.config["DEBUG"] = True



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return "<h1>Cours Python</h1><p>Ce site est un exemple d'API .</p>"

######################
# Zone User
######################

@app.route('/user/all', methods=['GET'])
def api_all():
    connexion = sqlite3.connect('wankuldb.db')

    connexion.row_factory = dict_factory
    
    cursor = connexion.cursor()

    all_user = cursor.execute('SELECT * FROM user;').fetchall()

    return jsonify(all_user)

@app.route('/user/create', methods=['POST'])
def add_user():
    connexion = sqlite3.connect('wankuldb.db')

    sql = '''INSERT INTO user(login, password)
                VALUES(?,?) '''
                
    cursor = connexion.cursor()

    body = request.get_json()

    data = json.loads(json.dumps(body))
    pwd_hash = sha256(str(data['password']).encode('utf-8')).hexdigest()
    data_user = (data['login'], pwd_hash)

    cursor.execute(sql, data_user)

    connexion.commit()

    return redirect("http://127.0.0.1:5000/user/all")
    
########################
# Zone BlockChain
########################


@app.route('/blockchain/all', methods=['GET'])
def all_blockchain():
    connexion = sqlite3.connect('wankuldb.db')
    connexion.row_factory = dict_factory   
    cursor = connexion.cursor()
    all_blockchain = cursor.execute('SELECT * FROM Blockchain;').fetchall()
    return jsonify(all_blockchain)

@app.route('/blockchain/create', methods=['POST'])
def add_blockchain():
    connexion = sqlite3.connect('wankuldb.db')

    sql = '''INSERT INTO Blockchain(name) 
            VALUES(?) '''
                
    cursor = connexion.cursor()

    body = request.get_json()
    data = json.loads(json.dumps(body))
    data_blockchain = [str(data['name'])]

    cursor.execute(sql, data_blockchain)

    connexion.commit()

    return redirect("http://127.0.0.1:5000/blockchain/all")


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Wankil page not found bro</p>", 404


########################
# Zone Block
########################


@app.route('/block/all', methods=['GET'])
def all_block():
    connexion = sqlite3.connect('wankuldb.db')
    connexion.row_factory = dict_factory   
    cursor = connexion.cursor()
    all_block = cursor.execute('SELECT * FROM Block;').fetchall()
    return jsonify(all_block)

@app.route('/block/create', methods=['POST'])
def add_block():
    connexion = sqlite3.connect('wankuldb.db')

    sql = '''INSERT INTO Block(previousHash, timestamp, data, nonce, blockHash, blockchainId ) 
            VALUES(?,?,?,?,?,?) '''
                
    cursor_insert = connexion.cursor()

    body = request.get_json()
    data = json.loads(json.dumps(body))

    connexion_select = sqlite3.connect('wankuldb.db')
    connexion_select.row_factory = dict_factory   
    cursor_select = connexion_select.cursor()
    all_block = cursor_select.execute('SELECT * FROM Block;').fetchall()

    if len(all_block) > 0:
        data['previousHash'] = all_block[-1]['blockHash']
    else :
        data['previousHash'] = None
    data['timestamp'] = datetime.today().strftime('%Y-%m-%d::%H-%M')    
    data['nonce'] = 0
    data['blockHash'] = ""
    
    while data['blockHash'][0:4] != "0000":
        data['nonce'] += 1
        block = str(len(all_block)+1)+ str(data['previousHash'])+ str(data['timestamp'])+ str(data['data']) + str(data['nonce'])
        data['blockHash'] = sha256(block.encode('utf-8')).hexdigest()

    data_blockchain = (data['previousHash'],data['timestamp'],data['data'],data['nonce'],data['blockHash'],data['blockchainId'])

    cursor_insert.execute(sql, data_blockchain)

    connexion.commit()

    return redirect("http://127.0.0.1:5000/block/all")

@app.route('/blockchain/block', methods=['GET'])
def api_filter():
    query_parameters = request.args

    name = query_parameters.get('name')

    query = "SELECT * FROM Blockchain WHERE"
    to_filter = []

    if name:
        query += ' name=? ;'
        to_filter.append(name)
    if not (name):
        return page_not_found(404)

    connexion = sqlite3.connect('wankuldb.db')
    connexion.row_factory = dict_factory
    cursor = connexion.cursor()

    blockchain = cursor.execute(query, to_filter).fetchall()

    sql = "SELECT * FROM Block WHERE blockchainId=?;"

    connexion = sqlite3.connect('wankuldb.db')
    connexion.row_factory = dict_factory
    cursor = connexion.cursor()
    results = cursor.execute(sql, [blockchain[0]['id']]).fetchall()

    return jsonify(blockchain,results)

app.run()