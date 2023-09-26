import json

import cv2
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import time
import os

from django.core import serializers

from Camera.settings import MEDIA_ROOT

from django.views.decorators.http import require_http_methods

from .models import Patient

cameraWriter = None  # 视频写入对象
camera = None  # 视频
record = False  # 录屏信号
flag = False
sign = False
video_path = None
temp_name = None  # 传递病人姓名给录像文件
temp_id = None  # 传递病人 ID 给录像文件


def generate_frames():
    global camera, record, flag, cameraWriter, video_path, temp_name, temp_id

    while True:
        if camera is not None:
            success, frame = camera.read()
            if record:
                if flag is False:
                    now = time.strftime("%Y-%m-%d-%H_%M_%S",
                                        time.localtime(time.time()))
                    if sign is True:
                        video_name = "media/" + r"temp.mp4"
                    else:
                        video_name = "media/" + temp_id + r"_" + temp_name + r"_" + now + r".mp4"
                        video_path = os.path.join(MEDIA_ROOT, now + r".mp4")
                    fps = camera.get(5)
                    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),)
                    cameraWriter = cv2.VideoWriter(
                        video_name, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)
                    flag = True
                cameraWriter.write(frame)  # 给新视频添加新帧
            if not success:
                break
            else:
                # 将处理后的帧转换为JPG格式
                ret, frame = cv2.imencode('.jpeg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
        else:
            break


@csrf_exempt
def start_camera(request):
    global camera
    if camera is None:
        camera = cv2.VideoCapture("rtsp://admin:linke2023@192.168.2.102/ch1/sub/av_stream?tcp")
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


@csrf_exempt
def stop_camera(request):
    global camera, record, flag, sign
    if camera is not None:
        camera.release()
        camera = None
    record = False
    flag = False
    sign = False
    return HttpResponse("Camera stopped")


@csrf_exempt
def start_record(request):
    global record
    record = True
    return HttpResponse("Recording started")


@csrf_exempt
def stop_record(request):
    global record, flag, sign
    record = False
    flag = False
    time.sleep(0.1)
    sign = True
    record = True
    time.sleep(0.1)
    record = False
    flag = False
    sign = False
    return HttpResponse("Recording stopped")


@require_http_methods(["GET"])
def save_patient(request):
    global temp_name, temp_id
    response = {}
    try:
        patient_name = request.GET.get("patient_name")
        patient_id = request.GET.get("patient_id")
        if Patient.objects.filter(patientId=patient_id).exists():
            response["respMsg"] = "ID exists"
            response["respCode"] = "999999"
            return JsonResponse(response)
        temp_name = patient_name
        temp_id = patient_id
        # 创建病人对象并保存到数据库
        patient = Patient(patientId=patient_id)
        patient.patientName = patient_name
        patient.save()
        response["respMsg"] = "success"
        response["respCode"] = "000000"
    except Exception as e:
        response["respMsg"] = str(e)
        response["respCode"] = "999999"
    return JsonResponse(response)


@require_http_methods(["GET"])
def inquire_patient(request):
    response = {}
    try:
        patient_name = request.GET.get("patient_name")
        patient = Patient.objects.filter(patientName=patient_name)
        response["list"] = json.loads(serializers.serialize("json", patient))
        response["respMsg"] = "success"
        response["respCode"] = "000000"
    except Exception as e:
        response["respMsg"] = str(e)
        response["respCode"] = "999999"
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_patient(request):
    response = {}
    try:
        patient = Patient.objects.filter()
        response["list"] = json.loads(serializers.serialize("json", patient))
        response["respMsg"] = "success"
        response["respCode"] = "000000"
    except Exception as e:
        response["respMsg"] = str(e)
        response["respCode"] = "999999"
    return JsonResponse(response)


@require_http_methods(["GET"])
def update_patient(request):
    global video_path
    response = {}
    try:
        patient_id = request.GET.get("patient_id")
        # 获取指定的条目
        patient = Patient.objects.get(patientId=patient_id)
        filename = os.path.basename(video_path)
        patient.videoUrl = "/root/autodl-tmp/media" + filename
        #  video_url = request.build_absolute_uri(video_path)
        # 更新相关字段
        #  patient.videoUrl = video_url
        # 更新其他字段

        # 保存更新后的条目
        patient.save()
        response["respMsg"] = "success"
        response["respCode"] = "000000"
    except Patient.DoesNotExist as e:
        response["respMsg"] = str(e)
        response["respCode"] = "999999"
    return JsonResponse(response)


@require_http_methods(["GET"])
def disease_kind(request):
    response = {}
    try:
        patient_disease = request.GET.get("patient_disease")
        patient_id = int(request.GET.get("patient_id"))
        # 获取指定的条目
        patient = Patient.objects.get(patientId=patient_id)
        # 更新相关字段
        patient.diseaseKind = patient_disease
        # 更新其他字段

        # 保存更新后的条目
        patient.save()
        response["respMsg"] = "success"
        response["respCode"] = "000000"
    except Patient.DoesNotExist as e:
        response["respMsg"] = str(e)
        response["respCode"] = "999999"
    return JsonResponse(response)


@require_http_methods(["GET"])
def upload_images(request):
    response = {}
    image_path = MEDIA_ROOT
    try:
        for filename in os.listdir(image_path):
            if filename.endswith(".jpg"):
                image_url = image_path + f'{filename}'  # 需要根据实际情况修改 URL
                base_name, extension = os.path.splitext(filename)
                kind = base_name.split('_')[0]
                patient_id = base_name.split('_')[1]
                patient_name = base_name.split('_')[2]
                try:
                    patient = Patient.objects.get(patientId=patient_id)
                except Patient.DoesNotExist:
                    # 如果条目不存在，则创建一个新条目
                    patient = Patient.objects.create(patientId=patient_id)
                    patient.patientName = patient_name
                if kind == "face":
                    patient.faceUrlSelf = image_url
                else:
                    patient.tongueUrlSelf = image_url
                patient.save()
        response["respMsg"] = "success"
        response["respCode"] = "000000"
    except Exception as e:
        response["respMsg"] = str(e)
        response["respCode"] = "999999"
    return JsonResponse(response)


@require_http_methods(["GET"])
def delete_items(request):
    patient_id = request.GET.get("patient_id")  # 接收前端传递的被选中的条目的ID列表
    response = {}
    try:
        item = Patient.objects.get(patientId=patient_id)
        item.delete()
        response["respMsg"] = "success"
        response["respCode"] = "000000"
    except Patient.DoesNotExist as e:
        response["respMsg"] = str(e)
        response["respCode"] = "999999"
    return JsonResponse(response)
