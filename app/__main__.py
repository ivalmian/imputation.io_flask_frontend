'''
app.__main__
-------------------
Flask debug runner.

Normally should use 

bin/run_local.sh

which utilizes gunicorn as the app server
'''

from app import app

if __name__=='__main__':
    app.run(debug=True)