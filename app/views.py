from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Profile, DogProfile, BoardPost

HOODS = ["Barceloneta","El Born","Eixample","Gràcia","Horta","Les Corts",
         "Nou Barris","Poblenou","Sant Andreu","Sant Pere","Sarrià","Sants"]

def home(request):
    return render(request, "home.html", {"hoods": HOODS})

def about(request):
    return render(request, "about.html")

def register(request):
    if request.method == "POST":
        first_name    = request.POST.get("first_name")
        last_name     = request.POST.get("last_name")
        email         = request.POST.get("email")
        password      = request.POST.get("password")
        neighborhood  = request.POST.get("neighborhood")
        birthdate     = request.POST.get("birthdate")
        dog_name      = request.POST.get("dog_name")
        dog_breed     = request.POST.get("dog_breed")
        dog_birthdate = request.POST.get("dog_birthdate") or "2020-01-01"
        dog_weight    = float(request.POST.get("dog_weight") or 0)
        dog_behaviour = request.POST.get("dog_behaviour")

        # Check email not already taken
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "Email already registered. Please use another one.",
                "hoods": HOODS
            })

        # Generate unique username from email
        base_username = email.split("@")[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Create the Django User
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create the Profile
        Profile.objects.create(
            user=user,
            name=first_name,
            lastname=last_name,
            birthdate=birthdate,
            neighborhood=neighborhood,
        )

        # Create the DogProfile if dog name provided
        if dog_name:
            DogProfile.objects.create(
                user=user,
                dogName=dog_name,
                dogBirthdate=dog_birthdate,
                breed=dog_breed or "",
                weightKG=dog_weight,
                behaviour=dog_behaviour or "",
            )

        login(request, user)
        return redirect("my_profile")

    return render(request, "register.html", {"hoods": HOODS})

def login_view(request):
    if request.method == "POST":
        email    = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect("my_profile")
            else:
                return render(request, "login.html", {"error": "Invalid email or password."})
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid email or password."})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def board(request):
    return render(request, "board.html")

def my_profile(request):
    return render(request, "my_profile.html")

def user_profile(request, user_id):
    return render(request, "user_profile.html")

def users_list(request):
    return render(request, "users.html")

def search(request):
    return render(request, "search.html")

def edit_profile(request):
    return render(request, "edit_profile.html")

def delete_post(request, post_id):
    pass