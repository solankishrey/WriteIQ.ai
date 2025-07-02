from backoffice_engine.models import User,Subscription,Feedback,PlanDetails
from backoffice_engine.forms import UserForm
from backoffice_engine.forms import UserUpdateForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from writiq import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session

def index(request):
    feedbacks = Feedback.objects.all().order_by('-id')  
    return render(request, 'index.html', {'feedbacks': feedbacks})



def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        user = User.objects.create(
            name=f"{first_name} {last_name}",
            email=email,
            password=password,
            otp="000000",
            otp_used=0
        )

        from datetime import date, timedelta
        
        free_plan = PlanDetails.objects.filter(name="Free Plan", duration_days=30, is_active=True).first()
        if free_plan:
            start_date = date.today()
            end_date = start_date + timedelta(days=free_plan.duration_days)
            
            Subscription.objects.create(
                user=user,
                plan=free_plan,
                start_date=start_date,
                end_date=end_date,
                status='active',
                pending_credit=free_plan.credit
            )
        else:
            print("No free plan found. Please create one in Plan table.")

        request.session['user_id'] = user.id  
        messages.success(request, "Account created successfully!")
        return redirect('/login/')
    
    return render(request, 'signup.html')



def app(request):
    return render(request, 'app.html')

from django.shortcuts import render
from backoffice_engine.models import User, Feedback, Subscription, GeneratedContent, Category, SubCategory

def dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_feedbacks': Feedback.objects.count(),
        'total_subscriptions': Subscription.objects.count(),
        'total_generated_content': GeneratedContent.objects.count(),
        'total_categories': Category.objects.count(),
        'total_subcategories': SubCategory.objects.count(),
    }
    return render(request, 'dashboard.html', context)



def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.id

            # ✅ Add this block to store current plan in session
            try:
                subscription = Subscription.objects.get(user_id=user.id)
                request.session['plan'] = subscription.plan.id
            except Subscription.DoesNotExist:
                request.session['plan'] = None

            return redirect('/logged_in/')
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials.")
            return redirect('/login/')
    return render(request, "login.html")


def features(request):
    return render(request,'features.html')

def pricing(request):
    plans = PlanDetails.objects.all()
    return render(request, 'pricing.html', {'plans': plans})


