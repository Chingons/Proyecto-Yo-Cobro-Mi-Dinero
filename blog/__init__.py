from flask import Flask

app = Flask(__name__, template_folder='templates')
app.secret_key = 'B867C43697225424DA95D30D54212201121177704A315DA56D2867068892F8F9'

from blog import rutas