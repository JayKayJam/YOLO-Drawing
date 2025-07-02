# just to avoid needing to train and run the code at the same time

from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(data="data.yaml", epochs=30, imgsz=640)