import requests
from requests.exceptions import RequestException
import json
import time
import hmac
from hashlib import sha256
from urllib.parse import urlencode
from logging import getLogger
from .exception import APIError


class API(object):
    """
    HTTP APIのラッパークラス

    https://lightning.bitflyer.com/docs#http-api
    """

    def __init__(self, mode='Public', product_code='BTC_JPY', config='config.json'):
        self.logger = getLogger(__name__)
        self.url = 'https://api.bitflyer.com'
        self.mode = mode
        self.product_code = product_code
        self.config = config
        self.key = None
        self.secret = None

        self.logger.info(f'HTTP {self.mode} API')
        if self.mode != 'Public' and self.mode != 'Private':
            raise APIError(f'{self.mode} is not defined.')

        if self.mode == 'Private':
            f = json.load(open(self.config, 'r'))
            self.key = f['Key']
            self.secret = f['Secret']

    def _make_sign(self, text):
        """
        HMAC-SHA256 署名
        """
        sign = hmac.new(str.encode(self.secret), str.encode(text), sha256)
        return sign.hexdigest()

    def _make_header(self, method, path, body):
        """
        HTTP リクエストヘッダ
        """
        timestamp = str(time.time())
        text = timestamp + method + path + body

        return {
            'ACCESS-KEY': self.key,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': self._make_sign(text),
            'Content-Type': 'application/json'
        }

    def _request(self, path, method='GET', params=None):
        """
        HTTP リクエスト
        """
        url = self.url + path
        body = ''
        headers = None

        if method == 'GET':
            if params:
                url += '?' + urlencode(params)
        else:
            body = json.dumps(params)
        self.logger.debug(f'Request: {method} {url} {body}')

        if self.mode == 'Private':
            headers = self._make_header(method, path, body)

        try:
            with requests.Session() as s:
                if headers:
                    s.headers.update(headers)
                if method == 'GET':
                    response = s.get(url, headers=headers)
                else:
                    response = s.post(url, data=body, headers=headers)
                response.raise_for_status()
        except RequestException as e:
            raise APIError(e)

        response.encoding = 'utf-8'
        http_response = response.text
        json_response = None
        if len(http_response) > 0:
            json_response = json.loads(http_response)
        return json_response

    def markets(self):
        """
        マーケットの一覧
        """
        path = '/v1/getmarkets'
        return self._request(path)

    def board(self):
        """
        板情報
        """
        path = '/v1/getboard'
        params = {'product_code': self.product_code}
        return self._request(path, params=params)

    def ticker(self):
        """
        Ticker
        """
        path = '/v1/getticker'
        params = {'product_code': self.product_code}
        return self._request(path, params=params)

    def executions(self, count=100, before=None, after=None):
        """
        約定履歴
        """
        path = '/v1/getexecutions'
        params = {
            'product_code': self.product_code,
            'count': count
        }
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        return self._request(path, params=params)

    def boardstate(self):
        """
        板の状態
        """
        path = '/v1/getboardstate'
        params = {'product_code': self.product_code}
        return self._request(path, params=params)

    def health(self):
        """
        取引所の状態
        """
        path = '/v1/gethealth'
        params = {'product_code': self.product_code}
        return self._request(path, params=params)

    def permissions(self):
        """
        API キーの権限を取得
        """
        if self.mode != 'Private':
            raise APIError('This API can only be used in private mode')

        path = '/v1/me/getpermissions'
        return self._request(path)

    def balance(self):
        """
        資産残高を取得
        """
        if self.mode != 'Private':
            raise APIError('This API can only be used in private mode')

        path = '/v1/me/getbalance'
        return self._request(path)

    def send_childorder(self, child_order_type, size, side='BUY', price=None, minute_to_expire=43200, time_in_force='GTC'):
        """
        新規注文を出す
        """
        if self.mode != 'Private':
            raise APIError('This API can only be used in private mode')

        path = '/v1/me/sendchildorder'
        params = {
            'product_code': self.product_code,
            'child_order_type': child_order_type,
            'side': side,
            'size': size,
            'minute_to_expire': minute_to_expire,
            'time_in_force': time_in_force
        }
        if child_order_type == 'LIMIT':
            params['price'] = price
        return self._request(path, method='POST', params=params)

    def cancel_childorder(self, child_order_id=None, child_order_acceptance_id=None):
        """
        注文をキャンセルする
        """
        if self.mode != 'Private':
            raise APIError('This API can only be used in private mode')

        path = '/v1/me/cancelchildorder'
        if child_order_id is None and child_order_acceptance_id is None:
            raise ValueError("Required!: 'child_order_id' or 'child_order_acceptance_id'")
        if child_order_id is not None:
            params = {
                'product_code': self.product_code,
                'child_order_id': child_order_id
            }
        if child_order_acceptance_id is not None:
            params = {
                'product_code': self.product_code,
                'child_order_id': child_order_id
            }
        return self._request(path, method='POST', params=params)

    def cancel_all_childorders(self):
        """
        すべての注文をキャンセルする
        """
        if self.mode != 'Private':
            raise APIError('This API can only be used in private mode')

        path = '/v1/me/cancelallchildorders'
        params = {'product_code': self.product_code}
        return self._request(path, method='POST', params=params)

    def childorders_list(self):
        """
        注文の一覧を取得
        """
        if self.mode != 'Private':
            raise APIError('This API can only be used in private mode')

        path = '/v1/me/getchildorders'
        return self._request(path)

    def executions_list(self):
        """
        約定の一覧を取得
        """
        if self.mode != 'Private':
            raise APIError('This API can only be used in private mode')

        path = '/v1/me/getexecutions'
        return self._request(path)
