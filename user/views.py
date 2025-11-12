from .cart import Cart
from user.models import *
from exam.models import *
from video.models import *
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404





def cart_detail(request):
    cart = Cart(request)
    return render(request, 'user/cart.html', {'cart': cart})

def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.add(book=book, quantity=1)
    return redirect('cart')

def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart')


from django.http import JsonResponse
from .cart import Cart


def cart_update(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        quantity = request.POST.get("quantity")

        cart = Cart(request)
        book = Book.objects.get(id=book_id)
        cart.add(book, quantity=int(quantity), update_quantity=True)

        return JsonResponse({
            "success": True,
            "total_price": str(cart.get_total_price())
        })

    return JsonResponse({"success": False}, status=400)





def login_views(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Daxil oldunuz!')
            return redirect('index')
        else:
            messages.error(request, 'Email və ya şifrə yanlışdır!')

    return render(request, 'user/login.html')



def register_views(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Şifrələr eyni olmalıdır.')

        elif User.objects.filter(username=email).exists():
            messages.error(request, 'Bu email artıq qeydiyyatdan keçib.')

        else:
            user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=False
                )
            UserProfile.objects.create(
                user=user,
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            verification = EmailVerification.objects.create(user=user, purpose='register')
            otp = verification.generate_otp()

            send_mail(
                'Email Təsdiqi',
                f'Salam {first_name}, sizin OTP kodunuz: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )



            messages.success(request, 'E-poçt ünvanınıza təsdiq kodu göndərildi.')
            return redirect('verify_email', user_id=user.id)

    return render(request, 'user/register.html')







def verify_email(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        verification = EmailVerification.objects.filter(user=user, purpose='register').latest('created_at')
    except User.DoesNotExist:
        messages.error(request, 'İstifadəçi tapılmadı.')
        return redirect('register')
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Email verification tapılmadı.')
        return redirect('register')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == verification.otp:
            verification.is_verified = True
            verification.save()
            user.is_active = True
            user.save()
            messages.success(request, 'Email təsdiqləndi, indi daxil ola bilərsiniz.')
            return redirect('login')
        else:
            messages.error(request, 'OTP kod yanlışdır.')

    return render(request, 'user/smsCode.html', {'user': user,
                                                'purpose': 'register'
                                                })


@login_required
def logout_views(request):
    logout(request)
    messages.success(request, 'Çıxış etdiniz.')
    return redirect('logout')


@login_required
def account_views(request):
    profile = UserProfile.objects.get(user=request.user)
    exams = Exam.objects.filter(purchases__user=request.user)
    videos = Video.objects.filter(purchases__user=request.user)
    purchased_exams = PurchasedExam.objects.filter(user=request.user)
    sessions = UserExamSession.objects.filter(
        user=request.user
    ).select_related('exam').order_by('-finished_at')


    context={
        'profile': profile,
        'exams': exams,
        'videos': videos,
        'purchased_exams': purchased_exams,
        'sessions': sessions,
    }
    return render(request, 'user/account.html', context)

def password_reset_views(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Bu e-poçt ilə istifadəçi tapılmadı.')
            return redirect('password_reset_views')

        # Mövcud verification varsa sil (əks halda UNIQUE constraint error verəcək)
        EmailVerification.objects.filter(user=user, purpose='reset').delete()

        # Yeni verification yarat
        verification = EmailVerification.objects.create(user=user, purpose='reset')
        otp = verification.generate_otp()

        # OTP-ni emailə göndər
        send_mail(
            'Şifrə sıfırlama',
            f'Salam {user.first_name}, şifrənizi sıfırlamaq üçün OTP kodunuz: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.success(request, 'OTP kodu e-poçt ünvanınıza göndərildi.')
        # OTP səhifəsinə yönləndiririk
        return redirect('password_reset_verify', user_id=user.id)

    return render(request, 'user/emailforReset.html')


def password_reset_verify(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        verification = EmailVerification.objects.filter(user=user, purpose='reset').latest('created_at')
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        messages.error(request, 'İstifadəçi tapılmadı.')
        return redirect('password_reset_views')

    if request.method == 'POST':
        otp = request.POST.get('otp')

        if otp != verification.otp:
            messages.error(request, 'OTP kod yanlışdır.')
        else:
            verification.is_verified = True
            verification.save()
            messages.success(request, 'OTP təsdiqləndi. İndi yeni şifrənizi daxil edin.')
            return redirect('password_reset_confirm', user_id=user.id)

    return render(request, 'user/smsCode.html', {
        'user': user,
        'purpose': 'reset'
    })



def password_reset_confirm(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        verification = EmailVerification.objects.filter(user=user, purpose='reset').latest('created_at')
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        messages.error(request, 'İstifadəçi tapılmadı.')
        return redirect('password_reset_views')

    if not verification.is_verified:
        messages.error(request, 'OTP təsdiqlənməyib.')
        return redirect('password_reset_verify', user_id=user.id)

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Şifrələr eyni deyil.')
        else:
            user.password = make_password(password)
            user.save()

            # OTP-ni silirik (təhlükəsizlik üçün)
            verification.otp = " "
            verification.save()

            messages.success(request, 'Şifrəniz yeniləndi. İndi daxil ola bilərsiniz.')
            return redirect('login')

    return render(request, 'user/resetPassword.html', {'user': user})