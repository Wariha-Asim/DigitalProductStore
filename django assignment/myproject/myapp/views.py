from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from .models import User, Product, Category, Profile
import os
import pathlib
import random
from django.db.models import Max
from django.core.files.storage import default_storage

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['id'] = user.id
                request.session['name'] = user.name
                request.session['email'] = user.email
                return redirect("showall")
            else:
                request.session['login_message'] = "Invalid email or password"
        except User.DoesNotExist:
            request.session['login_message'] = "Invalid email or password"
    
   
    login_message = request.session.pop('login_message', None)
    return render(request, 'login.html', {'login_message': login_message})

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.filter(email=email).exists():
            request.session['signup_message'] = "Email already exists"
            return render(request, 'signup.html', {'name': name, 'email': email, 'signup_message': request.session.pop('signup_message', None)})

        if password != confirm_password:
            request.session['signup_message'] = "Passwords do not match"
            return render(request, 'signup.html', {'name': name, 'email': email, 'signup_message': request.session.pop('signup_message', None)})

        user = User(name=name, email=email, password=make_password(password))
        user.save()

        request.session['name'] = user.name
        request.session['user_id'] = user.id

        request.session['signup_message'] = "You have signed up successfully"
        return redirect("showall")
    
   
    signup_message = request.session.pop('signup_message', None)
    return render(request, 'signup.html', {'signup_message': signup_message})

def showall(request):
    product = Product.objects.all()
    return render(request, 'showall.html', {'product1': product})

def deleteprod(request, id):
    product = get_object_or_404(Product, id=id)
    
    img_path = product.img_url.replace('/media/', '')
    
    product.delete()

    if default_storage.exists(img_path):
        default_storage.delete(img_path)

    messages.info(request, "The record has been deleted!!!")
    return redirect("showall")

def deleteall(request):
    products = Product.objects.all()
    
    for product in products:
        img_path = product.img_url.replace('/media/', '')
        
        product.delete()
        
        if default_storage.exists(img_path):
            default_storage.delete(img_path)

    messages.info(request, "All records have been deleted!!!")
    return redirect("showall")

def createprod(request):
    if request.method == "POST":
        title = request.POST.get("title")
        brand = request.POST.get("brand")
        price = request.POST.get("price")
        qty = request.POST.get("qty")
        desc = request.POST.get("desc")
        imgfile = request.FILES.get("file")
        category_id = request.POST.get("category")

        try:
            user = User.objects.get(id=request.session['id'])
            category = Category.objects.get(id=category_id)
        except (User.DoesNotExist, Category.DoesNotExist):
            return render(request, 'addprod.html', {'category1': Category.objects.all(), 'typemsg': 'Invalid user or category'})

        if bool(imgfile):
            file_name = imgfile.name.lower()
            if not (file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.jpeg')):
                msg = 'File type should be .jpg, .png or .jpeg'
                return render(request, 'addprod.html', {'category1': Category.objects.all(), 'typemsg': msg})

            fss = FileSystemStorage()
            product = Product(
                name=title,
                brand=brand,
                price=price,
                qty=qty,
                description=desc,
                category=category,
                user=user
            )
            product.save()

            max_id = Product.objects.aggregate(Max('id'))
            p = Product.objects.get(id=max_id['id__max'])

            file_path = f"{p.id}.png"
            file_url = fss.save(file_path, imgfile)
            p.img_url = fss.url(file_url)
            p.save(update_fields=['img_url'])

        else:
            msg = 'Please select a file'
            return render(request, 'addprod.html', {'category1': Category.objects.all(), 'filemsg': msg})

        return redirect('showall')
    else:
        categories = Category.objects.all()
        return render(request, 'addprod.html', {'category1': categories})

def logout(request):
    try:
        del request.session['name']
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('signup')

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('title')
        product.brand = request.POST.get('brand')
        product.price = request.POST.get('price')
        product.qty = request.POST.get('qty')
        product.description = request.POST.get('desc')

        category_id = request.POST.get('category')
        if category_id:
            product.category_id = category_id

        if bool(request.FILES.get('img_url', False)):
            imgfile = request.FILES['img_url']
            file_name = imgfile.name.lower()

            if not (file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.jpeg')):
                msg = 'File type should be .jpg, .png or .jpeg'
                return render(request, 'updateprod.html', {
                    'product1': product,
                    'category1': Category.objects.all(),
                    'typemsg': msg,
                    'request': request
                })

            old_image_path = pathlib.Path(__file__).parent.parent.joinpath("ProductImage").joinpath(f"{product_id}.png")
            if old_image_path.exists():
                os.remove(old_image_path)

            fss = FileSystemStorage()
            file_path = fss.save(f"{product_id}.png", imgfile)
            product.img_url = fss.url(file_path)

        product.save()
        return redirect('showall')
    else:
        categories = Category.objects.all()

    return render(request, 'updateprod.html', {
        'product1': product,
        'category1': categories,
        'request': request
    })

def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return render(request, 'product_detail.html', {'error_message': 'Product not found.'})

    return render(request, 'product_detail.html', {'product': product})

def password_reset_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            code = str(random.randint(1000, 9999))
            profile, created = Profile.objects.get_or_create(user=user)
            profile.reset_code = code
            profile.save()

            send_mail(
                'Password Reset Code',
                f'Your password reset code is {code}',
                'hellonoti12@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('password_reset_code')
        else:
            messages.error(request, "Email not found")

    return render(request, 'password_reset_email.html')

def password_reset_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        profile = Profile.objects.filter(reset_code=code).first()
        if profile:
            request.session['reset_code'] = code
            return redirect('password_reset_confirm')
        else:
            messages.error(request, "Invalid code")

    return render(request, 'password_reset_code.html')

def password_reset_confirm(request):
    if request.method == 'POST':
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        if password1 == password2:
            code = request.session.get('reset_code')
            profile = Profile.objects.filter(reset_code=code).first()
            if profile:
                user = profile.user
                user.password = make_password(password1)
                user.save()
                profile.reset_code = ''
                profile.save()
                return redirect('login')
            else:
                messages.error(request, "Reset code expired or invalid")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'password_reset_confirm.html')
