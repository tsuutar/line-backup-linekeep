import pyautogui
from time import sleep
import os
import tempfile
import pygetwindow as gw
from PIL import Image, ImageEnhance
import pyocr
import random

"""
LINE keepのテキスト文を保存
実行中にテキストを開くと、自動的に日付を取得し保存します。
ファイル名: LINE_日付_<ランダム値>_.txt
プログラムを停止するまで監視し続けます。
"""

# パス定義
TESSERACT_PATH = "C:/Program Files/Tesseract-OCR"
os.environ['PATH'] += os.pathsep + TESSERACT_PATH

#OCRエンジン取得
ocr_tool = pyocr.get_available_tools()[0]
#OCRの設定 ※tesseract_layout=6が精度には重要。デフォルトは3
builder = pyocr.builders.TextBuilder(tesseract_layout=6)

# メイン処理
if __name__ == '__main__':
    while True:
        # LINE-KEEPデスクトップアプリウィンドウを検索
        print('LINE-KEEP テキストウィンドウの検索')
        if len(gw.getWindowsWithTitle('テキスト')) == 0 :
            # print('LINE Keepアプリでテキストを表示していない')
            sleep(0.5)
            continue

        print('--テキスト保存--')
        # テキストウィンドウのアクティブ
        h_wnd = gw.getWindowsWithTitle('テキスト')[0]
        h_wnd.activate()
        win_x, win_y = h_wnd.topleft #left, top
        win_width, win_height = h_wnd.size #width, height

        # 現在のカーソル位置
        cur_position = pyautogui.position()

        # 情報を表示
        pyautogui.moveTo(win_x + 10, win_y + win_height -15)
        pyautogui.click()
        sleep(0.5)

        # 情報の保存時間を取得
        with tempfile.TemporaryDirectory() as tmpdir:
            # (1)キャプチャ
            s = pyautogui.screenshot(region=(win_x + 11, win_y + 133, 58, 15))
            s.save(os.path.join(tmpdir, "temp.png"))
            print(tmpdir)
            # (2)画像加工
            img = Image.open(os.path.join(tmpdir, "temp.png"))
            img = ImageEnhance.Contrast(img).enhance(4.0)
            img.save(os.path.join(tmpdir, "temp2.png")) # デバッグ用
            # (3)OCR
            date_text = ocr_tool.image_to_string(img , lang='eng', builder=builder)
            date_text = date_text.replace(',', '.').replace(' ', '').replace('-', '').replace('*', '').replace(':', '').replace('(', '')
            print(f'保存時間={date_text}')

        # ダウンロードボタン押下、保存、閉じる
        pyautogui.moveTo(win_x + win_width -20, win_y + win_height -20)
        pyautogui.click()
        sleep(0.7)
        random.seed()
        pyautogui.write(f'LINE_{date_text}_{random.randrange(1000, 9999)}_.txt')
        sleep(0.3)
        pyautogui.press("enter")
        sleep(0.3)
        pyautogui.press('esc')

        # カーソル位置を戻す
        pyautogui.moveTo(cur_position)
