import pymysql
import os
from openpyxl import Workbook
from openpyxl import load_workbook

#전체 Select
host = '192.168.25.10'

def select_all():
    conn = pymysql.connect(host=host, port=3306, user='root', password='1234', db='capstone', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = "select * from gaze_info"
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                print(row)
    finally:
        conn.close()

def select_user_info(user):
    conn = pymysql.connect(host=host, port=3306, user='root', password='1234', db='capstone', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = "SELECT * FROM gaze_info WHERE user = %(user)s"
            curs.execute(sql, {'user': user})
            rs = curs.fetchall()
    finally:
        conn.close()
        return rs

def select_user_imgstr(user):
    conn = pymysql.connect(host=host, port=3306, user='root', password='1234', db='capstone', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = "select img from gaze_screen WHERE user = %(user)s"
            curs.execute(sql, {'user': user})
            rs = curs.fetchall()
    finally:
        conn.close()
        return rs

#DB Insert
def insert_gaze_info(gaze_info):
    conn = pymysql.connect(host=host, port=3306, user='root', password='1234', db='capstone', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'insert into gaze_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            total_gaze = 0
            for i in range(2, 8):
                total_gaze = total_gaze + gaze_info[i]
            for i in range(2, 8):
                if gaze_info[i] != 0:
                    print(gaze_info[i]/total_gaze)
                    gaze_info[i] = round((gaze_info[i]/total_gaze)*100)
                else:
                    pass
            curs.execute(sql, (gaze_info[0], gaze_info[1], gaze_info[2], gaze_info[3], gaze_info[4], gaze_info[5],
                               gaze_info[6], gaze_info[7], gaze_info[8], gaze_info[9]))
        conn.commit()
    finally:
        conn.close()

def insert_gaze_screen(gaze_info):
    conn = pymysql.connect(host=host, port=3306, user='root', password='1234', db='capstone', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'insert into gaze_screen values(%s, %s, %s)'
            curs.execute(sql, (gaze_info[0], gaze_info[1], gaze_info[10]))
        conn.commit()
    finally:
        conn.close()


def select_user_info_to_excel(user):
    conn = pymysql.connect(host=host, port=3306, user='root', password='1234', db='capstone', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = "SELECT * FROM gaze_info WHERE user = %(user)s"
            curs.execute(sql, {'user': user})
            rs = curs.fetchall()

            wb = Workbook()
            ws = wb.active

            # 첫행 입력
            ws.append(('user', 'num', 'A(%)', 'B(%)', 'C(%)', 'D(%)', 'E(%)', 'F(%)', 'gaze_time', 'time'))

            # DB 모든 데이터 엑셀로
            for row in rs:
                ws.append(row)

            xl_name = 'data/' + user + '_gaze_info.xlsx'
            xl_path = os.path.join(os.getcwd(), xl_name)

            wb.save(xl_path)
    finally:
        conn.close()
        wb.close()