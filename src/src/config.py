#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'qmax'

from PIL import Image
import os



# url for crawlering
ems_singlequery_url = 'http://www.ems.com.cn/ems/order/singleQuery_t'
ems_multiquery_url = 'http://www.ems.com.cn/ems/order/multiQuery_t'
ems_rand_code_url = 'http://www.ems.com.cn/ems/rand.png'
crack_folder = '../codemap'

# code for extracting from html
exp_text_pattern = "(?isu)<ul\s+?class=\"mailnum_result_list_box\"[^>]*>(.*?)</ul>"
exp_li_pattern = "(?isu)<li style=\"cursor: pointer;\"[^>]*>(.*?)</li>"
exp_num_pattern = "(?isu)<span style=\"color:#\w+?\">(.*?)</span>"
exp0_pattern = "(?isu)<table>(.*?)</table>"
exp1_pattern = "(?isu)<tr[^>]*>(.*?)</tr>"
exp2_pattern = "(?isu)<td[^>]*>(.*?)</td>"

# crack
codemask = os.getcwd() + '/codemap/mask1.jpg'
letters_mask = Image.open(codemask)
# conn string
