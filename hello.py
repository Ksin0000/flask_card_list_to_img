from flask import Flask, render_template, request, url_for
import requests
import time

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("hello.html", url=url_for("card_list_input"))

@app.route("/card_list", methods=["GET"])
def card_list_input():
    textarea_template='1 Arcane Signet\n1 Chaos Warp'
    return render_template("card_list.html", textarea_text=textarea_template)

@app.route("/card_list", methods=["POST"])
def card_list_output():
    card_dict={}
    for i in request.form['cardlist'].split('\n'):
        if not i: continue
        card_name=i[i.find(' '):]
        url_items=r'https://api.scryfall.com/cards/named?exact='
        r_get = requests.get(url_items + card_name)
        time.sleep(0.1)#We kindly ask that you insert 50 – 100 milliseconds of delay between the requests you send to the server at api.scryfall.com. (i.e., 10 requests per second on average).
        r_get_json=r_get.json()
        if r_get_json['object'] == 'card':#カードが検索できなければ載せない
            print(card_name)
            if 'image_uris' in r_get_json:#普通のカード
                card_dict[card_name]=r_get_json['image_uris']['small']
            elif 'card_faces' in r_get_json:#両面カードなど
                card_dict[card_name]=r_get_json['card_faces'][0]['image_uris']['small']
            else : 
                card_dict[card_name]=''
    return render_template("card_list.html", textarea_text=request.form['cardlist'], card_dict=card_dict)
