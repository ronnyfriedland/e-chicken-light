from flask import Flask

from _cron import *

next_execution = datetime.datetime.now() + datetime.timedelta(minutes=5)

create_cron("e-chicken-light-check-job", "/usr/local/bin/python /usr/src/app/check.py --verbose", start=next_execution, interval=ExecutionPlan.weekly)

app = Flask(__name__)


@app.route('/crons')
def crons():
  return '<br/>'.join(list_crons())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')