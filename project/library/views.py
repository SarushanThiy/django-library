from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect

from .models import Book
from .forms import NewBookForm, LoanBookForm

# Create your views here.

# books = [
#     {'id': 1, 'title': 'Life, the Universe and Everything', 'author': 'Douglas Adams'},
#     {'id': 2, 'title': 'The Meaning of Liff', 'author': 'Douglas Adams'},
#     {'id': 3, 'title': 'The No. 1 Ladies\' Detective Agency', 'author': 'Alexander McCall Smith'}
# ]



def home(request):
    return render(request, 'home.html')


@login_required
def show(req, id):
    book = get_object_or_404(Book, pk=id)
    # data = {'book':book} 
    # return render(req, 'show.html', data)
    if req.method == 'POST':
        form = LoanBookForm(req.POST)
        if form.is_valid():
            book.owner = req.user
            book.save()
            return redirect("library-show", id = id) 
    else:
        form = LoanBookForm(initial={'owner': req.user})
    data = {
        'book': book,
        'form': form
    } 
    return render(req, "show.html", data)  
        

@login_required
def create(req):
    if req.method == 'POST':
        book = NewBookForm(req.POST)
        if book.is_valid():
            id = book.save().id
            return redirect("library-show", id = id)
    else:
        form = NewBookForm()
    data = {'form': form}
    return render(req, "new.html", data)



def all(req):
    data = {'books': Book.objects.all}
    return render(req, 'books.html', data)

    

def not_found_404(req, exception):
    data={'err': exception}
    return render(req, '404.html', data)

def server_error_500(req):
    return render(req, '500.html')
