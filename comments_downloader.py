import time

from selenium import webdriver
from parsel import Selector
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()

url = 'https://www.google.com/maps/place/%D0%9D%D0%93%D0%A3,+%D0%9D%D0%BE%D0%B2%D1%8B%D0%B9+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81/@54.8435927,83.0886072,19z/data=!4m8!3m7!1s0x42dfc5b763e5847b:0x3f0801e65e87519b!8m2!3d54.8429606!4d83.0909893!9m1!1b1!16s%2Fg%2F11glw249cw?entry=ttu'
driver.get(url)

scroll_xpath = '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf "]'
fBody = driver.find_element("xpath", scroll_xpath)
scroll = 0
while scroll < 10:  # this will scroll 3 times
    driver.execute_script('arguments[0].scrollTop = 1e9;', fBody)
    scroll += 1
    time.sleep(0.5)

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

train_sample = open("train_sample.tsv", "w+", encoding="utf-8")
train_sample.write("comment\trating\n")
# print(results[0].get('comment') + "\t" + results[0].get('rating'))
for value in results:
    train_sample.write(value.get('comment') + "\t" + value.get('rating') + "\n", )
train_sample.close()

driver.quit()
