from api.views import app,db

if __name__=='__main__':
    db.create_tables()
    app.run(debug=True, port=5003) 