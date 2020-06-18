'''
imputationflask.__main__
-------------------
Flask debug runner.

Normally should use

bin/run_local.sh

which utilizes gunicorn as the app server
'''

from imputationflask import app

if __name__ == '__main__':
    app.run(debug=True)