def profile(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        e = User.objects.get(id=id)

        try:
            s = Subscription.objects.get(user=e)
            plan_name = s.plan.name if s.plan else "Free"
            start_date = s.start_date
            end_date = s.end_date
            total_credits = s.plan.credit if s.plan else s.pending_credit 
            pending_credits = s.pending_credit
            print(f"pending_credits : {pending_credits}")
        except Subscription.DoesNotExist:
            plan_name = "Free"
            start_date = None
            end_date = None
            total_credits = 0
            pending_credits = 0

        return render(request, 'profile.html', {
            'e': e,
            'plan_name': plan_name,
            'start_date': start_date,
            'end_date': end_date,
            'total_credits': total_credits,
            'pending_credits': pending_credits
        })
    else:
        return redirect("/login/")

def update_profile(request, user_id):
    e = User.objects.get(id=user_id)
    if request.method == "POST":
        f = UserUpdateForm(request.POST, instance=e)
        if f.is_valid():
            try:
                f.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('/profile/')
            except:
                print(sys.exc_info())
                messages.error(request, "An error occurred while updating the profile.")
                return render(request, "updated_profile.html", {'e': e, 'form': f})
        else:
            for field in f:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            return render(request, "updated_profile.html", {'e': e, 'form': f})
    else:
        f = UserUpdateForm(instance=e)
        return render(request, "updated_profile.html", {'e': e, 'form': f})
    
def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def help(request):
    return render(request, 'help.html')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return render(request, 'logout.html') 


def submit_feedback(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        rating = request.POST.get("rating")

        Feedback.objects.create(name=name, email=email, message=message, rating=rating)
        messages.success(request, "Thank you for your feedback!")
        return redirect('/home/')
    return render(request, 'feedback.html')

def forgot_password(request):
    if request.method == "POST":
        otp = random.randint(10000, 99999)
        email = request.POST.get('email')

        request.session['temail'] = email  
        if User.objects.filter(email=email).exists():
            User.objects.filter(email=email).update(otp=otp, otp_used=0)

            subject = 'OTP Verification'
            message = f"Your Writiq OTP is: {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, email_from, recipient_list)
            print("------------ OTP mail sent ---------")
            return render(request, 'reset_password.html')

        else:
            messages.error(request, "Invalid email ID")
            return redirect('/login/')

    return render(request, 'forgot_password.html')
    

import sys
def reset_password(request): 
    if request.method == "POST":
        otp = request.POST["otp"]
        pwd = request.POST["password"]
        cpwd = request.POST["confirm_password"]
        e = request.session.get('temail')  

        try:
            user = User.objects.get(email=e, otp=otp, otp_used=0)
        except User.DoesNotExist:
            messages.error(request, "Invalid OTP")
            return render(request, 'reset_password.html')

        if pwd == cpwd:
            user.password = pwd
            user.otp_used = 1
            try:
                user.save() 
                messages.success(request, "Password reset successful.")
                return redirect("/logged_in/")
            except Exception as ex:
                print("-----------", sys.exc_info())
                messages.error(request, "Something went wrong.")
                return render(request, 'reset_password.html')
        else:
            messages.error(request, "Password and confirm password not match")
            return render(request, "reset_password.html")

    return render(request, "reset_password.html")


def logged_in(request):
    if not request.session.get('user_id'):
        return redirect('/login/') 
    return render(request, 'logged_in.html')
    

def delete_account(request, eid):
    try:
        e = User.objects.get(id=eid)
        e.delete()
        messages.success(request, "Your account has been deleted successfully.")
    except User.DoesNotExist:
        messages.error(request, "Account does not exist.")

    return redirect('/login/')


from datetime import date,timedelta
@csrf_exempt
@csrf_exempt
def payment_success(request):
    uid = request.POST.get("user_id")
    pid = request.POST.get("plan")

    p = PlanDetails.objects.get(id=pid)
    sd = date.today()
    ed = sd + timedelta(days=p.duration_days)

    Subscription.objects.filter(user=uid).update(
        plan=p,
        start_date=sd,
        end_date=ed,
        status='active',
        pending_credit=p.credit,
        total_credit=p.credit
    )

    request.session["user_id"] = int(uid)
    request.session["plan"] = int(pid)

    return render(request, 'payment_success.html')

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backoffice_engine.models import GeneratedContent, Category, SubCategory
from backoffice_engine.utils import generate_gemini_content
import json


def generator(request):
    user_id = request.session.get("user_id")
    subscription = Subscription.objects.filter(user_id=user_id).first()
    pending_credits = subscription.pending_credit if subscription else 0

    return render(request, 'generator.html', {
        'pending_credits': pending_credits
    })



def my_generated_content(request):
    user_id = request.session.get('user_id')
    documents = GeneratedContent.objects.filter(user_id=user_id).select_related('category_id', 'sub_category_id')
    return render(request, 'my_generated_content.html', {'documents': documents})


@csrf_exempt
def generate_content(request):
    if request.method == "POST":
        if 'user_id' not in request.session:
            return HttpResponse("User not logged in", status=401)

        user_id = request.session.get("user_id")
        try:
            user = User.objects.get(id=user_id)
            subscription = Subscription.objects.get(user=user)
        except (User.DoesNotExist, Subscription.DoesNotExist):
            return HttpResponse("Subscription not found", status=404)

        if subscription.pending_credit <= 0:
            return HttpResponse("You are out of credits!", status=403)

        doc_type = request.POST.get("doc_type", "")
        sub_category = request.POST.get("sub_category", "")
        creativity = request.POST.get("creativity", "50")
        prompt = request.POST.get("prompt", "")

        result = generate_gemini_content(doc_type, sub_category, creativity, prompt)

        subscription.pending_credit -= 1
        subscription.save()

        return HttpResponse(result)

@csrf_exempt
def save_generated_content(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content")
            prompt = data.get("prompt")
            category_name = data.get("category")
            sub_category_name = data.get("sub_category")

            user_id = request.session.get("user_id")
            if not user_id:
                return JsonResponse({"error": "User not logged in"}, status=403)

            category = Category.objects.filter(name=category_name).first()
            sub_category = SubCategory.objects.filter(name=sub_category_name, category_id=category).first()

            if not (category and sub_category):
                return JsonResponse({"error": "Invalid category or sub-category"}, status=400)

            GeneratedContent.objects.create(
                user_id=user_id,
                prompt=prompt,
                content=content,
                category_id=category,
                sub_category_id=sub_category,
            )

            return JsonResponse({"message": "Content saved successfully"})
        except Exception as e:
            print("Error saving content:", str(e))
            return JsonResponse({"error": "Failed to save content"}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)


from django.http import HttpResponse
from datetime import date
from backoffice_engine.models import Subscription, PlanDetails

@csrf_exempt
def check(request):
    user_id = request.session.get('user_id')  
    try:
        s = Subscription.objects.get(user_id=user_id)
    except Subscription.DoesNotExist:
        return HttpResponse("")

    end = s.end_date
    if date.today() >= end:
        free_plan = PlanDetails.objects.get(name="Free Plan")
        
        Subscription.objects.filter(user_id=user_id).update(
            plan=free_plan,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=free_plan.duration_days),
            pending_credit=free_plan.credit,
            total_credit=free_plan.credit,
            status="active"
        )
        
        request.session["plan"] = free_plan.id  # update session to reflect downgrade
        
        return HttpResponse("Your paid plan expired. You have been downgraded to the Free Plan.")
    
    return HttpResponse("")





