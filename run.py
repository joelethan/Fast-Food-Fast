from app.views.app_views import app,db

if __name__=='__main__':
    db.create_tables()
    db.auto_admin()
    app.run(debug=True, port=5003) 