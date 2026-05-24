import time

import pyautogui

# Текст рецензии, полностью соответствующий условиям задания
review_text = (
    "I recently attended an incredible live concert, and it was an unforgettable experience. "
    "My overall impression was purely fantastic; the energy in the stadium was absolutely electric "
    "from the moment the lights went down. The absolute highlight of the event was when the lead "
    "guitarist played a stunning solo during the final song while a massive laser show lit up the "
    "entire arena. The sound quality was perfect, and the band engaged beautifully with the audience. "
    "I highly recommend attending their next performance if you ever get the chance—it is well worth seeing."
)

print("У вас есть 5 секунд, чтобы переключиться на окно браузера и кликнуть в поле ввода...")
time.sleep(5)

print("Начинаю ввод текста...")
# interval=0.05 задает небольшую задержку между нажатиями клавиш для имитации печати
pyautogui.write(review_text, interval=0.05)

print("Ввод успешно завершен!")
