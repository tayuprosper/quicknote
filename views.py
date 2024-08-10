from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Note, User
from django.contrib.auth import login, authenticate, logout
from .forms import NoteForm, LoginForm,SignUpForm


#creating class for user form


# Create your views here.
def Home(req):
    return render(req,"index.html")


def Login(req):
    if req.method == "POST":
            user = authenticate(username=req.POST["username"],password=req.POST["password"])
            if user is not None:
                login(req,user)
                return redirect("Notes")
            else: 
                message = "invalid credentials"
                form = AuthenticationForm()
                return render(req,"auth.html",{'form': form, 'message' : message})
    else:  
        form = AuthenticationForm()
        return render(req,"auth.html",{'form': form})


@login_required
def Notes(req):
    notes = Note.objects.filter(owner = req.user).order_by("is_fav").reverse()
    context = {"notes": notes}
    return render(req,"notes.html", context)

@login_required
def Delete(req,note_id):
    if req.method == "POST":
        res = f"delete note with id {note_id}"
        messages.success(req,res)
    else:
        res = "bad request"
        messages.error(req,res)
    return redirect("Home")

@login_required
def Edit(req,note_id):
    if req.method == "GET":
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            messages.error(req,"Oops this note dosen't exits")
            return redirect("Notes")
        if note.owner != req.user:
            messages.error(req,"Bad request")
            return redirect("Notes")
        form = NoteForm(initial={"note_title":note.note_title,"notesContent":note.notesContent})
        return render(req,"editnote.html", {'form': form})
    else:
        
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            message = "OOps somthing went wrong"
            messages.error(req,note)
            return redirect("Notes")
        if req.user == note.owner:
            print(note.owner.id)
            print(req.user.id)
            note.note_title = req.POST["note_title"]
            note.notesContent = req.POST["notesContent"]
            note.save()
            messages.success(req,"Note edited succesfuly")
            return redirect("Notes")
        else:
            messages.error(req,"Bad request")
            return redirect("Notes")




@login_required
def Create(req):
    if req.method == 'POST':
        form = NoteForm(req.POST)
        if form.is_valid():
            note = Note(note_title=req.POST["note_title"],notesContent = req.POST["notesContent"], owner_id = req.user.id)
            note.save()
            return redirect("Notes")
        else:
            messages.error("something went wrong")
            return render(req,"editnote.html", {'form' : form})
    else:
        
        form = NoteForm()
        return render(req,"editnote.html", {'form' : form})
    
def Signup(req):
    if req.method == "POST":
        form = SignUpForm(req.POST)
        print(req.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            user = authenticate(username=req.POST["username"], password1=req.POST["password1"],password2=req.POST["password2"], first_name=req.POST["first_name"],last_name=req.POST["last_name"])
            if user is not None:
                login(user)
                return redirect("Notes")
            else:
                print(form.errors)
                return render(req,"auth.html", {'form': form, "auth_type": 'signup', "message": form.errors})
        else:
           print(form.errors)
           return render(req,"auth.html", {'form': form, "auth_type": 'signup',"message": form.errors})
    else:
        form = SignUpForm()
        return render(req,"auth.html", {'form': form, "auth_type": 'signup'})
    

@login_required
def SetFav(req,note_id):
   if req.method == 'POST':
       note = get_object_or_404(Note,pk=note_id)
       note.is_fav = not note.is_fav
       note.save()
       value = str(note.is_fav)
       print(value)
       return JsonResponse({'is_fav': value})

def Logout(req):
    logout(req)
    return redirect("Home")

@login_required
def ViewNote(req,note_id):
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        messages.error("Unauthorised")
        return redirect("Notes")
    context = {"note": note}
    return render(req,"viewnote.html",context)