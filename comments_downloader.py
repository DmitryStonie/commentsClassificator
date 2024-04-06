import random
import time
from enum import Enum

from selenium import webdriver
from parsel import Selector
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By


class ComType(Enum):
    GOOD = 1
    BAD = 2
    ALL = 3

def scroll(driver, limit):
    page_content = driver.page_source
    response = Selector(page_content)
    comments_string = response.xpath('//div[@class = "fontBodySmall" and contains(text(), "Отзывов:")]/text()').get()
    if comments_string is None:
        return
    comments_count = int(''.join(x for x in comments_string if x.isdigit()))
    scroll_xpath = '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf "]'
    fBody = driver.find_element("xpath", scroll_xpath)
    scroll = 0
    while scroll < min(limit / 10, comments_count / 10) + 1:
        driver.execute_script('arguments[0].scrollTop = 1e9;', fBody)
        scroll += 1
        time.sleep(0.5)
def chooseType(driver, type):
    actions = ActionChains(driver)
    if type == ComType.GOOD:
        time.sleep(0.1)
        driver.find_element(By.XPATH, '//div[@class="fontBodyLarge k5lwKb"]').click()
        time.sleep(0.1)
        actions.send_keys(Keys.ARROW_UP).perform()
        time.sleep(0.1)
        actions.send_keys(Keys.ARROW_UP).perform()
        time.sleep(0.1)
        actions.send_keys(Keys.ENTER).perform()
    elif type == ComType.BAD:
        time.sleep(0.1)
        driver.find_element(By.XPATH, '//div[@class="fontBodyLarge k5lwKb"]').click()
        time.sleep(0.1)
        actions.send_keys(Keys.ARROW_UP).perform()
        time.sleep(0.1)
        actions.send_keys(Keys.ENTER).perform()

def openComments(driver):
    buttons = driver.find_elements(By.XPATH, '//div[@class="MyEned"]//button[@class="w8nwRe kyuRq"]')
    if buttons is None:
        return
    for button in buttons:
        webdriver.ActionChains(driver).move_to_element(button).click(button).perform()



def get_comments(url, driver, comments_to_parse, type):
    driver.get(url)
    chooseType(driver, type)
    scroll(driver, comments_to_parse)
    openComments(driver)

    page_content = driver.page_source
    response = Selector(page_content)
    results = []
    for el in response.xpath('//div[@data-review-id and @jsaction]'):
        comment = el.xpath('.//div[@class="MyEned"]/span/text()').get()
        if comment is not None:
            comment = comment.replace('\n', ' ').replace('\t', ' ')
            rating = int(float(el.xpath('count(.//span[@class="hCCjke vzX5Ic google-symbols NhBTye"])').get()))
            if rating == 4 or rating == 5:
                rating = "1"
            else:
                rating = "0"
            results.append({
                'comment': comment,
                'rating': rating
            })
    return results



def write_results(results, filename):
    train_sample = open(filename + ".tsv", "w+", encoding="utf-8")
    train_sample.write("comment\trating\n")
    for value in results:
        train_sample.write(value.get('comment') + "\t" + value.get('rating') + "\n")
    train_sample.close()


