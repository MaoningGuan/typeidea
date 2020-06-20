#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        # max_age设置浏览器中存储的cookie的有效时长，httponly=True设置该cookie只能在服务器端才可以访问
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            # print(request.COOKIES)
            uid = request.COOKIES[USER_KEY]
            # print('已存在的uid:', uid)
        except KeyError:
            # 生成唯一的用户id
            uid = uuid.uuid4().hex
            # print('产生新的uid:', uid)
        return uid
