import numpy as np
import cv2

from image import MyImage

class Shoulder(object):
    def __init__(self, img):
        self.color_image = img
        self.noback_image = img
        self.gray_image = None
        self.canny_image = None
        self.detect_area = [350, 619, 430, 133, 380]
        self.hough_lines = []

        self.all_img_path = MyImage.mkdir_all_img()
        MyImage.all_save(img, self.all_img_path, '00')

    def remove_background(self):
        # ゼロの空白画像を作成（imgと同じ寸法)
        marker = np.zeros_like(self.noback_image[:,:,0]).astype(np.int32)

        # 背景部分を１で指定
        # 手動でポイントを一つ一つ指定
        marker[431][133] = 1
        marker[414][134] = 1
        marker[402][136] = 1
        marker[389][140] = 1
        marker[373][147] = 1
        marker[355][160] = 1
        marker[341][175] = 1
        marker[328][194] = 1
        marker[315][228] = 1
        marker[307][253] = 1
        marker[303][278] = 1
        marker[300][294] = 1
        #--------------------ここまで左肩
        #--------------------ここから頭
        marker[273][296] = 1
        marker[235][280] = 1
        marker[202][275] = 1
        marker[168][276] = 1
        marker[146][283] = 1
        marker[110][304] = 1
        marker[84][331] = 1
        marker[74][363] = 1
        marker[71][381] = 1 #頂点
        marker[74][399] = 1
        marker[84][431] = 1
        marker[110][458] = 1
        marker[168][479] = 1
        marker[202][486] = 1
        marker[146][487] = 1
        marker[235][482] = 1
        marker[273][466] = 1
        #-------------------ここまで頭
        #-------------------ここから右肩
        marker[300][468] = 1
        marker[303][484] = 1
        marker[307][509] = 1
        marker[315][524] = 1
        marker[328][558] = 1
        marker[341][577] = 1
        marker[355][592] = 1
        marker[373][605] = 1
        marker[389][612] = 1
        marker[402][616] = 1
        marker[414][618] = 1
        marker[431][619] = 1

        # 切り取りたいパーツを指定
        # 体とマスクと顔を色分けして分かりやすくしてる
        marker[391][456] = 255    # suit
        marker[352][362] = 125    # shirt
        marker[250][378] = 62     # face
        marker[121][378] = 31     # head

        # マークされた画像を生成するアルゴリズム
        marked = cv2.watershed(self.noback_image, marker)

        # 背景を黒にして、白にしたいものは白にする
        marked[marked == 1] = 0
        marked[marked > 1] = 255

        # 5×5ピクセルのカーネルを使用して画像を薄くし、輪郭のディテールを失わないようにする
        kernel = np.ones((5,5),np.uint8)
        dilation = cv2.dilate(marked.astype(np.float32), kernel, iterations = 1)

        # 最初の画像に作成したマスクを適用
        final_img = cv2.bitwise_and(self.noback_image, self.noback_image, mask=dilation.astype(np.uint8))

        # BGR を RGB に変換することで、正確な色で画像を描画
        b, g, r = cv2.split(final_img)
        self.noback_image = cv2.merge([r, g, b])
        MyImage.all_save(self.noback_image, self.all_img_path, '01')

    def get_gray_image(self):
        self.gray_image = cv2.cvtColor(self.noback_image, cv2.COLOR_BGR2GRAY)
        MyImage.all_save(self.gray_image, self.all_img_path, '02')

    # canny変換
    def convert_canny_image(self):
        self.canny_image = cv2.Canny(self.gray_image, 200, 200)
        MyImage.all_save(self.canny_image, self.all_img_path, '03')

    # 確率的ハフ変換
    def hough_lines_p(self):
        self.hough_lines = cv2.HoughLinesP(
            self.canny_image, rho=1, theta=np.pi/360, threshold=50, minLineLength=60, maxLineGap=10
        )
    
    def detect_area_line(self, line):
        x1, y1, x2, y2 = line[0]
        a = (y2-y1)/(x2-x1)
        result1 = "true"

        # 画面サイズを取得
        height, width, channels = MyImage.get_size(self.color_image)

        # 左半分の直線を検知する。
        if x1 < self.detect_area[4] or x2 < self.detect_area[4]:
            result1 = 1
        # 右半分の直線を検知する。
        if x1 > self.detect_area[4] or x2 > self.detect_area[4]:
            result1 = -1
        # 上部の直線を除く
        if y1<self.detect_area[0] or y2<self.detect_area[0]:
            result1 = "false"
        # 右部の直線を除く
        if x1>self.detect_area[1] or x2>self.detect_area[1]:
            result1 = "false"
        # 下部の直線を除く
        if y1>self.detect_area[2] or y2>self.detect_area[2]:
            result1 = "false"
        # 左部の直線を除く
        if x1<self.detect_area[3] or x2<self.detect_area[3]:
            result1 = "false"
        # 左半分の直線を検知する。
        if x1 < self.detect_area[4] or x2 < self.detect_area[4]:
            result1 = 1
        # 傾きの値が大きい直線を排除。
        if a>2 or a<-2:
            result1 = 'false'
        return result1

    # 結果
    def detect(self):
        self.remove_background()
        self.get_gray_image()
        self.convert_canny_image()
        self.hough_lines_p()
        aline = []
        left_flag = 0
        right_flag = 0
        save_path = ""
        while left_flag == 0 or right_flag == 0:
            for line in self.hough_lines:
                x1, y1, x2, y2 = line[0]
                a = (y2-y1)/(x2-x1)
                # 描画条件
                is_range = self.detect_area_line(line)
                if is_range== 1:
                    if left_flag== 0:
                        cv2.line(self.color_image,(x1,y1),(x2,y2),(0,0,255),2) # 描画
                        aline = np.append(aline, a)
                        left_flag = 1
                elif is_range== -1:
                    if right_flag== 0:
                        cv2.line(self.color_image,(x1,y1),(x2,y2),(0,0,255),2) # 描画
                        aline = np.append(aline, a)
                        right_flag = 1

        # 描画後の画像保存
        save_path = MyImage.save(self.color_image)
        MyImage.all_save(self.color_image, self.all_img_path, '04')

        num1 = aline[0]+aline[1]
        num2 = 1-(aline[0]*aline[1])
        flag = 0
        tan = (-num2+np.sqrt(np.power(num2, 2)+np.power(num1, 2)))/num1
        deg = np.rad2deg(np.arctan(tan))
        if(deg>0):
            flag = 1
        else:
            deg = -deg
        
        if(deg > 4):
            if(flag == 0):
                # result = '右に' + str(round(deg, 1)) + '傾いています' + '\n' + str(aline[0]) + '\n' + str(aline[1])
                result = '右に' + str(round(deg)) + '度傾いています'
            else:
                # result = '左に' + str(round(deg, 1)) + '傾いています' + '\n' + str(aline[0]) + '\n' + str(aline[1])
                result = '左に' + str(round(deg)) + '度傾いています'
        else:
            # result = 'OK' + '\n' + str(aline[0]) + '\n' + str(aline[1])
            result = 'OK'
        return result, save_path