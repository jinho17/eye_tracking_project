from heatmappy import Heatmapper
from PIL import Image
import database_func as db
import img_lib

def percent_to_diameter(percent):
    default = 150

    if percent == 0:
        return 0
    elif percent <= 10:
        return default
    elif percent <= 20:
        return default + 50
    elif percent <= 30:
        return default + 100
    elif percent <= 40:
        return default + 150
    elif percent <= 50:
        return default + 200
    elif percent <= 60:
        return default + 250
    elif percent <= 70:
        return default + 300
    elif percent <= 80:
        return default + 350
    elif percent <= 90:
        return default + 400
    else:
        return default + 450

def heatmap_creaate(user):
    img_tup = db.select_user_imgstr(user)
    num = 1
    for img_str in img_tup:
        img = img_lib.str_to_img(img_str[0])
        img_lib.img_save(img, user, num)
        num = num+1

    points = [(320, 270), (960, 270), (1600, 270), (320, 810), (960, 810), (1660, 810)]

    info = db.select_user_info(user)

    # 입력 이미지 경로 설정
    num = 1

    for gaze in info:
        img_path = 'data/' + user + '_' + str(num) + '.png'
        img = Image.open(img_path)
        for i in range(0, 6):
            point = [points[i]]

            percent = gaze[i+2]
            diameter = percent_to_diameter(percent)

            if diameter == 0:
                continue

            # 히트맵 그리기
            heatmapper = Heatmapper(
                point_diameter=diameter,  # the size of each point to be drawn
                point_strength=1,  # the strength, between 0 and 1, of each point to be drawn
                opacity=0.6,  # the opacity of the heatmap layer
                colours='default',  # 'default' or 'reveal'
                                    # OR a matplotlib LinearSegmentedColorMap object
                                    # OR the path to a horizontal scale image
                grey_heatmapper='PIL'  # The object responsible for drawing the points
                                        # Pillow used by default, 'PySide' option available if installed
            )

            # 이미지 위에 히트맵 그리기
            heatmap = heatmapper.heatmap_on_img(point, img)
            heatmap.save(img_path)
            img = Image.open(img_path)
        num = num + 1
