from django.shortcuts import render
from .models import Post


posts = [
    {
        'title': 'Why Python is my language of choice?',
        'author': 'Lipu',
        'date_posted': '20th Jan 2019',
        'content': '''python3 -m django --version
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
python3 manage.py shell 
'''
    },
    {
        'title': 'Django is the best!',
        'author': 'Kunu',
        'date_posted': '21th Jan 2019',
        'content': 'This is my second blog ever. I had to make it content-licious'
    },
    {
        'title': 'Blockchain: The next big thing after Internet',
        'author': 'Jaan',
        'date_posted': '21th Jan 2019',
        'content': 'This is my second blog ever. I had to make it content-licious'
    }
]


def home(request):
    content = {'posts': Post.objects.all(),
               'title': 'Home'}
    return render(request, 'blog/home.html', content)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
