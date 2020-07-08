"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import time
import threading
import cv2
import numpy as np
from gaze_tracking import GazeTracking

import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage, QPixmap, QCloseEvent
from PyQt5.QtWidgets import QApplication, QStackedWidget
from GUImain.GUIframe import MyApp

import keyboard
import keyboard_event as event
import database_func as db

end_sig = False
img_num = 0
esc = False

webcam = cv2.VideoCapture(0)
R_top = 0
L_top = 0
C_top = 0

R_bottom = 0
L_bottom = 0
C_bottom = 0

avg_top_right = 0
avg_top_left = 0
avg_bottom_right = 0
avg_bottom_left = 0
avg_top_center = 0
avg_bottom_center = 0

total_left_hor_gaze = 0
total_right_hor_gaze = 0
total_top_ver_gaze = 0
total_bottom_ver_gaze = 0

sectionA =0
sectionB =0
sectionC =0
sectionD =0
sectionE =0
sectionF =0

section = "None"

count = 1
test_count = 1
flag = 0
gaze = GazeTracking()


#GUI
app = QApplication(sys.argv)
gui = MyApp()
gui.Stack.setCurrentWidget(gui.stack1)
gui.currentStack = 1
gui.name_btn.clicked.connect(gui.change_display)

def Section(where):
        global sectionA, sectionB, sectionC, sectionD, sectionE, sectionF
        if where == "A":
            sectionA += 1
            return sectionA
        elif where == "B":
            sectionB += 1
            return sectionB
        elif where == "C":
            sectionC += 1
            return sectionC
        elif where == "D":
            sectionD += 1
            return sectionD
        elif where == "E":
            sectionE += 1
            return sectionE
        elif where == "F":
            sectionF += 1
            return sectionF


def Thread_run():
    print(section, ":", Section(section))
    thread = threading.Timer(1, Thread_run)
    thread.daemon = True
    thread.start()
    return thread

thread = Thread_run()

