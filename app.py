import os, sys
from flask import Flask, render_template, session, jsonify, redirect, url_for, flash

app = Flask(__name__, template_folder='templates')
app.secret_key = 'test'
MODE = os.environ.get('MODE', 'ok')

INFO = dict(full_name='Jumardi Pratama', email='jumardi@example.com', phone='+62 812 9876 5432',
            user_id='GC-00123', devices=3, activities=128, steps=8450, battery=76)

@app.route('/')
def index():
    session.update(user_id=1, full_name=INFO['full_name'], role='admin')
    info = dict(INFO)
    kw = {}
    if MODE == 'bad':
        info.update(steps=None, battery=12, devices='abc', activities=None, full_name='')
        kw['recent_activities'] = []
    elif MODE == 'custom':
        info.update(step_goal=8000, battery=35)
        kw['recent_activities'] = [
            {'icon': 'running', 'title': 'Lari sore', 'detail': '5,2 km', 'time': '1 jam lalu', 'color': 'orange'},
            {'icon': 'fas fa-bicycle', 'title': 'Bersepeda', 'detail': '12 km', 'time': 'Kemarin', 'color': 'purple'},
        ]
        flash('Login berhasil!', 'success')
    return render_template('index.html', info=info, **kw)

@app.route('/login')
def login(): return 'login'

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('login'))

@app.route('/api/dashboard_stats')
def stats():
    if MODE == 'bad': return jsonify(error='x'), 500
    if MODE == 'empty': return jsonify(dates=[], steps=[], calories=[])
    return jsonify(dates=['2026-09-21','2026-09-22','2026-09-23','2026-09-24','2026-09-25','2026-09-26','2026-09-27'],
                   steps=[6520, 8130, 10240, 7410, 12050, 9320, 8450],
                   calories=[310, 385, 470, 350, 560, 430, 402])

if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
