# -*- coding: utf-8 -*-
import urllib.request
from urllib.error import URLError
import re
import os
import time
import ssl
context = ssl._create_unverified_context()

def get_attach(url):
    print('try getting url %s' % url)
    headers = {
        'Host': 'bbs.tju.edu.cn',
        'Referer': 'https://bbs.tju.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    req = urllib.request.Request(
        url = url,
        headers = headers
    )

    try:
        file = urllib.request.urlopen(url, context=context)
        disposition = get_disposition(file)
        if re.match(r'''.*(\.png|\.jpg|\.gif|\.bmp|\.mng|\.psd|\.jpeg|\.tiff|\.tif)$|
        (.*"image_android")|
        (.*=filename$)|
        (.*=untitled$)''', disposition, re.IGNORECASE):
            # image
            return False
        else:
            return file

    except URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        return False

def save_file(attachment):
    disposition = get_disposition(attachment)

    fileRegex = re.match(r'(.*filename=)(.*\..*)$', disposition)
    if fileRegex:
        filename = fileRegex.group(2)
    else:
        return False

    filepath = os.path.join(os.path.abspath('.'), 'dump')
    if not filepath:
        os.mkdir(filepath)

    with open(os.path.join(filepath, filename), 'wb') as out_file:
        data = attachment.read()
        out_file.write(data)
    print('attachment got & saved to %s' % filepath)


def logging(logger, id):
    logTime = time.asctime(time.localtime(time.time()))
    logger.write('%s --->>>--- %s \n' % (logTime, str(id)))

def get_disposition(file):
    return file.info().get('Content-Disposition')


if __name__ == "__main__":
    # testing
    for id in range(69900, 70000):
        get_attach('https://bbs.tju.edu.cn/api/attach/%s' % id)
