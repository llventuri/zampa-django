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

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "Email already registered.",
                "hoods": HOODS
            })

        base_username = email.split("@")[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(username=username, email=email, password=password)

        Profile.objects.create(
            user=user,
            name=first_name,
            lastname=last_name,
            birthdate=birthdate,
            neighborhood=neighborhood,
        )

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

@login_required
def board(request):
    if request.method == "POST":
        dog = DogProfile.objects.filter(user=request.user).first()
        if dog:
            BoardPost.objects.create(
                dog=dog,
                title=request.POST.get("title"),
                neighborhood=request.POST.get("neighborhood"),
                schedule=request.POST.get("schedule", ""),
                post_type=request.POST.get("post_type"),
                text=request.POST.get("text", ""),
                dateRequested=request.POST.get("dateRequested"),
            )
        return redirect("board")

    selected_neighborhood = request.GET.get("neighborhood", "")
    posts = BoardPost.objects.filter(active=True).order_by("-dateTimePost")
    if selected_neighborhood:
        posts = posts.filter(neighborhood=selected_neighborhood)

    return render(request, "board.html", {
        "posts": posts,
        "hoods": HOODS,
        "selected_neighborhood": selected_neighborhood,
    })

@login_required
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    dog = DogProfile.objects.filter(user=request.user).first()
    posts = BoardPost.objects.filter(dog__user=request.user).order_by("-dateTimePost")
    return render(request, "my_profile.html", {
        "profile": profile,
        "dog": dog,
        "posts": posts,
    })

def user_profile(request, user_id):
    profile_user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=profile_user)
    dog = DogProfile.objects.filter(user=profile_user).first()
    posts = BoardPost.objects.filter(dog__user=profile_user, active=True).order_by("-dateTimePost")
    return render(request, "user_profile.html", {
        "profile": profile,
        "dog": dog,
        "posts": posts,
    })

def users_list(request):
    profiles = Profile.objects.select_related("user").all()
    users = []
    for profile in profiles:
        dog = DogProfile.objects.filter(user=profile.user).first()
        users.append({
            "user": profile.user,
            "profile": profile,
            "dog": dog,
        })
    return render(request, "users.html", {"users": users})

def search(request):
    users = []
    searched = False
    query_name         = request.GET.get("username", "")
    query_dog          = request.GET.get("dog_name", "")
    query_neighborhood = request.GET.get("neighborhood", "")

    if query_name or query_dog or query_neighborhood:
        searched = True
        profiles = Profile.objects.select_related("user").all()

        if query_name:
            profiles = profiles.filter(name__icontains=query_name)
        if query_neighborhood:
            profiles = profiles.filter(neighborhood=query_neighborhood)

        for profile in profiles:
            dog = DogProfile.objects.filter(user=profile.user).first()
            if query_dog and (not dog or query_dog.lower() not in dog.dogName.lower()):
                continue
            users.append({
                "user": profile.user,
                "profile": profile,
                "dog": dog,
            })

    return render(request, "search.html", {
        "users": users,
        "searched": searched,
        "query_name": query_name,
        "query_dog": query_dog,
        "query_neighborhood": query_neighborhood,
        "hoods": HOODS,
    })

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    dog = DogProfile.objects.filter(user=request.user).first()

    if request.method == "POST":
        profile.name         = request.POST.get("first_name")
        profile.lastname     = request.POST.get("last_name")
        profile.neighborhood = request.POST.get("neighborhood")
        profile.save()

        dog_name      = request.POST.get("dog_name")
        dog_breed     = request.POST.get("dog_breed")
        dog_birthdate = request.POST.get("dog_birthdate") or "2020-01-01"
        dog_weight    = float(request.POST.get("dog_weight") or 0)
        dog_behaviour = request.POST.get("dog_behaviour")

        if dog:
            dog.dogName      = dog_name
            dog.breed        = dog_breed
            dog.dogBirthdate = dog_birthdate
            dog.weightKG     = dog_weight
            dog.behaviour    = dog_behaviour
            dog.save()
        elif dog_name:
            DogProfile.objects.create(
                user=request.user,
                dogName=dog_name,
                dogBirthdate=dog_birthdate,
                breed=dog_breed or "",
                weightKG=dog_weight,
                behaviour=dog_behaviour or "",
            )

        return redirect("my_profile")

    return render(request, "edit_profile.html", {
        "profile": profile,
        "dog": dog,
        "hoods": HOODS,
    })

@login_required
def delete_post(request, post_id):
    post = BoardPost.objects.get(id=post_id, dog__user=request.user)
    post.delete()
    return redirect("my_profile")