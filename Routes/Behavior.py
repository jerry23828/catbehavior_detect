# routes/video_feed.py
from flask import Blueprint, Response, session, jsonify
from Service.Behavior import gen_frames
from Model.Behavior import Behavior

video = Blueprint('video', __name__)


@video.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    owner = session['Uid']
    return Response(gen_frames(owner), mimetype='multipart/x-mixed-replace; boundary=frame')


# @video.route('/behave_statistic', methods=['GET', 'POST'])
# def behave_statistic():
#     category = Behavior.session.query(Behavior.Bclass, Behavior.func.count(Behavior.Bclass).label('count')).group_by(Behavior.Bclass).all()
#     data = {cate: count for cate, count in category}
#     return jsonify(data)
