from django.http import JsonResponse
from django.shortcuts import render,redirect
from .llm_service import LLM_Service
from .dashboard_llm_service import Dashboard_LLM_Service
from .models import HeartUser
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt


def home(request):
    # If logged-in, go to dashboard
    if request.session.get("user_id"):
        return redirect("/dashboard/")
    return render(request, "home.html")


def aiwrite(request):
    return render(request,'aiwrite.html')

def dashboard(request):
    # If NOT logged in → go to home
    if not request.session.get("user_id"):
        return redirect("/")
    return render(request, "dashboard.html")




llm_simple = LLM_Service()
dashboard_llm = Dashboard_LLM_Service()

def generate_text(request):
    mode = request.GET.get("mode", "").strip()
    text = request.GET.get("text", "").strip()
    tone = request.GET.get("tone", "soft").strip()  # default tone = soft

    # --- Validation ---
    if not mode:
        return JsonResponse({"response": "⚠️ Mode is missing."})

    if not text:
        return JsonResponse({"response": "⚠️ Please enter text."})

    # --- Generate output ---
    response_text = llm_simple.generate(mode, text, tone)

    return JsonResponse({"response": response_text})


def generate_dashboard(request):
    mode = request.GET.get("mode")
    name = request.GET.get("name", "")
    desc = request.GET.get("desc", "")
    depth = request.GET.get("depth", "light")
    language = request.GET.get("language", "en")

    if not mode or not desc:
        return JsonResponse({"response": "Please write something."})

    result = dashboard_llm.generate(mode, name, desc, depth, language)

    # ✅ RETURN STRING ONLY
    return JsonResponse({"response": result})







@csrf_exempt
def signup_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    if not username or not email or not password:
        return JsonResponse({"error": "Missing fields"}, status=400)

    if HeartUser.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already taken"}, status=400)

    if HeartUser.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)

    user = HeartUser.objects.create(
        username=username,
        email=email,
        password=make_password(password),
    )

    request.session["user_id"] = user.id     # VERY IMPORTANT
    request.session["username"] = user.username

    return JsonResponse({"status": "ok"})


@csrf_exempt
def logout_and_delete(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    user_id = request.session.get("user_id")

    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=400)

    try:
        user = HeartUser.objects.get(id=user_id)
        user.delete()
    except HeartUser.DoesNotExist:
        pass

    request.session.flush()   # remove session from server

    return JsonResponse({"status": "deleted"})






