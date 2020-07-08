import keyboard
import time
import img_lib
import database_func as db
from io import BytesIO
from PIL import ImageGrab
import heatmap

def tracking_con(gaze_info):
    now = time.localtime()
    t = "%04d/%02d/%02d/%02dh/%2dm/%02ds" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    img_buffer = BytesIO()
    img = ImageGrab.grab()
    img.save(img_buffer, format='png')
    img_str = img_lib.img_to_str(img_buffer)
    gaze_info.append(t)
    gaze_info.append(img_str)
    db.insert_gaze_info(gaze_info)
    db.insert_gaze_screen(gaze_info)
    key = int(time.time())
    while True:
        now = int(time.time())
        if now - key >= 2:
            end_sig = False
            break

        if keyboard.is_pressed('down') or keyboard.is_pressed('up'):
            key = int(time.time())
        elif keyboard.is_pressed('esc'):
            end_sig = True
            break
    return end_sig

def tracking_end(gaze_info):
    now = time.localtime()
    t = "%04d/%02d/%02d/%02dh/%2dm/%02ds" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    img_buffer = BytesIO()
    img = ImageGrab.grab()
    img.save(img_buffer, format='png')
    img_str = img_lib.img_to_str(img_buffer)
    gaze_info.append(t)
    gaze_info.append(img_str)
    db.insert_gaze_info(gaze_info)
    db.insert_gaze_screen(gaze_info)
    heatmap.heatmap_creaate(gaze_info[0])
    db.select_user_info_to_excel(gaze_info[0])
    end_sig = True
    return end_sig