goodPlaces = [
    'https://www.google.com/maps/place/%D0%93%D0%B8%D0%BF%D0%B5%D1%80+%D0%9B%D0%B5%D0%BD%D1%82%D0%B0/@54.9407841,82.9195948,16.3z/data=!3m1!5s0x42dfe77a17333a6d:0x66f923e3ae70e232!4m8!3m7!1s0x42dfe76537db0fe3:0xdf6a0568275f916!8m2!3d54.9414588!4d82.9238062!9m1!1b1!16s%2Fg%2F11xhq6wlf?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%9E%D0%92%D0%90%D0%A2/@55.0303131,82.9245177,3a,75y,90t/data=!3m7!1e2!3m5!1sAF1QipM8EFqtkmyhL_5_1M04UIZplCNeE98vbETNLnhJ!2e10!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipM8EFqtkmyhL_5_1M04UIZplCNeE98vbETNLnhJ%3Dw150-h150-k-no-p!7i4096!8i3072!4m8!3m7!1s0x42dfe5d05bd82a23:0x295c8d5c15ad0c39!8m2!3d55.0303131!4d82.9245177!9m1!1b1!16zL20vMGI0ZDBm?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D0%BA%D1%80%D0%B0%D0%B5%D0%B2%D0%B5%D0%B4%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9+%D0%BC%D1%83%D0%B7%D0%B5%D0%B9/@55.0303131,82.9245177,15z/data=!4m8!3m7!1s0x42dfe5d1ab0c096d:0x147a0c66714ffb39!8m2!3d55.0285782!4d82.9203176!9m1!1b1!16s%2Fg%2F122_sk1d?entry=ttu',
    'https://www.google.com/maps/place/%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%D0%BF%D0%B0%D1%80%D0%BA/@55.0303131,82.9245177,15z/data=!4m8!3m7!1s0x42dfe5c572857aaf:0x9acb6ed25a85f5d0!8m2!3d55.0343!4d82.9243006!9m1!1b1!16s%2Fg%2F1237w0sr?entry=ttu',
    'https://www.google.com/maps/place/%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D1%8B%D0%B9+%D0%A4%D0%B0%D0%BA%D0%B5%D0%BB/@55.0265533,82.9027657,15.26z/data=!4m8!3m7!1s0x42dfe42d2eca30e1:0xc61798ce9fd1e419!8m2!3d55.0285243!4d82.9081342!9m1!1b1!16s%2Fg%2F11b81j1yc4?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D1%86%D0%B8%D1%80%D0%BA/@55.0413722,82.8970626,15.52z/data=!4m8!3m7!1s0x42dfe43517d0c82b:0x9c7bcf6600597c37!8m2!3d55.0418167!4d82.909729!9m1!1b1!16s%2Fg%2F122wtxml?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%B7%D0%BE%D0%BE%D0%BF%D0%B0%D1%80%D0%BA+%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8+%D0%A0.%D0%90.+%D0%A8%D0%B8%D0%BB%D0%BE/@55.0597824,82.8958873,14.48z/data=!4m8!3m7!1s0x42dfe450d1f53a87:0xdefd43ae19406923!8m2!3d55.0566252!4d82.8890057!9m1!1b1!16s%2Fg%2F1yjg826nd?entry=ttu',
    'https://www.google.com/maps/place/%D0%9F%D1%80%D1%83%D0%B4+%D1%81+%D1%83%D1%82%D0%BA%D0%B0%D0%BC%D0%B8/@54.8334475,83.096316,14z/data=!4m8!3m7!1s0x42dfc46a0ef2c205:0xbbafaaecf8293dfb!8m2!3d54.8303081!4d83.1028988!9m1!1b1!16s%2Fg%2F11ggvsd7nq?entry=ttu',
    'https://www.google.com/maps/place/%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BD%D0%B0%D0%B1%D0%B5%D1%80%D0%B5%D0%B6%D0%BD%D0%B0%D1%8F/@55.0087982,82.9185406,14.74z/data=!4m8!3m7!1s0x42dfe66b190e2457:0xa548b51c5df76a75!8m2!3d55.0068947!4d82.9351178!9m1!1b1!16s%2Fg%2F12hnxrdyb?entry=ttu',
    'https://www.google.com/maps/place/%D0%9C%D0%B5%D0%B6%D0%B4%D1%83%D0%BD%D0%B0%D1%80%D0%BE%D0%B4%D0%BD%D1%8B%D0%B9+%D0%B0%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82+%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA+(%D0%A2%D0%BE%D0%BB%D0%BC%D0%B0%D1%87%D1%91%D0%B2%D0%BE)/@55.003717,82.6494173,13.44z/data=!4m8!3m7!1s0x42e00965cb2a0325:0x53b2caa591c9542e!8m2!3d55.0113541!4d82.652163!9m1!1b1!16zL20vMDNtNl82?entry=ttu'
    ]
