# -*- coding: iso-8859-15 -*-
import flask
from flask import redirect, url_for, request, jsonify,render_template
from flask_cors import CORS, cross_origin
import sqlite3
import json
from hashlib import sha256
from datetime import datetime


app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True


######################
# All function
######################

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def dbConnection():
    connexion = sqlite3.connect('wankuldb.db')
    connexion.row_factory = dict_factory
    return connexion

def verifyToken(userHeader):
    connexion = dbConnection()

    sql = "SELECT * FROM user WHERE login=?;"

    connexion.row_factory = dict_factory
    cursor = connexion.cursor()
    infoUser = cursor.execute(sql, [userHeader['login']]).fetchall()

    testToken = sha256(str(infoUser[0]['hashPassword']).encode('utf-8') + str("connect").encode('utf-8')).hexdigest()
    connexion.close()
    if userHeader['token'] == testToken:
        return True
    else : 
        return False

def userHeader(request):
    header = {
        "login": request.headers['Login'],
        "token": request.headers['Token']
    }

    return header

######################
# Home
######################

@app.route('/', methods=['GET'])
def home():
    return "<h1>Cours Python</h1><p>Bienvenu chez nous !.</p>"

######################
# Zone User
######################

@app.route('/user/all', methods=['GET'])
def api_all():
    if verifyToken(userHeader(request)) :    
        connexion = dbConnection()
        cursor = connexion.cursor()
        all_user = cursor.execute('SELECT * FROM user;').fetchall()
        connexion.close()
        return jsonify(all_user)
    else :
        return token_not_valid()


@app.route('/user/create', methods=['POST'])
def add_user():
    connexion = dbConnection()
    sql = '''INSERT INTO user(login, password, hashPassword)
                VALUES(?,?,?) '''
                
    cursor = connexion.cursor()
    data = request.form
    pwd_hash = sha256(str(data['password']).encode('utf-8')).hexdigest()
    password = sha256(str(data['login']).encode('utf-8') + str(pwd_hash).encode('utf-8')).hexdigest()
    data_user = (data['login'], password, pwd_hash)
    cursor.execute(sql, data_user)
    connexion.commit()
    connexion.close()
    return redirect("http://127.0.0.1:5000/user/all")
    

@app.route('/user/login', methods=['POST'])
def login():
    connexion = dbConnection()

    sql = "SELECT * FROM user WHERE login=?;"

    data = request.form
    pwd_hash = sha256(str(data['password']).encode('utf-8')).hexdigest()
    test_password = sha256(str(data['login']).encode('utf-8') + str(pwd_hash).encode('utf-8')).hexdigest()

    cursor = connexion.cursor()
    infoUser = cursor.execute(sql, [data['login']]).fetchall()
    connexion.close()
    if infoUser[0]['password'] == test_password:
        token = sha256(str(infoUser[0]['hashPassword']).encode('utf-8') + str("connect").encode('utf-8')).hexdigest()
        user = {
            "login": infoUser[0]['login'],
            "token": token
        }
        return render_template("traitement.html", user=user)
    else : 
        return error_page("Informations d'identification incorrectes")

    


    
########################
# Zone BlockChain
########################


@app.route('/blockchain/all', methods=['GET'])
def all_blockchain():
    if verifyToken(userHeader(request)) :
        connexion = dbConnection()   
        cursor = connexion.cursor()
        all_blockchain = cursor.execute('SELECT * FROM Blockchain;').fetchall()
        connexion.close()
        return jsonify(all_blockchain)
    else :
        return token_not_valid()

@app.route('/blockchain/create', methods=['POST'])
def add_blockchain():
    if verifyToken(userHeader(request)) :
        data = request.form
        if len(data) == 0:
            return render_template("creation.html")
        else :
            data_blockchain = [str(data['newBlockchain'])]
            connexion = dbConnection()
            sql = '''INSERT INTO Blockchain(name) 
                    VALUES(?) '''
            cursor = connexion.cursor()
            cursor.execute(sql, data_blockchain)
            connexion.commit()
            connexion.close()
            return redirect("http://localhost:5000/accueil")
    else :
        return token_not_valid()


########################
# Zone Block
########################


@app.route('/block/all', methods=['GET'])
def all_block():
    if verifyToken(userHeader(request)) :
        connexion = dbConnection() 
        cursor = connexion.cursor()
        all_block = cursor.execute('SELECT * FROM Block;').fetchall()
        return jsonify(all_block)
    else :
        return token_not_valid()

