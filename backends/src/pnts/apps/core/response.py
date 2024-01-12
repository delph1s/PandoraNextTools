"""
module description:

PandoraNext core response module
"""

from django.http.response import DjangoJSONEncoder, JsonResponse

from rest_framework.response import Response


class CoreDRFJSONEncoder(DjangoJSONEncoder):
    """
    重写DjangoJSONEncoder
    (1) 默认返回支持中文格式的json字符串
    """

    def __init__(
        self,
        *,
        skipkeys=False,
        ensure_ascii=False,
        check_circular=True,
        allow_nan=True,
        sort_keys=False,
        indent=None,
        separators=None,
        default=None
    ):
        super().__init__(
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            default=default,
        )


class SuccessResponse(Response):
    """
    标准响应成功的返回, SuccessResponse(data)
    (1) 默认错误码返回2000, 支持指定其他返回码
    """

    def __init__(
        self,
        data=None,
        msg='success',
        code=2000,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        self.std_data = {
            'code': code,
            'data': data,
            'msg': msg,
            'status': 'success',
        }
        super().__init__(
            self.std_data, status, template_name, headers, exception, content_type
        )

    def __str__(self):
        return str(self.std_data)


class ErrorResponse(Response):
    """
    标准响应错误的返回,ErrorResponse(msg='xxx')
    (1) 默认错误码返回4000, 也可以指定其他返回码:ErrorResponse(code=xxx)
    """

    def __init__(
        self,
        data=None,
        msg='error',
        code=4000,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        self.std_data = {
            'code': code,
            'data': data,
            'msg': msg,
            'status': 'error',
        }
        super().__init__(
            self.std_data, status, template_name, headers, exception, content_type
        )

    def __str__(self):
        return str(self.std_data)


class SuccessJsonResponse(JsonResponse):
    """
    标准JsonResponse, SuccessJsonResponse(data=data)
    (1) 仅SuccessResponse无法使用时才能推荐使用SuccessJsonResponse
    """

    def __init__(
        self,
        data,
        msg='success',
        code=2000,
        encoder=DjangoJSONEncoder,
        safe=True,
        json_dumps_params=None,
        **kwargs
    ):
        std_data = {
            'code': code,
            'data': data,
            'msg': msg,
            'status': 'success',
        }
        super().__init__(std_data, encoder, safe, json_dumps_params, **kwargs)


class ErrorJsonResponse(JsonResponse):
    """
    标准JsonResponse, 仅ErrorResponse无法使用时才能使用ErrorJsonResponse
    (1) 默认错误码返回4000, 也可以指定其他返回码:ErrorJsonResponse(code=xxx)
    """

    def __init__(
        self,
        data,
        msg='error',
        code=4000,
        encoder=CoreDRFJSONEncoder,
        safe=True,
        json_dumps_params=None,
        **kwargs
    ):
        std_data = {
            'code': code,
            'data': data,
            'msg': msg,
            'status': 'error',
        }
        super().__init__(std_data, encoder, safe, json_dumps_params, **kwargs)
