# app.py
from PBD_config import app
from flask import Flask, render_template, request
from Routes.Behavior import video
from Routes.Users import user
from Routes.Pets import pet

app.register_blueprint(video, url_prefix="/video")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(pet, url_prefix="/pet")
app.secret_key = 'behave_detect'


@app.route('/')
def home():
    # 获取闪现消息
    message = request.args.get('message')
    return render_template('login.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
