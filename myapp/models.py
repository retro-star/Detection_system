from django.db import models


# Create your models here.
# 用户表
class User(models.Model):
    user_name = models.CharField(verbose_name='用户名', max_length=10, unique=True)
    password = models.IntegerField(verbose_name='密码')
    user_type = models.IntegerField(verbose_name='用户类型', choices=((1, '管理员'), (2, '普通用户')), default=2)

    def __str__(self):
        return self.user_name


# 检测事件表
class Events(models.Model):
    time = models.DateTimeField(verbose_name='检测时间', unique=True)
    re0 = models.IntegerField(verbose_name='正常数量')
    re1 = models.IntegerField(verbose_name='边瑕疵数量')
    re2 = models.IntegerField(verbose_name='角瑕疵数量')
    re3 = models.IntegerField(verbose_name='白色点瑕疵数量')
    re4 = models.IntegerField(verbose_name='浅色块瑕疵数量')
    re5 = models.IntegerField(verbose_name='深色点瑕疵数量')
    re6 = models.IntegerField(verbose_name='光圈瑕疵数量')
    the_user = models.ForeignKey(to='User', to_field='user_name', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.time)


# 图片表
class Picture(models.Model):
    pic_name = models.CharField(verbose_name='图片名', max_length=50)
    result = models.IntegerField(verbose_name='检测结果', choices=(
        (0, '无瑕疵'), (1, '边异常'), (2, '角异常'), (3, '白色点瑕疵'), (4, '浅色块瑕疵'), (5, '深色点瑕疵'), (6, '光圈瑕疵')), default=0)
    the_events = models.ForeignKey(to='Events', to_field='time', on_delete=models.CASCADE)
