from django.shortcuts import render
from django.views.generic import View,TemplateView
from django.http import JsonResponse
from django.http import HttpResponse
from . import forms
from .models import Message
# Create your views here.
import json


class MessageView(View):
    def get(self, request):
        return render(request, 'blog/block.html', {"foo": "message", })

class AddMessageView(TemplateView):
    def post(self,request):
        # 通过ajax提交留言
        message_form = forms.MessageForm(request.POST)
        if message_form.is_valid():
            name = request.POST.get("name")
            website = request.POST.get("website")
            email = request.POST.get("email")
            message = request.POST.get("message")
            message_model = Message()

            message_model.name = name
            message_model.website = website
            message_model.email = email
            message_model.message = message
            message_model.save()
            return JsonResponse({"status": "success"})
        else:
            error_dict = message_form.errors
            error_str = json.dumps(error_dict)
            error_dict = json.loads(error_str)
            return JsonResponse({"status": "fail", 'message': error_dict})

# 全局 400 错误页面
def handler_400_error(request, exception, template_name='404.html'):
    from django.shortcuts import render_to_response
    response = render_to_response('blog/404.html')
    response.status_code = 400
    return response


# 全局 403 错误页面
def handler_403_error(request, exception, template_name='404.html'):
    from django.shortcuts import render_to_response
    response = render_to_response('blog/404.html')
    response.status_code = 403
    return response


# 全局 404 错误页面
def handler_404_error(request, exception, template_name='404.html'):
    from django.shortcuts import render_to_response
    response = render_to_response('blog/404.html')
    response.status_code = 404
    return response


# 全局 500 错误页面， 这里注意，参数同其他3个的不一样，不需要 exception
def handler_500_error(request, template_name='404.html'):
    from django.shortcuts import render_to_response
    response = render_to_response('blog/404.html')
    response.status_code = 500
    return response
