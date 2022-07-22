import os
import shutil
import time
import zipfile

from PIL import Image
from django import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect
from myapp import models, CNN
from myapp.utils import page


def login(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('user_password')
        user = models.User.objects.filter(user_name=username)

        if request.POST.get('registered'):
            return redirect('/register/')

        if user:
            if user.filter(password=password):
                request.session["info"] = {"id": user[0].id, "username": user[0].user_name,
                                           "usertype": user[0].user_type}
                if user.filter(user_type=1):
                    return redirect('/admin/')
                elif user.filter(user_type=2):
                    return redirect('/customer/detection/')
            else:
                error_msg = '密码错误'
        else:
            error_msg = '用户名不存在'
        return render(request, 'log_in.html', {'error_msg': error_msg})
    elif request.method == 'GET':
        return render(request, 'log_in.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('user_password')
        user = models.User.objects.filter(user_name=username)

        if request.POST.get('login'):
            return redirect('/log_in/')

        if user:
            error_msg = '该用户已存在'
        elif username:
            user = models.User(user_name=username, password=password)
            user.save()
            error_msg = '注册成功,请返回登陆'
        else:
            error_msg = '用户名不能为空'
        return render(request, 'register.html', {'error_msg': error_msg})


def logout(request):
    request.session.clear()
    return redirect("/log_in/")


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['user_name', 'password', 'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs = {"placeholder": filed.label}


def admin(request):
    if request.method == 'GET':
        user_list = models.User.objects.all()
        page_object = page.Page(request, user_list)
        page_form = page_object.page_form
        page_string = page_object.html()
        conetxt = {"page_forms": page_form, "page_string": page_string}
        return render(request, 'admin.html', conetxt)


def admin_edit(request, nid):
    if request.method == 'GET':
        user = models.User.objects.filter(id=nid).first()
        form = UserModelForm(instance=user)
        return render(request, 'admin_edit.html', {'form': form})

    elif request.method == 'POST':
        user = models.User.objects.filter(id=nid).first()
        form = UserModelForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/admin/')
        else:
            return render(request, 'admin_edit.html', {'form': form})


def admin_delete(request):
    nid = request.GET.get('nid')
    models.User.objects.filter(id=nid).delete()
    return redirect('/admin/')


def customer_detection(request):
    if request.method == 'GET':
        return render(request, 'customer_detection.html')
    elif request.method == 'POST':
        if 'files' in request.FILES:
            imgs = request.FILES['files']
            if zipfile.is_zipfile(imgs):
                imgs = zipfile.ZipFile(imgs, 'r')
                pics_path = 'myapp/pics'  # 收到的图片临时存放地址
                shutil.rmtree(pics_path)  # 删除该文件夹
                os.mkdir(pics_path)  # 创建该文件夹
                imgs.extractall(pics_path)  # 将收到的zip文件解压到该文件夹

                start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                info = request.session['info']
                request.session['time'] = start_time
                user_name = info['username']
                form = models.Events(time=start_time, re0=0, re1=0, re2=0, re3=0, re4=0, re5=0, re6=0,
                                     the_user=models.User.objects.get(user_name=user_name))
                form.save()
                pic_names = os.listdir(pics_path)
                re0 = re1 = re2 = re3 = re4 = re5 = re6 = 0
                pic_info = {}
                for pic_name in pic_names:
                    path = os.path.join(pics_path, pic_name)
                    re = CNN.pic(path)
                    pic_info[pic_name] = re
                    if re == 0:
                        re0 += 1
                    elif re == 1:
                        re1 += 1
                    elif re == 2:
                        re2 += 1
                    elif re == 3:
                        re3 += 1
                    elif re == 4:
                        re4 += 1
                    elif re == 5:
                        re5 += 1
                    elif re == 6:
                        re6 += 1
                    form = models.Picture(pic_name=pic_name, result=re,
                                          the_events=models.Events.objects.get(time=start_time))
                    form.save()
                    models.Events.objects.filter(time=start_time).update(re0=re0, re1=re1, re2=re2, re3=re3, re4=re4,
                                                                         re5=re5, re6=re6)
                anw = models.Events.objects.get(time=start_time)
            else:
                err = '请将图片压缩打包'
                return render(request, 'customer_detection.html', {"err": err})
            imgs.close()
            return render(request, 'customer_detection.html', {"anw": anw})


def draw1(request):
    time = request.GET.get('time')
    form = models.Events.objects.get(time=time)
    if form:
        data = [form.re0, form.re1, form.re2, form.re3, form.re4, form.re5, form.re6]
        return JsonResponse({'status': True, 'data': data})


def customer_info(request):
    info = request.session['info']
    user_name = info['username']
    forms = models.Events.objects.filter(the_user=user_name)
    page_object = page.Page(request, forms)
    page_form = page_object.page_form
    page_string = page_object.html()
    conetxt = {"page_forms": page_form, "page_string": page_string}
    return render(request, 'customer_info_1.html', conetxt)


def customer_info_delete(request):
    nid = request.GET.get('nid')
    models.Events.objects.filter(id=nid).delete()
    return redirect('/customer/info/')


def customer_info_2(request):
    time1 = request.GET.get('time')
    if time1:
        forms = models.Picture.objects.filter(the_events=time1)
        request.session['start_time'] = time1
    else:
        time1 = request.session['start_time']
        forms = models.Picture.objects.filter(the_events=time1)
    page_object = page.Page(request, forms)
    page_form = page_object.page_form
    page_string = page_object.html()
    conetxt = {"page_forms": page_form, "page_string": page_string}
    return render(request, 'customer_info_2.html', conetxt)
