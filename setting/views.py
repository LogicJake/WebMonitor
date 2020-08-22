from django.shortcuts import render
import os


# Create your views here.
def log_view(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    log_path = os.path.join(BASE_DIR, 'static', 'log', 'log.txt')

    content = '日志文件不存在'
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            content = f.read()

    return render(request, 'log.html', {'content': content})