while True:
    #GUI
    if gui.quit_sig:
        sys.exit()


    if bool(gui.start_btn.isChecked()):
        # We get a new frame from the webcam
        _, frame = webcam.read()
        new_frame = np.zeros((500, 500, 3), np.uint8)

        gaze.refresh(frame)
        frame, loc1, loc2 = gaze.annotated_frame()

        text = ""

        '''
        #draw face guide line
        red_color = (0, 0, 255)
        guide_x1 = 150
        guide_y1 = 100
        guide_w = 300
        guide_h = 300
        face_line = cv2.rectangle(frame, (guide_x1, guide_y1), (guide_x1 + guide_w, guide_y1 + guide_h), red_color, 3)
        '''

        #GUI
        #if bool(gui.start_btn.isChecked()):
        if test_count < 50:
            cv2.circle(frame, (25, 25), 25, (0, 0, 255), -1)
            if gaze.horizontal_ratio() != None and gaze.vertical_ratio() != None:
                total_left_hor_gaze += gaze.horizontal_ratio()
                total_top_ver_gaze += gaze.vertical_ratio()
                test_count += 1
                print("hor ratio1:", gaze.horizontal_ratio())
                print("ver ratio1:", gaze.vertical_ratio())

        elif 50 <= test_count < 100:
            cv2.circle(frame, (610, 25), 25, (0, 0, 255), -1)
            if gaze.horizontal_ratio() != None and gaze.vertical_ratio() != None:
                total_right_hor_gaze += gaze.horizontal_ratio()
                total_top_ver_gaze += gaze.vertical_ratio()
                test_count += 1
                print("hor ratio2:", gaze.horizontal_ratio())
                print("ver ratio2:", gaze.vertical_ratio())

        elif 100 <= test_count < 150:
            cv2.circle(frame, (25, 450), 25, (0, 0, 255), -1)
            if gaze.horizontal_ratio() != None and gaze.vertical_ratio() != None:
                total_left_hor_gaze += gaze.horizontal_ratio()
                total_bottom_ver_gaze += gaze.vertical_ratio()
                test_count += 1
                print("hor ratio3:", gaze.horizontal_ratio())
                print("ver ratio3:", gaze.vertical_ratio())


        elif 150 <= test_count < 200:
            cv2.circle(frame, (610, 450), 25, (0, 0, 255), -1)
            if gaze.horizontal_ratio() != None and gaze.vertical_ratio() != None:
                total_right_hor_gaze += gaze.horizontal_ratio()
                total_bottom_ver_gaze += gaze.vertical_ratio()
                test_count += 1
                print("hor ratio4:", gaze.horizontal_ratio())
                print("ver ratio4:", gaze.vertical_ratio())
                gaze_time = int(time.time())
            save_loc1 = loc1
            save_loc2 = loc2

        else:
            if flag == 0:
                avg_left_hor_gaze = total_left_hor_gaze / 100
                avg_right_hor_gaze = total_right_hor_gaze / 100
                avg_top_ver_gaze = total_top_ver_gaze / 100
                avg_bottom_ver_gaze = total_bottom_ver_gaze / 100
                print(avg_left_hor_gaze, avg_right_hor_gaze, avg_top_ver_gaze, avg_bottom_ver_gaze)
                flag = 1

            if gaze.is_blinking():
                text = "Blinking"

            if gaze.is_top_right(avg_right_hor_gaze, avg_top_ver_gaze):
                new_frame[:] = (0, 200, 227)
                text = "Looking top right"
                section = "A"
            elif gaze.is_top_left(avg_left_hor_gaze, avg_top_ver_gaze):
                new_frame[:] = (0, 0, 255)
                text = "Looking top left"
                section = "B"
            elif gaze.is_bottom_right(avg_right_hor_gaze, avg_top_ver_gaze):
                new_frame[:] = (255, 0, 170)
                text = "Looking bottom right"
                section = "C"
            elif gaze.is_bottom_left(avg_left_hor_gaze, avg_top_ver_gaze):
                new_frame[:] = (0, 255, 0)
                text = "Looking bottom left"
                section = "D"
            elif gaze.is_top_center(avg_top_ver_gaze, avg_right_hor_gaze, avg_left_hor_gaze):
                new_frame[:] = (0, 104, 250)
                text = "Looking top center"
                section = "E"
            elif gaze.is_bottom_center(avg_top_ver_gaze, avg_right_hor_gaze, avg_left_hor_gaze):
                new_frame[:] = (255, 0, 0)
                text = "Looking bottom center"
                section = "F"

            cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.rectangle(frame, save_loc1, save_loc2, (0, 0, 255), 2)
        if test_count < 200:
            cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            #cv2.imshow("New Frame", new_frame)
            cv2.imshow("Frame", frame)

        else:
            cv2.destroyAllWindows()

        #database
        if keyboard.is_pressed('down') or keyboard.is_pressed('up'):
            gaze_time = int(time.time()) - gaze_time
            img_num = img_num + 1
            gaze_info = [gui.name, img_num, sectionA, sectionB, sectionC, sectionD, sectionE, sectionF, gaze_time]
            end_sig = event.tracking_con(gaze_info)
            sectionA = 0
            sectionB = 0
            sectionC = 0
            sectionD = 0
            sectionE = 0
            sectionF = 0
            gaze_time = time.time()


        elif keyboard.is_pressed('esc'):
            print('esc press')
            gaze_time = int(time.time()) - gaze_time
            img_num = img_num + 1
            gaze_info = [gui.name, img_num, sectionA, sectionB, sectionC, sectionD, sectionE, sectionF, gaze_time]
            esc = event.tracking_end(gaze_info)

        # GUI
        gui.start = True
        qformat = QImage.Format_Indexed8
        if len(frame.shape) == 3:
            if frame.shape[2] == 4:  # RGBA
                qformat = QImage.Format_RGBA8888
            else:  # RGB
                qformat = QImage.Format_RGB888
        out_image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], qformat)
        out_image = out_image.rgbSwapped()
        gui.face_label.setAlignment(QtCore.Qt.AlignCenter)
        gui.face_label.setPixmap(QPixmap.fromImage(out_image))
    elif gui.start:
        if not end_sig:
            if not esc:
                gaze_time = int(time.time()) - gaze_time
                img_num = img_num + 1
                gaze_info = [gui.name, img_num, sectionA, sectionB, sectionC, sectionD, sectionE, sectionF, gaze_time]
                end_sig = event.tracking_end(gaze_info)
            thread.cancel()
            cv2.destroyAllWindows()

            gui.Stack.setCurrentWidget(gui.stack3)
            gui.currentStack = 3

            info = db.select_user_info(gui.name)

            gaze_num = 0
            for gaze in info:
                gaze_num = gaze_num + 1
            num = 1
            loop = 1000
            end_sig = True

        if loop == 1000:
            img_path = "data/"+gui.name+"_"+str(num)+".png"
            print(img_path)
            graph = QPixmap(img_path)
            graph = graph.scaledToWidth(800)
            gui.graph_label.setPixmap(graph)
            num = num + 1
            if num > gaze_num:
                num = 1
            loop = 0
        loop = loop + 1


    if cv2.waitKey(1) == 27:
        break


total_gaze = R_top + L_top + C_top + R_bottom + L_bottom + C_bottom



# print("Top Gaze ratio : ", round(R_top/total_gaze, 2), round(L_top/total_gaze,2), round(C_top/total_gaze,2))
# print("Bottom Gaze ratio: ", round(R_bottom/total_gaze,2), round(L_bottom/total_gaze,2), round(C_bottom/total_gaze,2))
cv2.destroyAllWindows()