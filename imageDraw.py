from PIL import Image, ImageFont, ImageDraw
from sqlite3 import connect
from conf import DB_NAME
from db_create import DBHelper

db = DBHelper(DB_NAME)


def create_pic(data_img):
    for i in range(len(data_img)):
        my_image = Image.open("images/root.jpg")
        date_font = ImageFont.truetype('images/PlayfairDisplay-VariableFont_wght.ttf', 35)
        font1 = ImageFont.truetype('images/PlayfairDisplay-VariableFont_wght.ttf', 60)
        regionic = db.get_region(data_img[i][4])
        region_pic = f"{regionic['regions'].upper()} VAQTI"
        year, month, day = str(data_img[i][1]).split('-')
        if month == "04":
            month_str = "aprel"
        else:
            month_str = "may"
        date_pic = f"{day}-{month_str}"
        image_editable = ImageDraw.Draw(my_image)
        image_editable.text((445, 268), date_pic, (255, 255, 255), font=date_font)
        image_editable.text((300, 130), region_pic, (0, 0, 0), font=font1)
        image_editable.text((720, 360), data_img[i][2][:4], (244, 13, 11), font=font1)
        image_editable.text((720, 504), data_img[i][3][:5], (17, 160, 91), font=font1)

        my_image.save(f"images/{data_img[i][0]}.jpg")


def create_month_pic(fajmagh):
    for i in range(0, len(data_pic), 30):
        my_image = Image.open("images/table/region_root.png")
        region_font = ImageFont.truetype('images/PlayfairDisplay-VariableFont_wght.ttf', 50)
        fajmagh_font = ImageFont.truetype('images/PlayfairDisplay-VariableFont_wght.ttf', 24)
        regionic = db.get_region(fajmagh[i+1][4])
        region_pic = f"{regionic['regions'].upper()} VAQTI"
        print(region_pic)

        for j in range(30):
            fajr1 = fajmagh[j+i][2]
            maghrib1 = fajmagh[j+i][3]
            image_editable = ImageDraw.Draw(my_image)
            image_editable.text((315, 100), region_pic, (0, 0, 0), font=region_font)
            y_cord = 236 + (j * 49)
            image_editable.text((695, y_cord), fajr1[:4], (0, 0, 0), font=fajmagh_font)
            image_editable.text((890, y_cord), maghrib1[:5], (0, 0, 0), font=fajmagh_font)

            my_image.save(f"images/table/region_{fajmagh[i+1][4]}.png")


if __name__ == "__main__":
    with connect("taqvim.db") as datas:
        cur = datas.cursor()
        cur.execute(
            """
            SELECT * FROM ram_cal
            """
        )
        data_pic = cur.fetchall()
        create_pic(data_pic)
        create_month_pic(data_pic)
