from django.db import models
import uuid
from django.utils import timezone


class Patient(models.Model):
    objects = models.Manager()
    patientId = models.CharField(max_length=100, primary_key=True, verbose_name="病历ID")
    patientName = models.CharField(max_length=100, verbose_name="姓名")
    diseaseKind = models.CharField(max_length=100, verbose_name="病种", default="")
    videoUrl = models.URLField(verbose_name="视频url")
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    faceUrlSelf = models.URLField(verbose_name="面象照片url", default="")
    faceUrlStd = models.URLField(verbose_name="基准面象照片url", default="")
    tongueUrlSelf = models.URLField(verbose_name="舌象照片url", default="")
    tongueUrlStd = models.URLField(verbose_name="基准舌象照片url", default="")

    def __unicode__(self):
        return self.patientName

    def __str__(self):
        return self.patientName
