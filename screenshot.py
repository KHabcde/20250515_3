import pyautogui

# 座標の設定
left = 1000
top = 50
right = 1150
bottom = 70
# 幅と高さを計算
width = right - left
height = bottom - top

# スクリーンショットの取得と保存
screenshot = pyautogui.screenshot(region=(left, top, width, height))
screenshot.save("screenshot_capture.png")

print("スクリーンショットを保存しました: screenshot_capture.png")

