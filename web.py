# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 's3cr3t-k3y!!11'
app.config['MONGODB_SETTINGS'] = {'DB': 'boadica'}

db = MongoEngine(app)


class Produto(db.Document):
    fabricante = db.StringField()
    modelo = db.StringField()
    especificacoes = db.StringField()
    preco = db.DecimalField()
    vendedor = db.StringField()
    vendedor_link = db.StringField()
    local = db.StringField()

    def __unicode__(self):
        return '{0} - {1}'.format(self.fabricante, self.modelo)


@app.route('/')
def index():
    produtos = Produto.objects.all()

    return render_template('lista.html', produtos=produtos)

if __name__ == '__main__':
    app.run()
