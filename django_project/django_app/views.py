from django.shortcuts import render, redirect
from django_app.main import Main
# Create your views here.


def index(request):
    if request.method == 'POST':
        reference = Main(request)

        if (error := reference.is_validate()) == True:
            reference.add_user()
            return render(request, 'index.html')

        else:
            return render(request, 'signup.html', {'has_error': error})

    return render(request, 'index.html')


def signup(request):
    return render(request, 'signup.html')


def homepage(request):
    if request.method == 'POST' and 'signin-button' in request.POST:
        reference = Main(request)

        if (error := reference.is_exist()) == True:
            users = reference.fetch()
            return render(request, 'homepage.html', {'users': users})

        else:
            return render(request, 'index.html', {'has_error': error})

    elif request.method == 'POST' and 'done-edit' in request.POST:
        reference = Main(request)

        if (error := reference.is_validate()) == True:
            user_id = reference.fetch(int(request.POST['row-id']))
            reference.update(request.POST, user_id[0])
            users = reference.fetch()
            return render(request, 'homepage.html', {'users': users})

        else:
            return render(request, 'editpage.html', {'has_error': error, 'row_id': request.POST['row-id']})

    elif request.method == 'POST' and 'delete-button' in request.POST:
        return render(request, 'homepage.html')

    reference = Main(request)
    users = reference.fetch()
    return render(request, 'homepage.html', {'users': users})


def editpage(request):
    if request.method == 'POST' and 'edit-button' in request.POST:
        reference = Main(request)
        _, u_n, mail, addr = reference.fetch(
            int(request.POST['edit-button']))

        return render(request, 'editpage.html', {
            'row_id': request.POST['edit-button'],
            'username': u_n,
            'email': mail,
            'address': addr})

    elif request.method == 'POST' and 'delete-button' in request.POST:
        reference = Main(request)
        user_id = reference.fetch(int(request.POST['delete-button']))
        reference.delete(user_id[0])
        users = reference.fetch()
        return render(request, 'homepage.html', {'users': users})
