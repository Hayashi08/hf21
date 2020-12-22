import numpy as np
import cv2

from image import MyImage

class Shoulder(object):
    def __init__(self, img):
        self.color_image = img
        self.noback_image = img
        self.gray_image = None
        self.canny_image = None
        self.detect_area = [250, 600, 400, 100]
        self.hough_lines = []

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

    def get_gray_image(self):
        self.gray_image = cv2.cvtColor(self.noback_image, cv2.COLOR_BGR2GRAY)
    
    # canny変換
    def convert_canny_image(self):
        self.canny_image = cv2.Canny(self.gray_image, 200, 200)

    # 確率的ハフ変換
    def hough_lines_p(self):
        self.hough_lines = cv2.HoughLinesP(
            self.canny_image, rho=1, theta=np.pi/360, threshold=50, minLineLength=60, maxLineGap=10
        )
    
    def detect_area_line(self, line):
        x1, y1, x2, y2 = line[0]
        xa = (x2-x1)
        ya = (y2-y1)

        # 画面サイズを取得
        height, width, channels = MyImage.get_size(self.color_image)

        # 長すぎる直線を除く
        if xa > (width/2):
            return "false"
        # 上部の直線を除く
        if y1<self.detect_area[0] or y2<self.detect_area[0]:
            return "false"
        # 右部の直線を除く
        if x1>self.detect_area[1] or x2>self.detect_area[1]:
            return "false"
        # 下部の直線を除く
        if y1>self.detect_area[2] or y2>self.detect_area[2]:
            return "false"
        # 左部の直線を除く
        if x1<self.detect_area[3] or x2<self.detect_area[3]:
            return "false"
        # x方向に短すぎる直線を除く
        if xa < 50:
            return "false"
        return "true"

    # 結果
    def detect(self):
        self.remove_background()
        self.get_gray_image()
        self.convert_canny_image()
        self.hough_lines_p()
        xline = []
        yline = []
        save_path = ""
        # if self.hough_lines:
        for line in self.hough_lines:
            x1, y1, x2, y2 = line[0]
            xa = (x2-x1)
            ya = (y2-y1)
            
            # 描画条件
            is_range = self.detect_area_line(line)
            if is_range=="true":
                cv2.line(self.color_image,(x1,y1),(x2,y2),(0,0,255),2) # 描画

                line = np.append(line, [xa,ya])
                # 負の数を正の数に変換
                if(xa < 0):
                    xa = -xa
                if(ya < 0):
                    ya = -ya
                xline =np.append(xline, xa)
                yline =np.append(yline, ya)
        # 描画後の画像保存
        save_path = MyImage.save(self.color_image)

        if((yline[0]-yline[1] > 10) or (yline[0]-yline[1] < -10)):
            result = '傾むいてます。'
        elif((xline[0]-xline[1] > 10) or (xline[0]-xline[1] < -10)):
            result = '回転してます。'
        else:
            result = 'OK'
        # else:
        #     result = "検出できませんでした"
        return result, save_path