import cv2
import torch
from flask import current_app
from Model.Behavior import Behavior
from ultralytics import YOLO
from PBD_config import db_init as db, app

# 加载YOLOv8模型
model = YOLO('Data/best.pt')
camera = cv2.VideoCapture(0)


def gen_frames(owner):
    with app.app_context():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                # 使用YOLOv8模型进行检测
                results = model(frame)
                # 绘制检测结果
                for result in results:  # 迭代每个检测结果
                    boxes = result.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        confidence_value = float(conf) if isinstance(conf, torch.Tensor) else float(
                            conf)
                        # 可视化
                        label = f'{model.names[cls]} {conf:.2f}'
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                        behavior = Behavior(Bowner_id=owner, Bclass=label, Bconfidence=confidence_value,
                                            Bphoto=cv2.imencode('.jpg', frame)[1].tobytes())
                        db.session.add(behavior)
                        db.session.commit()

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
