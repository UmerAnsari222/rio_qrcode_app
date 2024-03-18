from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, QRCodeData, QRCodeScan, Profile, ProfilePoint, GiftPoint, UserGifts
from django.db.models import Q
from .utils.generate_profile_qr import generate_profile_qr_code
from django.contrib.auth.decorators import login_required
import json
from random import randint

# Create your views here.


@login_required(login_url="/login")
def homeView(request):
    if request.user.is_authenticated is not True:
        return redirect("LoginView")

    user = request.user
    qr_codes = QRCodeData.objects.all()
    scanned_codes_ids = QRCodeScan.objects.filter(user=user).values_list(
        "qr_code_id", flat=True
    )
    print(scanned_codes_ids)

    # Retrieve QRCodeScan objects for scanned codes
    scanned_codes = QRCodeScan.objects.filter(qr_code_id__in=scanned_codes_ids)
    print(scanned_codes)
    # Exclude scanned codes from qr_codes
    qr_codes_not_scanned = qr_codes.exclude(id__in=scanned_codes_ids)
    print(qr_codes_not_scanned)
    # Combine both sets
    # all_qr_codes = list(qr_codes_not_scanned) + list(scanned_codes)
    context = {"qr_codes": qr_codes_not_scanned,
               "scanned_codes": scanned_codes}
    return render(request, "home_page.html", context)


@login_required(login_url="/login")
def profileView(request):
    if request.user.is_authenticated is not True:
        return redirect("LoginView")

    profile = Profile.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    smallest_gift_point_record = GiftPoint.objects.order_by(
        'gift_points').first()

    gifts_exists = check_gift_points(profile, smallest_gift_point_record)

    user_gifts = UserGifts.objects.filter(user=user)
    print(user_gifts)

    if request.method == 'POST':
        print(gifts_exists)

        # Check if any records exist
        if gifts_exists.exists():
            # Get a random index within the range of available records
            random_index = randint(0, gifts_exists.count() - 1)

            # Retrieve the random record
            random_gift = gifts_exists[random_index]

            UserGifts.objects.create(user=user, gifts=random_gift)

            profile.points -= random_gift.gift_points
            profile.save()
            # Now you can use random_gift for further operations
            print(random_gift)
            gifts_exists = check_gift_points(
                profile, smallest_gift_point_record)

            context = {"profile": profile,
                       "gifts_exists": gifts_exists.exists(),
                       "user_gifts": user_gifts
                       }
            return render(request, "profile_page.html", context)

    print(gifts_exists)
    context = {"profile": profile,
               "gifts_exists": gifts_exists.exists(),
               "user_gifts": user_gifts
               }
    return render(request, "profile_page.html", context)


def dashboardView(request):
    if (
        request.user.is_authenticated is not True
        and request.user.is_superuser is not True
    ):
        return redirect("LoginView")

    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "dashboard_page.html", context)


@login_required(login_url="/login")
def scanView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data.get("decodedText"))

        if request.user.is_authenticated:
            user = Profile.objects.get(username=request.user.username)
            if user is not None:
                qr_code = QRCodeData.objects.get(uuid=data.get("decodedText"))
                exist_scan = QRCodeScan.objects.filter(
                    user=request.user, qr_code=qr_code
                ).exists()

                if exist_scan:
                    return JsonResponse(
                        {"error": "QR code already scanned"}, status=500
                    )

                create_scan = QRCodeScan.objects.create(
                    user=request.user, qr_code=qr_code
                )

                # user = Profile.objects.get(username=request.user.username)

                user.points = user.points + qr_code.data

                user.save()

                context = {"success": "QR code Scan Successfully"}
                return JsonResponse(context)
    return render(request, "scan_page.html")


@login_required(login_url="/login")
def codeDetailView(request, uuid):
    print(uuid)
    qr_code = QRCodeData.objects.get(uuid=uuid)

    if qr_code is None:
        return render(
            request, "code_detail.html", {
                "error": "Not Found",
            }
        )
    context = {"qr_code": qr_code}
    return render(request, "code_detail.html", context)


def loginView(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username) is None:
            return render(request, "login_page.html", {"error": "User not found"})

        auth = authenticate(username=username, password=password)
        print(auth)

        if auth is None:
            return render(
                request, "login_page.html", {
                    "error": "Incorrect username or password"}
            )

        if auth.is_authenticated:
            login(request, auth)
            return redirect("/")

    return render(request, "login_page.html")


def registerView(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if User.objects.filter(username=username).exists():
            return render(
                request, "register_page.html", {
                    "error": "Username already exists"}
            )

        profile_point = ProfilePoint.objects.first()
        if profile_point is not None:
            user = User.objects.create_user(username, email, password)
            auth = authenticate(username=user.username, password=password)
            print(auth.is_authenticated)
            if auth is not None:
                login(request, auth)
                profile_point = ProfilePoint.objects.first()
                qr_code = generate_profile_qr_code(
                    profile_point.profile_points)
                profile = Profile.objects.create(
                    username=user.username, points=0, qr_code=qr_code
                )
                print("PROFILE", profile)
                return redirect("/")
        else:
            return render(
                request, "register_page.html", {
                    "error": "Some error occurred"
                }
            )

    return render(request, "register_page.html")


def logoutView(request):
    logout(request)
    return redirect("/login")


def check_gift_points(profile, smallest_gift_point_record):
    gifts = GiftPoint.objects.filter(
        # Points are less than or equal to profile points
        Q(gift_points__lte=profile.points) &
        # Points are not equal to smallest gift points
        ~Q(gift_points__lt=smallest_gift_point_record.gift_points) &
        # Points are not greater than profile points
        ~Q(gift_points__gt=profile.points)
    )

    return gifts
