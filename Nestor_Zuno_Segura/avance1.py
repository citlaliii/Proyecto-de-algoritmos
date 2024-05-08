import cv2
import platform
import math

class Webcam:
    def __init__(self):
        self.stopped = False
        self.stream = None
        self.lastFrame = None
        self.os_name = platform.system()

    def start(self):
        if self.stream is None:
            if self.os_name == "Windows":
                self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            elif self.os_name == "Darwin": # macOS
                self.stream = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
            else: # Linux
                self.stream = cv2.VideoCapture(0, cv2.CAP_V4L)
        return self

    def read(self):
        ret, frame = self.stream.read()
        if ret:
            return frame
        else:
            return None

    def stop(self):
        if self.stream is not None:
            self.stream.release()
            self.stream = None

    def width(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)

    def height(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def process_camera(self):
        image = self.read()
        if image is not None:
            image.flags.writeable = False
            image = cv2.flip(image, 1)
            image.flags.writeable = True
            # Actualizamos self.lastFrame con el último fotograma capturado
            self.lastFrame = image
            # Llamamos a detect_head_movement para calcular el ángulo de movimiento de la cabeza
            self.detect_head_movement()

    def detect_head_movement(self):
        if self.lastFrame is not None:
            # Convertir la imagen a escala de grises para simplificar la detección de movimiento
            gray = cv2.cvtColor(self.lastFrame, cv2.COLOR_BGR2GRAY)
            # Detectar caras en la imagen
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Si se detecta al menos una cara
            if len(faces) > 0:
                # Se asume que el primer rectángulo del array faces corresponde a la cara más grande
                (x, y, w, h) = faces[0]
                # Calcular el centro de la cara
                face_center_x = x + w // 2
                face_center_y = y + h // 2
                # Girar el fotograma 90 grados en sentido antihorario
                rotated_frame = cv2.transpose(self.lastFrame)
                rotated_frame = cv2.flip(rotated_frame, 0)
                # Dibujar un círculo en el centro de la cara en el fotograma girado
                cv2.circle(rotated_frame, (face_center_y, rotated_frame.shape[0] - face_center_x), 5, (0, 255, 0), -1)
                # Mostrar el fotograma girado en la ventana
                cv2.imshow("Webcam", rotated_frame)
                cv2.waitKey(1)
                # Calcular el desplazamiento horizontal y vertical desde el centro de la ventana
                center_x = self.width() // 2
                center_y = self.height() // 2
                dx = face_center_x - center_x
                dy = face_center_y - center_y
                # Calcular el ángulo de movimiento de la cabeza (en grados)
                angle = math.atan2(dy, dx) * 180.0 / math.pi
                print("Ángulo de movimiento de la cabeza:", angle)

def main():
    # Inicializar la cámara
    webcam = Webcam()
    webcam.start()

    # Bucle principal
    running = True
    while running:
        # Procesar imagen de la cámara
        webcam.process_camera()

    # Detener la cámara
    webcam.stop()

if __name__ == "__main__":
    main()
