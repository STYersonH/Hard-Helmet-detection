from ultralytics import YOLO
import yagmail
import cv2
import math
import pygame
import os
from datetime import datetime

def video_detection(path_x):
    video_capture = path_x
    # crear el objeto de la camara
    cap = cv2.VideoCapture(video_capture) # abrir el video
    frame_width = int(cap.get(3)) # obtener el ancho del frame
    frame_height = int(cap.get(4)) # obtener el alto del frame

    model = YOLO("YOLO-Weights/ppe.pt")  # Cargar el modelo YOLOv entrenado
    classNames = ['head', 'helmet', 'person']  # Clases que se detectaran

    contador = 0 # si el contador llega a 10 se activa la alarma
    alarm_playing = False  # para controlar cuando sonara la alarma
    pygame.mixer.init()  # inicializar pygame para reproducir la alarma

    while True:
        success, img = cap.read()  # leer el frame actual
        results = model(img, stream=True)  # procesar el frame actual

        head_detected = False  # para controlar si se detecta una cabeza

        # Recorrer los resultados obtenidos en el frame actual (todos los objetos detectados)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # ANALIZAR LOS RESULTADOS
                # -----------------------

                x1, y1, x2, y2 = box.xyxy[0]  # coordenadas de la caja del objeto detectado
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(x1, y1, x2, y2)
                conf = math.ceil((box.conf[0] * 100)) / 100  # confianza del objeto detectado
                cls = int(box.cls[0])  # clase del objeto detectado
                class_name = classNames[cls]  # obtener nombre de la clase del objeto detectado
                label = f'Casco Detectado {conf}' if class_name.lower() == 'helmet' else f'Casco no detectado {conf}' # etiqueta que se mostrara en el frame

                print('resultados: ', class_name)  # imprimir la clase del objeto detectado

                # Si se detecta alguna cabeza con una confianza mayor a 0.5 en el frame actual
                if class_name == 'head' and conf > 0.5:
                    head_detected = True

                # Dibujar la caja y la etiqueta del objeto detectado en el frame actual
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                print(t_size)
                c2 = x1 + t_size[0], y1 - t_size[1] - 3  # obtener coordenadas de la etiqueta

                # Asignar un color a la caja y la etiqueta del objeto detectado
                if class_name == "helmet":
                    color = (67,215,5)
                else:
                    color = (32,40,210)

                # DIBUJAR LA CAJA Y LA ETIQUETA DEL OBJETO DETECTADO EN EL FRAME ACTUAL
                # ---------------------------------------------------------------------
            
                if conf > 0.5:
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)  # caja
                    cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)  # fondo de la etiqueta
                    cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1,
                                lineType=cv2.LINE_AA)  # etiqueta

        # Si se detecta una cabeza, se aumenta el contador
        if head_detected:
            contador += 1
        else:
            contador = 0

        # Si se detecta una cabeza y no se esta reproduciendo la alarma, se reproduce
        if contador >= 10 and not alarm_playing:
            # ACTIVAR LA ALARMA
            # -----------------
            pygame.mixer.music.load('alarm.mp3')
            pygame.mixer.music.play()
            alarm_playing = True

            # CREAR EL REPORTE
            # ----------------

            # Guardar la imagen y sobreponerla en cada momento.
            frame_filename = os.path.join('', f"report.jpeg")
            cv2.imwrite(frame_filename, img)

            # Get the current date in the format YYYY-MM-DD
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Define the responsible person and the shift
            persona_encargada = "SEGURIDAD PUERTA 6 - AREA DE PREVENCION"
            turno = "Mañana"

            # Rest of your code
            email = "edward.melendez.mendigure@gmail.com"
            password = "mpjccskhhqupkzhh"
            yag = yagmail.SMTP(user=email, password=password)
            senders = ['192666@unsaac.edu.pe']
            head = "Reporte de incidentes - CONSTRUCTORA"
            body = ""
            file_report = 'report.html'
            image_filename = 'report.jpeg'

            # Read the content of the HTML file
            with open(file_report, 'r') as file:
                html_content = file.read()

            # Replace the placeholders with the current values
            html_content = html_content.replace('%fecha_actual%', current_date)
            html_content = html_content.replace('%persona_encargada%', persona_encargada)
            html_content = html_content.replace('%turno%', turno)

            # Save the modified HTML to a new file (optional)
            with open('modified_report.html', 'w') as modified_file:
                modified_file.write(html_content)

            # ENVIAR EL REPORTE POR CORREO
            # ----------------------------

            # Send the email with the attached report
            yag.send(senders, head, [body], attachments=['modified_report.html', image_filename])


        # si no se detecta alguna cabeza y se esta reproduciendo la alarma, se detiene
        elif not head_detected and alarm_playing:
            pygame.mixer.music.stop()
            alarm_playing = False

        # DIBUJAR EL CONTADOR EN LA PANTALLA
        # ----------------------------------
        # Display the counter on the screen
        counter_label = f'sin casco: {contador}'
        # Define the size of the text box
        text_size = cv2.getTextSize(counter_label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

        # Define the coordinates of the box
        box_coords = ((10, img.shape[0] - 20), (10 + text_size[0] + 20, img.shape[0] - text_size[1] - 20))

        # Draw a semi-transparent rectangle as the background of the text
        overlay = img.copy()
        cv2.rectangle(overlay, box_coords[0], box_coords[1], (17, 156, 242), -1)

        # Combine the image with the overlay with a certain alpha
        alpha = 0.6
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        # Put the text on the image
        cv2.putText(img, counter_label, (20, img.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        yield img  # retornar el flujo de imagenes procesadas

cv2.destroyAllWindows()
