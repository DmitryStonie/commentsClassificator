import random
import time

from selenium import webdriver
from parsel import Selector


def scroll(driver, limit):
    page_content = driver.page_source
    response = Selector(page_content)
    comments_string = response.xpath('//div[@class = "fontBodySmall" and contains(text(), "Отзывов:")]/text()').get()
    comments_count = int(''.join(x for x in comments_string if x.isdigit()))
    scroll_xpath = '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf "]'
    fBody = driver.find_element("xpath", scroll_xpath)
    scroll = 0
    while scroll < min(limit / 10, comments_count / 10) + 1:
        driver.execute_script('arguments[0].scrollTop = 1e9;', fBody)
        scroll += 1
        time.sleep(0.5)


def get_comments(url, driver):
    driver.get(url)
    scroll(driver, 200)
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


urls = [
    'https://www.google.com/maps/place/%D0%93%D0%B8%D0%BF%D0%B5%D1%80+%D0%9B%D0%B5%D0%BD%D1%82%D0%B0/@54.9407841,82.9195948,16.3z/data=!3m1!5s0x42dfe77a17333a6d:0x66f923e3ae70e232!4m8!3m7!1s0x42dfe76537db0fe3:0xdf6a0568275f916!8m2!3d54.9414588!4d82.9238062!9m1!1b1!16s%2Fg%2F11xhq6wlf?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%9E%D0%92%D0%90%D0%A2/@55.0303131,82.9245177,3a,75y,90t/data=!3m7!1e2!3m5!1sAF1QipM8EFqtkmyhL_5_1M04UIZplCNeE98vbETNLnhJ!2e10!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipM8EFqtkmyhL_5_1M04UIZplCNeE98vbETNLnhJ%3Dw150-h150-k-no-p!7i4096!8i3072!4m8!3m7!1s0x42dfe5d05bd82a23:0x295c8d5c15ad0c39!8m2!3d55.0303131!4d82.9245177!9m1!1b1!16zL20vMGI0ZDBm?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D0%BA%D1%80%D0%B0%D0%B5%D0%B2%D0%B5%D0%B4%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9+%D0%BC%D1%83%D0%B7%D0%B5%D0%B9/@55.0303131,82.9245177,15z/data=!4m8!3m7!1s0x42dfe5d1ab0c096d:0x147a0c66714ffb39!8m2!3d55.0285782!4d82.9203176!9m1!1b1!16s%2Fg%2F122_sk1d?entry=ttu',
    'https://www.google.com/maps/place/%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%D0%BF%D0%B0%D1%80%D0%BA/@55.0303131,82.9245177,15z/data=!4m8!3m7!1s0x42dfe5c572857aaf:0x9acb6ed25a85f5d0!8m2!3d55.0343!4d82.9243006!9m1!1b1!16s%2Fg%2F1237w0sr?entry=ttu',
    'https://www.google.com/maps/place/%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D1%8B%D0%B9+%D0%A4%D0%B0%D0%BA%D0%B5%D0%BB/@55.0265533,82.9027657,15.26z/data=!4m8!3m7!1s0x42dfe42d2eca30e1:0xc61798ce9fd1e419!8m2!3d55.0285243!4d82.9081342!9m1!1b1!16s%2Fg%2F11b81j1yc4?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D1%86%D0%B8%D1%80%D0%BA/@55.0413722,82.8970626,15.52z/data=!4m8!3m7!1s0x42dfe43517d0c82b:0x9c7bcf6600597c37!8m2!3d55.0418167!4d82.909729!9m1!1b1!16s%2Fg%2F122wtxml?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%B7%D0%BE%D0%BE%D0%BF%D0%B0%D1%80%D0%BA+%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8+%D0%A0.%D0%90.+%D0%A8%D0%B8%D0%BB%D0%BE/@55.0597824,82.8958873,14.48z/data=!4m8!3m7!1s0x42dfe450d1f53a87:0xdefd43ae19406923!8m2!3d55.0566252!4d82.8890057!9m1!1b1!16s%2Fg%2F1yjg826nd?entry=ttu',
    'https://www.google.com/maps/place/%D0%9F%D1%80%D1%83%D0%B4+%D1%81+%D1%83%D1%82%D0%BA%D0%B0%D0%BC%D0%B8/@54.8334475,83.096316,14z/data=!4m8!3m7!1s0x42dfc46a0ef2c205:0xbbafaaecf8293dfb!8m2!3d54.8303081!4d83.1028988!9m1!1b1!16s%2Fg%2F11ggvsd7nq?entry=ttu',
    'https://www.google.com/maps/place/%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BD%D0%B0%D0%B1%D0%B5%D1%80%D0%B5%D0%B6%D0%BD%D0%B0%D1%8F/@55.0087982,82.9185406,14.74z/data=!4m8!3m7!1s0x42dfe66b190e2457:0xa548b51c5df76a75!8m2!3d55.0068947!4d82.9351178!9m1!1b1!16s%2Fg%2F12hnxrdyb?entry=ttu',
    'https://www.google.com/maps/place/%D0%9C%D0%B5%D0%B6%D0%B4%D1%83%D0%BD%D0%B0%D1%80%D0%BE%D0%B4%D0%BD%D1%8B%D0%B9+%D0%B0%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82+%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA+(%D0%A2%D0%BE%D0%BB%D0%BC%D0%B0%D1%87%D1%91%D0%B2%D0%BE)/@55.003717,82.6494173,13.44z/data=!4m8!3m7!1s0x42e00965cb2a0325:0x53b2caa591c9542e!8m2!3d55.0113541!4d82.652163!9m1!1b1!16zL20vMDNtNl82?entry=ttu',
    'https://www.google.com/maps/place/%D0%9C%D0%9A%D0%A3+%22%D0%A6%D0%A3%D0%93%D0%90%D0%AD%D0%A2%22/@55.0329894,82.9000533,17z/data=!4m8!3m7!1s0x42dfe4324cb76e6d:0x87a8a0735d2b6f6e!8m2!3d55.0329864!4d82.9026282!9m1!1b1!16s%2Fg%2F11bzs2r296?entry=ttu',
    'https://www.google.com/maps/place/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B0%D1%8F+%D0%9A%D0%BB%D0%B8%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F+%D0%91%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0+%E2%84%96+11/@54.9846787,82.8259621,14.75z/data=!4m8!3m7!1s0x42dfe1227f514815:0xda14278da6e9fa4d!8m2!3d54.9825467!4d82.8245939!9m1!1b1!16s%2Fg%2F1tfkp9cl?entry=ttu',
    'https://www.google.com/maps/place/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B0%D1%8F+%D0%BA%D0%BB%D0%B8%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F+%D0%B1%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0+%E2%84%96+34/@54.9847389,82.8796327,16z/data=!4m8!3m7!1s0x42dfe6dabaaa2b89:0x68f62795291ebf94!8m2!3d54.9833144!4d82.8778167!9m1!1b1!16s%2Fg%2F1tdkw753?entry=ttu',
    'https://www.google.com/maps/place/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6+%D0%BF%D0%B0%D1%80%D0%B8%D0%BA%D0%BC%D0%B0%D1%85%D0%B5%D1%80%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D0%B8%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B0/@54.9776092,82.8685778,16.26z/data=!4m8!3m7!1s0x42dfe6d486633cdb:0x165bcdd4deca93d6!8m2!3d54.9776197!4d82.8657661!9m1!1b1!16s%2Fg%2F1tsjc6lj?entry=ttu',
    'https://www.google.com/maps/place/%D0%93%D0%91%D0%A3%D0%97+%D0%93%D0%94%D0%9A%D0%91+%D0%A1%D0%9C%D0%9F.+%D0%A2%D1%80%D0%B0%D0%B2%D0%BC%D0%BF%D1%83%D0%BD%D0%BA%D1%82/@55.0210061,82.9209549,17.3z/data=!4m8!3m7!1s0x42dfe5d6322bbde5:0x14baa006f07c4fb!8m2!3d55.0211697!4d82.9220761!9m1!1b1!16s%2Fg%2F1th5b3z6?entry=ttu',
    'https://www.google.com/maps/place/%D0%9C%D0%91%D0%9E%D0%A3+%D0%A1%D0%9E%D0%A8+%E2%84%96+41/@54.9288017,82.9193081,17z/data=!3m1!5s0x42dfdd8655329c9f:0x90a76b34ca39fd3c!4m8!3m7!1s0x42dfdd87ac75b3bb:0xf5131599a6712615!8m2!3d54.929048!4d82.923801!9m1!1b1!16s%2Fg%2F1ths7xlk?entry=ttu',
    ]


def get_samples(train_ratio):
    if train_ratio <= 0 or train_ratio >= 1:
        return None
    driver = webdriver.Chrome()
    results = []
    for url in urls:
        results += get_comments(url, driver)

    driver.quit()
    random.shuffle(results)
    train_sample = results[:int(train_ratio * len(results))]
    test_sample = results[int(train_ratio * len(results)):]
    write_results(train_sample, "train_sample")
    write_results(test_sample, "test_sample")


#get_samples(0.7)
