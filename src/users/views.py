from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import (
	authenticate, 
    get_user_model, 
    login, 
    logout
)
from .forms import UserLoginForm, UserRegisterForm


# Create your views here.

# assign User to User model using get_user_model() 
User = get_user_model()


def login_view(request):
    """
    User Login view
    """
    if request.method == "POST":
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get('password')
            # Check is is authenticate or none
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('/')
        else:
            print(form.errors)
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "users/login.html", context)



def register_view(request):
    """
    User Register view with activation link vai email.
    """
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        verification_url = "Verification Link: http://127.0.0.1:8000/user/verification?email={}&id={}"
        # Send activation link with query paremeter
        user.send_verification_email(
            subject="Confirm Your Email", 
            message=verification_url.format(user.email, user.id), 
            from_email="no_reply@adnblog.com"
        )
        return redirect("/")

    context = {
        "form": form,
    }
    return render(request, "users/registration.html", context)


def user_verification(request):
    """
    User verification based on query paremeter.
    """
    email = request.GET.get("email")
    user_id = request.GET.get("id")
    if email and user_id:
        try:
            user = User.objects.get(email=email, id=user_id)
            if user.is_active:
                messages.success(request, 'Account Already Verified.')
            else:
                user.is_active = True
                user.save()
                messages.success(request, 'Successfully Verified The Account.')
        except Exception as e:
            messages.success(request, 'Invalid Query')
    else:
        messages.success(request, 'Invalid Query')

    return redirect("/user/login/")


def logout_view(request):
    """
    User logout view
    """
    logout(request)
    return redirect("/")
