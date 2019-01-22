# -*- coding: utf-8 -*-
import urllib.request
import os

class XiaohuaPicturePipeline(object):
    def process_item(self, item, spider):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        req = urllib.request.Request(url=item['addr'],headers=headers)
        res = urllib.request.urlopen(req)
        file_name = os.path.join(r'F:\xiaohua-pictures',item['name']+'.jpg')
        with open(file_name,'wb') as fp:
            fp.write(res.read())
