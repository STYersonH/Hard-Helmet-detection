from ultralytics import YOLO
import cv2
import math
import pygame

def video_detection(path_x):
    video_capture = path_x
    #Create a Webcam Object
    cap=cv2.VideoCapture(video_capture)
    frame_width=int(cap.get(3))
    frame_height=int(cap.get(4))
    #out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P','G'), 10, (frame_width, frame_height))

    model=YOLO("YOLO-Weights/ppe.pt")
    #classNames = ['helmet_blue', 'helmet_white', 'helmet_yellow', 'no_hard_hat']
    classNames = ['head', 'helmet', 'person']


    alarm_playing = False  # Add this line before the while loop
    pygame.mixer.init()

    while True:
        success, img = cap.read()
        results=model(img,stream=True)

        head_detected = False  # Add this line before the while loop

        for r in results:
            boxes=r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                print(x1,y1,x2,y2)
                conf=math.ceil((box.conf[0]*100))/100
                cls=int(box.cls[0])
                class_name=classNames[cls]
                label=f'{class_name}{conf}'
                
                print('resultados: ', class_name)
                
                # detect head to run the alarm
                if class_name == 'head' and conf > 0.5:
                    head_detected = True
                
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                print(t_size)
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                if class_name == 'head':
                    color=(0, 204, 255)
                elif class_name == "helmet":
                    color = (222, 82, 175)
                elif class_name == "person":
                    color = (0, 149, 255)
                else:
                    color = (85,45,255)
                if conf>0.5:
                    cv2.rectangle(img, (x1,y1), (x2,y2), color,3)
                    cv2.rectangle(img, (x1,y1), c2, color, -1, cv2.LINE_AA)  # filled
                    cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
       

        '''
        # Check if a 'head' is detected and the alarm is not playing
        if head_detected and not alarm_playing:
            playsound('alarm.mp3')  # Play alarm sound
            alarm_playing = True
        elif not head_detected and alarm_playing:
            # Stop the alarm if a 'head' is not detected
            # Note: playsound does not support stopping a sound in the middle, 
            # so you might need to use a shorter sound clip or a different library if this is required
            alarm_playing = False
        '''
        if head_detected and not alarm_playing:
            pygame.mixer.music.load('alarm.mp3')
            pygame.mixer.music.play()
            alarm_playing = True
        elif not head_detected and alarm_playing:
            pygame.mixer.music.stop()
            alarm_playing = False

        yield img
        #out.write(img)
        #cv2.imshow("image", img)
        #if cv2.waitKey(1) & 0xFF==ord('1'):
            #break
    #out.release()
cv2.destroyAllWindows()