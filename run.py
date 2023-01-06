from blog import app

app.config['SECRET_KEY'] = '\x88\xa7\xd9q\x1a5YJ\x0f\xbc\xc4\xd9q\xae\x99\xbe2\x97\xb0\x0c\t\x17\x12i'

if __name__ == "__main__":
    app.run(debug = True, port=5000, host="0.0.0.0")

