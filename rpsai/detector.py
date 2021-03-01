from threading import Thread
import collections

import tensorflow as tf
import numpy as np
import cv2


class Detector:
    def __init__(self, model_path, label_path):
        self.running = True
        self.camera = cv2.VideoCapture(0)
        
        self.results = collections.deque(maxlen=10)
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.target_height = self.input_details[0]['shape'][1]
        self.target_width = self.input_details[0]['shape'][2]
        
        self.classes = {}
        with open(label_path, 'r') as f:
            for line in f.readlines():
                pair = line.strip().split(maxsplit=1)
                self.classes[int(pair[0])] = pair[1].strip()
        
    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        
    def update(self):
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            
            input_data = self.preprocess_image(frame)
            detection = self.predict(input_data)
            frame = self.draw_detection(frame, detection)            
            self.results.append(np.argmax(detection[0]))
            
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        self.camera.release()
        cv2.destroyAllWindows()
        
    def stop(self):
        self.running = False
        
    def preprocess_image(self, frame):
        resized = cv2.resize(frame, (self.target_width, self.target_height))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        normalized = (np.float32(rgb) - 127.5) / 127.5
        input_data = np.expand_dims(normalized, axis=0)
        return input_data
    
    def predict(self, input_data):
        self.interpreter.set_tensor(self.input_details[0]['index'],
                                    input_data)
        self.interpreter.invoke()
        detection = self.interpreter.get_tensor(self.output_details[0]['index'])
        return detection

    def draw_detection(self, frame, detection):
        for i, s in enumerate(detection[0]):
            tag = f'{self.classes[i]}: {s*100:.2f}%'
            cv2.putText(frame, tag, (10, 20 + 20 * i),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 1)
        return frame
    
    def get_result(self):
        if len(self.results) == 0:
            return 0

        counter = collections.Counter(self.results)
        result = counter.most_common()[0][0]
        return result


if __name__ == '__main__':
    import time
    
    d = Detector('model_unquant.tflite', 'labels.txt')
    d.start()
    
    for i in range(20):
        print(i, d.get_result())
        time.sleep(1)
    
    d.stop()
