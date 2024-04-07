import random
import time
from enum import Enum
from places import theaters

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
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//div[@class="fontBodyLarge k5lwKb"]').click()
        time.sleep(0.1)
        actions.send_keys(Keys.ARROW_UP).perform()
        time.sleep(0.1)
        actions.send_keys(Keys.ARROW_UP).perform()
        time.sleep(0.1)
        actions.send_keys(Keys.ENTER).perform()
    elif type == ComType.BAD:
        time.sleep(0.5)
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
            if (type == ComType.GOOD and rating == "1") or (type == ComType.BAD and rating == "0"):
                results.append({'comment': comment, 'rating': rating})
    return results



def write_results(results, filename):
    train_sample = open(filename + ".tsv", "w+", encoding="utf-8")
    train_sample.write("comment\trating\n")
    for value in results:
        train_sample.write(value.get('comment') + "\t" + value.get('rating') + "\n")
    train_sample.close()



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


urls = [*theaters.values()]
get_samples(2000, 0.75)