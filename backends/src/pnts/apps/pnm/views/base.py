import httpx
import json

from django.conf import settings
from rest_framework.views import APIView

from apps.core import status
from apps.core.response import (
    SuccessResponse,
    ErrorResponse,
)
from utils.ssh.mgr import SSHManager


class PandoraNextAccountUsageView(APIView):
    def post(self, request):
        request_data = request.data
        if "method" not in request_data:
            request_data["method"] = "api"

        if request_data["method"] == "api":
            try:
                if "proxy" in request_data:
                    ret = httpx.get(
                        "https://dash.pandoranext.com/api/{settings.PANDORA_NEXT_LICENSE_ID}/usage",
                        proxies={
                            "http://": request_data["proxy"],
                            "https://": request_data["proxy"],
                        },
                    )
                else:
                    ret = httpx.get(
                        "https://dash.pandoranext.com/api/{settings.PANDORA_NEXT_LICENSE_ID}/usage"
                    )

                if status.is_success(ret.status_code):
                    return SuccessResponse(
                        {"detail": ret.json()}, code=status.HTTP_2001_GET_DATA_OK
                    )

                return ErrorResponse(
                    {"detail": ret.text},
                    code=status.HTTP_4000_REQUEST_FAIL,
                )
            except Exception as e:
                return ErrorResponse(
                    {"detail": str(e)}, code=status.HTTP_5000_INTERNAL_SERVER_ERROR
                )

        if request_data["method"] == "ssh":
            ssh_mgr = SSHManager(
                hostname=settings.SSH_HOSTNAME,
                port=settings.SSH_PORT,
                username=settings.SSH_USERNAME,
                ssh_key=(settings.SSH_KEY_FILE, settings.SSH_KEY_TYPE),
                password=settings.SSH_PASSWORD,
            )
            cmd_str = f'curl "https://dash.pandoranext.com/api/{settings.PANDORA_NEXT_LICENSE_ID}/usage"'
            try:
                stdout, stderr = (
                    stdr.decode("utf-8") for stdr in ssh_mgr.run_command(cmd_str)
                )
                stdout_json = json.loads(stdout)
                return SuccessResponse(
                    {"data": stdout_json}, code=status.HTTP_2001_GET_DATA_OK
                )
            except Exception as e:
                return ErrorResponse(
                    {"detail": str(e)}, code=status.HTTP_5000_INTERNAL_SERVER_ERROR
                )

        return ErrorResponse(
            {"detail": "`method` 参数配置目前仅支持`api`和`ssh`"},
            code=status.HTTP_5000_INTERNAL_SERVER_ERROR,
        )
