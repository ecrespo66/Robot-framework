import threading
import multiprocessing
from iBott.browser_activities import ChromeBrowser
import time


def gotopage(keyword, index):
    browser = ChromeBrowser()
    browser.open()

    browser.set_window_size(632, 384)
    if index == 0:
        x = 0
        y = 0
    elif index == 1:
        x = 632
        y = 0
    elif index == 2:
        x = 0
        y = 384
    elif index == 3:
        x = 632
        y = 386

    browser.set_window_position(x, y)

    browser.get("http://google.com")

    if browser.element_exists("tag_name", "iframe"):
        iframe = browser.find_element_by_tag_name("iframe")
        browser.switch_to.frame(iframe)
        acceptButton = browser.find_element_by_xpath("//*[contains(text(),'Acepto')]")
        acceptButton.click()
        browser.switch_to.default_content()

        time.sleep(1)

        Xpathelement = "//input[@name='q']"

        # localizar el elemento
        element = browser.find_element_by_xpath(Xpathelement)

        # hacemos click sobre el elemento
        element.click()

        # escribirmos el texto sobre el elemento
        buscar_texto = keyword
        element.send_keys(buscar_texto)
        # presionamos enter sobre el elemento
        browser.enter(element)
        position = 90
        browser.scrolldown(position)

        # localizamos los elementos con la clase "s75CSd"
        related_keywords = browser.find_elements_by_class_name("s75CSd")

        # Itereamos por la lista de elementos para extraer su texto
        for k in related_keywords:
           print(k.text)

        browser.close()

keywords = ['perritos', 'gatitos', 'periquitos', 'caballitos']
index = 0
for keyword in keywords:
    t = threading.Thread(target=gotopage, args=[keyword, index])
    t.start()
    index += 1