@app.route('/block/create', methods=['POST'])
def add_block():
    if verifyToken(userHeader(request)) :
        connexion = dbConnection() 
        sql = '''INSERT INTO Block(previousHash, timestamp, data, nonce, blockHash, blockchainId ) 
                VALUES(?,?,?,?,?,?) '''
        cursor = connexion.cursor()
        body =  request.form
        data = {
            "data" : body['data'],
            "blockchainName" : body['blockchainName']
        }
        query = "SELECT * FROM Blockchain WHERE name=?;"
        blockchain_name = data['blockchainName']
        blockchain = cursor.execute(query,[blockchain_name]).fetchall()
        if len(blockchain) != 0:
            blockchain_id = blockchain[0]['id']
            all_block = cursor.execute(f'SELECT * FROM Block WHERE blockchainId={blockchain_id};').fetchall()
            if len(all_block) > 0:
                data['previousHash'] = all_block[-1]['blockHash']
            else :
                data['previousHash'] = None
            data['timestamp'] = datetime.today().strftime('%Y-%m-%d::%H-%M')    
            data['nonce'] = 0
            data['blockHash'] = ""
            data['blockchainId'] = blockchain_id
            while data['blockHash'][0:4] != "0000":
                data['nonce'] += 1
                block = str(len(all_block)+1)+ str(data['previousHash'])+ str(data['timestamp'])+ str(data['data']) + str(data['nonce'])
                data['blockHash'] = sha256(block.encode('utf-8')).hexdigest()
            data_blockchain = (data['previousHash'],data['timestamp'],data['data'],data['nonce'],data['blockHash'],data['blockchainId'])
            cursor.execute(sql, data_blockchain)
            connexion.commit()
            connexion.close()
            return redirect(f"http://127.0.0.1:5000/accueil?Blockchain={blockchain_name}")
        else :
            return error_page("Blockchain inconnu")
    else :
        return token_not_valid()

@app.route('/block/suppr', methods=['DELETE'])
def del_block():
    if verifyToken(userHeader(request)):
        connexion = sqlite3.connect('wankuldb.db')
        connexion.row_factory = dict_factory  
        cursor = connexion.cursor()

        body = request.get_json()
        data = ""

        if len(body) > 0:
            data = json.loads(json.dumps(body))
        else :
            return error_page("error")

        query = "SELECT * FROM Blockchain WHERE name=?;"

        blockchain = cursor.execute(query,[data['blockchainName']]).fetchall()
        blockchain_id = blockchain[0]['id']

        requete = 'SELECT * FROM Block WHERE blockchainId=?;'
        all_block = cursor.execute(requete, [blockchain_id]).fetchall()

        for i in range(data['nb_suppression']):
            index_a_supprimer = all_block[-i]['index']
            requete_suppr = "DELETE FROM Block WHERE `index`=?;"
            execute = cursor.execute(requete_suppr, [index_a_supprimer]).fetchall()
            connexion.commit()

        all_block = cursor.execute('SELECT * FROM Block;').fetchall()

        if len(all_block) == 0:
            update = "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='Block';"
            execute = cursor.execute(update)
            connexion.commit()
            connexion.close()
        return redirect("http://127.0.0.1:5000/block/all")
    else :
        return token_not_valid()

@app.route('/blockchain/block', methods=['GET'])
def api_filter():
    if verifyToken(userHeader(request)) :
        connexion = dbConnection()
        query_parameters = request.args
        name = query_parameters.get('name')
        query = "SELECT * FROM Blockchain WHERE name=? ;"
        cursor = connexion.cursor()
        blockchain = cursor.execute(query, [name]).fetchall()
        if len(blockchain) > 0 :
            sql = "SELECT * FROM Block WHERE blockchainId=?;"
            results = cursor.execute(sql, [blockchain[0]['id']]).fetchall()
            infoBlockchain = {"blockchain":blockchain,"blocks":results}
            # render_template("./templates/acceuil.html", blockchain=infoBlockchain)
            connexion.close()
            return jsonify(infoBlockchain)
        else :
            return error_page("error")
    else :
        return token_not_valid()

@app.route('/accueil', methods=['GET'])
def accueilPage():
    return render_template("accueil.html")
@app.route('/creation', methods=['GET'])
def creationPage():
    return render_template("creation.html")
@app.route('/login', methods=['GET'])
def loginPage():
    return render_template("connexion.html")

@app.errorhandler(404)
def page_not_found(e):
    return error_page("Page not found bro")

def user_not_found():
    return "<h1>404</h1><p>User not found bro</p>"

def token_not_valid():
    return error_page("Token not valid bro")

def error_page(error):
    return render_template("error.html", error=error)

app.run()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})