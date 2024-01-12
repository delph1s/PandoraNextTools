from django.db import models
from django.db.models import (
    BigAutoField,
    BooleanField,
    CharField,
    DateTimeField,
)


class CoreModel(models.Model):
    id = BigAutoField(primary_key=True, verbose_name="ID", help_text="ID")
    created_time = DateTimeField(
        auto_now=False, auto_now_add=True, verbose_name="创建时间", help_text="创建时间"
    )
    updated_time = DateTimeField(
        auto_now=True, auto_now_add=False, verbose_name="修改时间", help_text="修改时间"
    )
    delete_flag = BooleanField(default=False, verbose_name="删除标志", help_text="删除标志")

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name
