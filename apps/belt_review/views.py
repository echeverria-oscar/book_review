from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User
from .models import Book
from .models import Review
from . models import Author
# Create your views here.
def index(request):

    return render(request, 'belt_review/index.html')

def books(request):
    if 'logged_user' not in request.session:
        return redirect('/')

    review = Review.objects.all().order_by('created_at')

    context = {
        'user' : User.objects.get(id = request.session['logged_user']),
        'reviews' : review
    }

    return render(request, 'belt_review/success.html', context)

def register(request):
    if request.method == "POST":
        form_errors = User.objects.validate(request.POST)

        if len(form_errors) > 0:
            for error in form_errors:
                messages.error(request, error)
        else:
            User.objects.register(request.POST)
            messages.success(request, "You have successfully registered! Please login to continue")

    return redirect('/')

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Not login credentials!")
        else:
           request.session['logged_user'] = user.id
           return redirect('/books')

def logout(request):
    if 'logged_user' in request.session:
        request.session.pop('logged_user')
    return redirect('/')

def addbook(request):
        author = Author.objects.all()

        context = {
            'authors' : author,
        }

        return render(request, "belt_review/addbooks.html", context)

def add(request):
    if request.method == "POST":
        user_id = request.session['logged_user']


        if request.POST['author'] != "":
            user = User.objects.get(id=user_id)
            author = Author.objects.get(id=request.POST['author'])
            book = Book.objects.create(book = request.POST['book'], author = author, user = user_id)
            Review.objects.create(review = request.POST['review'],rating = request.POST['rating'], book = book, user = user_id)

        elif request.POST['add_author'] != "":
            author = Author.objects.create(author = request.POST['add_author'], user_id = user_id,)
            book = Book.objects.create(book = request.POST['book'], author = author, user_id = user_id)
            Review.objects.create(review = request.POST['review'], book = book, rating = request.POST['rating'], user_id = user_id)


    return redirect('bookreview', id=book.id)

def bookreview(request, id):

    book = Book.objects.get(id=id)
    review = Review.objects.filter(book_id=id)
    context = {
    'books': book,
    'reviews': review,
    }

    return render(request, 'belt_review/addreview.html', context)

def user_review(request, id):
    if request.method == "POST":
        user_id = request.session['logged_user']
        book = Book.objects.get(id=id)
        Review.objects.create(review = request.POST['review'], book = book, rating=request.POST['rating'], user_id = user_id)



        return redirect('bookreview', id=book.id)

def profile(request, id):

    review = Review.objects.filter(user_id=id)
    rating = Review.objects.filter(user_id = id)

    if rating > 0:
        rating = len(rating)

    context = {
        'users' : User.objects.get(id = id),
        'reviews' : review,
        'rating' :rating,
    }
    print context

    return render(request, "belt_review/profile.html", context)
