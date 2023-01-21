import os
from flask import request, Flask, render_template
import redis
from rq import Queue
from rq.job import Job

from task_alg import factorial_task

app = Flask(__name__)

redis_url = os.getenv('REDISTOGO_URL', 'redis://192.168.122.202:6379')
redisConn = redis.from_url(redis_url)

redisQueue = Queue(connection=redisConn)


@app.route('/task', methods=['GET'])
def get_post():
    return render_template('form.html')

@app.route('/task', methods=['POST'])
def add_task():
    input = request.form.get('input')
    redisJob = redisQueue.enqueue(factorial_task, int(input))
    return f'<html>Task <a href=\"\\result\\{redisJob.id}\">{redisJob.id}</a> has been added to queue. {len(redisQueue)} tasks waiting to be performed</html>'

@app.route('/result/<jobID>')
def get_result(jobID):
    redisJob = Job.fetch(jobID, connection=redisConn)
    print(redisJob.result)
    return str(redisJob.result)

if __name__ == "__main__":
    app.run(debug=True)