badPlaces = [
    'https://www.google.com/maps/place/%D0%9C%D0%9A%D0%A3+%22%D0%A6%D0%A3%D0%93%D0%90%D0%AD%D0%A2%22/@55.0329894,82.9000533,17z/data=!4m8!3m7!1s0x42dfe4324cb76e6d:0x87a8a0735d2b6f6e!8m2!3d55.0329864!4d82.9026282!9m1!1b1!16s%2Fg%2F11bzs2r296?entry=ttu',
    'https://www.google.com/maps/place/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B0%D1%8F+%D0%9A%D0%BB%D0%B8%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F+%D0%91%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0+%E2%84%96+11/@54.9846787,82.8259621,14.75z/data=!4m8!3m7!1s0x42dfe1227f514815:0xda14278da6e9fa4d!8m2!3d54.9825467!4d82.8245939!9m1!1b1!16s%2Fg%2F1tfkp9cl?entry=ttu',
    'https://www.google.com/maps/place/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B0%D1%8F+%D0%BA%D0%BB%D0%B8%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F+%D0%B1%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0+%E2%84%96+34/@54.9847389,82.8796327,16z/data=!4m8!3m7!1s0x42dfe6dabaaa2b89:0x68f62795291ebf94!8m2!3d54.9833144!4d82.8778167!9m1!1b1!16s%2Fg%2F1tdkw753?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6+%D0%BF%D0%B0%D1%80%D0%B8%D0%BA%D0%BC%D0%B0%D1%85%D0%B5%D1%80%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D0%B8%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B0/@54.9776092,82.8685778,16.26z/data=!4m8!3m7!1s0x42dfe6d486633cdb:0x165bcdd4deca93d6!8m2!3d54.9776197!4d82.8657661!9m1!1b1!16s%2Fg%2F1tsjc6lj?entry=ttu',
    'https://www.google.com/maps/place/%D0%93%D0%91%D0%A3%D0%97+%D0%93%D0%94%D0%9A%D0%91+%D0%A1%D0%9C%D0%9F.+%D0%A2%D1%80%D0%B0%D0%B2%D0%BC%D0%BF%D1%83%D0%BD%D0%BA%D1%82/@55.0210061,82.9209549,17.3z/data=!4m8!3m7!1s0x42dfe5d6322bbde5:0x14baa006f07c4fb!8m2!3d55.0211697!4d82.9220761!9m1!1b1!16s%2Fg%2F1th5b3z6?entry=ttu',
    'https://www.google.com/maps/place/%D0%9C%D0%91%D0%9E%D0%A3+%D0%A1%D0%9E%D0%A8+%E2%84%96+41/@54.9288017,82.9193081,17z/data=!3m1!5s0x42dfdd8655329c9f:0x90a76b34ca39fd3c!4m8!3m7!1s0x42dfdd87ac75b3bb:0xf5131599a6712615!8m2!3d54.929048!4d82.923801!9m1!1b1!16s%2Fg%2F1ths7xlk?entry=ttu',
    'https://www.google.com/maps/place/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B0%D1%8F+%D0%91%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0+%E2%84%96+3/@54.8532355,82.9799551,14.62z/data=!4m8!3m7!1s0x42dfdc830e4c5857:0xafa0fb79bf4c483f!8m2!3d54.8482321!4d82.968208!9m1!1b1!16s%2Fg%2F1tdh6_qz?entry=ttu',
    'https://www.google.com/maps/place/%D0%A8%D0%BA%D0%BE%D0%BB%D0%B0+%E2%84%96+165/@54.8584088,82.9709187,15.52z/data=!4m8!3m7!1s0x42dfdc8b187a7319:0x2c5bb5a2d82315dc!8m2!3d54.8633549!4d82.9669114!9m1!1b1!16s%2Fg%2F1tgllg6x?entry=ttu',
    'https://www.google.com/maps/place/%D0%A8%D0%BA%D0%BE%D0%BB%D0%B0+%E2%84%96+179/@54.8649727,82.9836369,15.52z/data=!4m8!3m7!1s0x42dfdcbe843210d7:0x424b4efdcab95414!8m2!3d54.8641736!4d82.9866159!9m1!1b1!16s%2Fg%2F1tfsljx7?entry=ttu',
    'https://www.google.com/maps/place/%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F+%D0%BF%D0%BE+%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%D1%81%D0%B0%D0%BC+%D0%BC%D0%B8%D0%B3%D1%80%D0%B0%D1%86%D0%B8%D0%B8+%D0%93%D0%A3+%D0%9C%D0%92%D0%94+%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8+%D0%BF%D0%BE+%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%BE%D0%B9+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8/@55.0512517,82.9622634,16.78z/data=!4m8!3m7!1s0x42dfef61f8eef095:0xee792693e50bcbd3!8m2!3d55.0504588!4d82.9645273!9m1!1b1!16s%2Fg%2F11bzyn5hvf?entry=ttu',
    'https://www.google.com/maps/place/%D0%9F%D0%BE%D0%BB%D0%B8%D0%BA%D0%BB%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0+%E2%84%96+2/@55.0322832,83.012984,18z/data=!4m16!1m7!3m6!1s0x42dfef31e1c4b577:0x2ac5c65e811a4402!2z0J_QvtC70LjQutC70LjQvdC40LrQsCDihJYgMg!8m2!3d55.0322822!4d83.0137838!16s%2Fg%2F1tg6npdf!3m7!1s0x42dfef31e1c4b577:0x2ac5c65e811a4402!8m2!3d55.0322822!4d83.0137838!9m1!1b1!16s%2Fg%2F1tg6npdf?entry=ttu',
    'https://www.google.com/maps/place/%D0%9F%D0%BE%D0%BB%D0%B8%D0%BA%D0%BB%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0+%E2%84%96+13/@54.9476106,82.954443,17z/data=!4m8!3m7!1s0x42dfe792fe01f627:0x1bdae4cc6568e23a!8m2!3d54.9476075!4d82.9570179!9m1!1b1!16s%2Fg%2F11fkmz35c1?entry=ttu',
    'https://www.google.com/maps/place/%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5+%D0%9F%D0%B5%D0%BD%D1%81%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE+%D1%84%D0%BE%D0%BD%D0%B4%D0%B0+%D0%A0%D0%A4+%D0%B2+%D0%9A%D0%B8%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%BC+%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%D0%B5/@54.9606419,82.822811,12z/data=!4m12!1m2!2m1!1z0J_QtdC90YHQuNC-0L3QvdGL0Lkg0KTQvtC90LQ!3m8!1s0x42dfe75cffffffff:0x39a00c85a3a7d948!8m2!3d54.9956266!4d82.8686608!9m1!1b1!15sCh3Qn9C10L3RgdC40L7QvdC90YvQuSDQpNC-0L3QtCIDiAEBkgEWc29jaWFsX3NlY3VyaXR5X29mZmljZeABAA!16s%2Fg%2F11mq5sk_j7?entry=ttu',
    'https://www.google.com/maps/place/NSUNet,+%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82-%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80+%D0%9D%D0%93%D0%A3/@54.8434985,83.0892107,19z/data=!4m18!1m9!3m8!1s0x42dfc5b763e5847b:0x3f0801e65e87519b!2z0J3Qk9CjLCDQndC-0LLRi9C5INC60L7RgNC_0YPRgQ!8m2!3d54.8429606!4d83.0909893!9m1!1b1!16s%2Fg%2F11glw249cw!3m7!1s0x42dfc47ab92b75f3:0x7b78835655938b2c!8m2!3d54.8435401!4d83.0887182!9m1!1b1!16s%2Fg%2F11fzf8xqkh?entry=ttu',
    'https://www.google.com/maps/place/%D0%A0%D0%BE%D1%81%D1%82%D0%B5%D0%BB%D0%B5%D0%BA%D0%BE%D0%BC/@54.984644,82.9068268,20.75z/data=!4m8!3m7!1s0x42dfe6fac58a8a05:0x233fb0dad577d40a!8m2!3d54.9846355!4d82.9070287!9m1!1b1!16s%2Fg%2F1pp2x96k0?entry=ttu',
    'https://www.google.com/maps/place/%D0%A0%D0%BE%D1%81%D1%82%D0%B5%D0%BB%D0%B5%D0%BA%D0%BE%D0%BC/@54.9650231,83.1187954,20.75z/data=!4m8!3m7!1s0x42dfeb3ea14220a9:0xfdbfb224593fbd9f!8m2!3d54.9648704!4d83.1188201!9m1!1b1!16s%2Fg%2F11gn26gbvz?entry=ttu',
    'https://www.google.com/maps/place/%D0%A0%D0%BE%D1%81%D1%82%D0%B5%D0%BB%D0%B5%D0%BA%D0%BE%D0%BC/@54.7601279,83.1049264,19.5z/data=!4m8!3m7!1s0x42dfcf7ea8fb1717:0x3e5206d140c5655f!8m2!3d54.7602372!4d83.1054837!9m1!1b1!16s%2Fg%2F11d_z8pt1s?entry=ttu',
    'https://www.google.com/maps/place/%D0%AD%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D1%8B%D0%B9+%D0%B3%D0%BE%D1%80%D0%BE%D0%B4/@55.0412608,82.9128352,18.25z/data=!4m8!3m7!1s0x42dfe50263930757:0xb4c2461c1397d29d!8m2!3d55.041197!4d82.913703!9m1!1b1!16s%2Fg%2F11mw08vzcr?entry=ttu',
    'https://www.google.com/maps/place/%D0%A1%D0%B0%D0%BB%D0%BE%D0%BD-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD+%D0%9C%D0%A2%D0%A1/@55.029767,82.9182806,18.5z/data=!4m8!3m7!1s0x42dfe5d1b7880053:0xa8995b2aa68784ca!8m2!3d55.029661!4d82.918721!9m1!1b1!16s%2Fg%2F1q6b84f0j?entry=ttu',
    'https://www.google.com/maps/place/%D0%A1%D0%B0%D0%BB%D0%BE%D0%BD-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD+%D0%9C%D0%A2%D0%A1/@55.037432,82.9783208,19z/data=!4m8!3m7!1s0x42dfef5b00e4d851:0x80b8cbf6707a7711!8m2!3d55.037712!4d82.978431!9m1!1b1!16s%2Fg%2F1ydpv9j7j?entry=ttu',
    'https://www.google.com/maps/place/%D0%A2%D0%A2%D0%9A-%D0%97%D0%B0%D0%BF%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F+%D0%A1%D0%B8%D0%B1%D0%B8%D1%80%D1%8C/@55.0309641,82.8995412,20z/data=!4m8!3m7!1s0x42dfe5ce55555555:0x45de793e1ff385c6!8m2!3d55.030962!4d82.899991!9m1!1b1!16s%2Fg%2F1hc5wxhdp?entry=ttu',
    'https://www.google.com/maps/place/%D0%AD%D0%BA%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F-%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA/@55.0243436,82.9202546,19.75z/data=!4m8!3m7!1s0x42dfe549a0a7d7b1:0x81b7e6c25bddfdf7!8m2!3d55.0244068!4d82.9202877!9m1!1b1!16s%2Fg%2F11hzhqjztb?entry=ttu',
    'https://www.google.com/maps/place/%D0%9F%D0%90%D0%A2%D0%9F+%E2%84%96+4/@54.9357318,83.1310712,18.5z/data=!4m8!3m7!1s0x42dfc1e4fc80edb5:0x54129597669b5224!8m2!3d54.9357!4d83.131399!9m1!1b1!16s%2Fg%2F11gzztyxp?entry=ttu',
    'https://www.google.com/maps/place/%D0%93%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F+%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F+%D0%9A%D0%BB%D0%B8%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F+%D0%9F%D1%81%D0%B8%D1%85%D0%B8%D0%B0%D1%82%D1%80%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F+%D0%91%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0+%E2%84%96+3/@55.0681298,83.0599566,16.54z/data=!4m8!3m7!1s0x42dfee88ec19cc55:0xed83b39abb040172!8m2!3d55.0677039!4d83.0606394!9m1!1b1!16s%2Fg%2F1tfphc9h?entry=ttu',
]
urls = goodPlaces + badPlaces


def get_samples(num_of_comments, train_ratio):
    if train_ratio < 0 or train_ratio > 1:
        return None
    driver = webdriver.Chrome()
    results = []
    good_comments_to_parse = num_of_comments / 2
    bad_comments_to_parse = num_of_comments - good_comments_to_parse
    for url in urls:
        results += get_comments(url, driver, good_comments_to_parse, ComType.GOOD)
        good_comments_to_parse = num_of_comments / 2 - len(results)
        if good_comments_to_parse <= 0:
            if good_comments_to_parse < 0:
                results = results[:int(num_of_comments / 2)]
            break
    for url in urls:
        results += get_comments(url, driver, bad_comments_to_parse, ComType.BAD)
        bad_comments_to_parse = num_of_comments - len(results)
        if bad_comments_to_parse <= 0:
            if bad_comments_to_parse < 0:
                results = results[:num_of_comments]
            break
    driver.quit()
    random.shuffle(results)
    train_sample = results[:int(train_ratio * len(results))]
    test_sample = results[int(train_ratio * len(results)):]
    write_results(train_sample, "train_sample")
    write_results(test_sample, "test_sample")



get_samples(2000, 0.75)