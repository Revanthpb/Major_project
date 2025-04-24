from ultralytics import YOLO
import cv2

def detect_threat(video_path='data/videos/test.mp4', model_path='object_detection/model/best.pt'):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, save=False, conf=0.3)
        for result in results:
            result.plot()
            annotated = result.plot()
            cv2.imshow('YOLOv8 Threat Detection', annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_threat()