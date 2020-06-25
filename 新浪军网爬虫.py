import requests, json, re, os


def get_url():
    number = eval(input("请输入要爬取的数量："))
    print(type(number))
    response = requests.get(
        "http://api.slide.news.sina.com.cn/interface/api_album.php?activity_size=198_132&size=img&ch_id=8&page=1&num={}&jsoncallback=slideNewsSinaComCnCB&_=1576583537503".format(
            number)).text
    response = response.split("slideNewsSinaComCnCB(")[1].rstrip(")")
    response = json.loads(response)
    response_list = response["data"]
    url_list = []
    for i in response_list:
        url_list.append(i["url"])
    return url_list


def get_image_url():
    details_page_url = get_url()
    count = 1
    for i in details_page_url:
        print("正在访问第{}页".format(count))
        count += 1
        respoonse = requests.get(i)
        respoonse.encoding = "gb2312"
        parse_image_url(respoonse.text)


def parse_image_url(html):
    pattern_obj = re.compile(r'''var slide_data = (.*?)
      var ARTICLE_DATA''')
    result_text = re.findall(pattern_obj, html)[0]
    result_json = json.loads(result_text)["images"]
    for i in result_json:
        title = i["title"].replace(":", "")
        image_url = i["image_url"]
        write_image("http:" + image_url, title)


def write_image(image_url, title):
    os.makedirs("新浪军事/" + title, exist_ok=True)
    with open("新浪军事/" + title + "/" + image_url.split("/")[-1], "wb")as f:
        image_wb = requests.get(image_url).content
        f.write(image_wb)
        f.close()
        print("新浪军事/" + title + "/" + image_url.split("/")[-1], "写入完毕！")


get_image_url()
