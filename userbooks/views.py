from django.shortcuts import render

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def regpage(request):
    return render(request, 'page.html')

def regprocess(request):
    errors = User.objects.basic_validator(request.POST)
    users= User.objects.all()
    for user in users:
        if user.email ==request.POST['email']:
            errors['email']= 'This Email already exist in our database!'
        
    if len(errors) > 0:
        
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')

    else:
        
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        
       
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=firstname, last_name=lastname,  email= email,password=pw_hash) 
        request.session['firstname'] = User.objects.last().first_name
        request.session['userid'] = User.objects.last().id
        
        
        messages.success(request, "Registration successfully completed")
        
        return redirect('/books')

def welcome(request):


    context={
        'books': Book.objects.all(),
        'users': User.objects.all()
    }
    if 'userid'  in request.session and  'firstname'  in request.session:
        return render(request,"bookspage.html",context)
    else:
        return redirect('/')

    


def log(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['firstname'] = logged_user.first_name
            request.session['userid'] = logged_user.id

            messages.success(request, "Login successfully completed")
            return redirect('/books')
        messages.success(request, "Invalid Credintial!")
        return redirect('/')
    messages.success(request, "Invalid Credintial!")
    return redirect('/')



def addbook(request):
    errors = Book.objects.basic_validator(request.POST)
    
    
        
    if len(errors) > 0:
        
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/books')

    else:
        
        title = request.POST['title']
        description = request.POST['desc']
        
        theuser= User.objects.get(id=request.session['userid'])
        Book.objects.create(title=title, description=description,  uploaded_by= theuser) 
        book1= Book.objects.last()
        book1.users_who_like.add(theuser)
        book1.save()

        messages.success(request, "Book was added successfully")
        
        return redirect('/books')


def showbook(request,id):
    context={
        "bookone": Book.objects.get(id=id),
        'users': User.objects.all()
        }

    # book1= Book.objects.get(id=int(id))
   
    # book1.users_who_like.add(author1)
    # book1.save()
    
    return render(request, 'showbook.html', context)


def delbook(request,id):
    book1=Book.objects.get(id=int(id))
    book1.delete()
    return redirect('/books')


def updatebook(request,id):
    bookinstance = Book.objects.get(id=int(id))
    bookinstance.description=request.POST["desc"]
    bookinstance.save()
    return redirect("/books")

def addtofav(request,id):
    userliking= User.objects.get(id=request.session['userid'])
    likedbook=Book.objects.get(id=int(id))
    likedbook.users_who_like.add(userliking)
    likedbook.save()
    return redirect('/books/'+str(id))

def unfav(request,id):
    userunlike= User.objects.get(id=request.session['userid'])
    unlikedbook=Book.objects.get(id=int(id))
    unlikedbook.users_who_like.remove(userunlike)
    unlikedbook.save()
    return redirect('/books/'+str(id))




def logout(request):
    if 'userid' in request.session:
        del request.session['userid']
    if 'firstname' in request.session:
        del request.session['firstname']
    
        
    request.session.flush()
    return redirect('/')
        
        



