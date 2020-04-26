from django.db import models

# Create your models here.

class Message(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    message = models.CharField(max_length=2000, verbose_name="内容")
    name = models.CharField(max_length=50, verbose_name="昵称")
    website = models.URLField(verbose_name="网站")
    email = models.EmailField(verbose_name="邮箱")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    class Meta:
        verbose_name = verbose_name_plural = "留言信息"

    def __str__(self):
        return self.name