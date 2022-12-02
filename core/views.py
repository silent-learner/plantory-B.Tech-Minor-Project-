from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .dl_model.model import classify_image
# Create your views here.

def index(req):
    context = {
        "home": "active font-weight-bold" 
    }
    return render(req,'core/index.html',context)


def LogIn(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('community')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'core/login.html', context)

def plantdisease(req):
	context = {
        "plantdisease": "active font-weight-bold" 
    }
	if(req.method == 'GET'):
		return render(req,'core/plantdisease.html',context)

	if( req.method == 'POST'):

		unploaded_file = req.FILES['plant_leaf']
		image = unploaded_file.read()

		result = classify_image(image)
        #Select the top three predictions according to their probabilities
		top1 = '1. Species: %s, Disease: %s'%(result[0][0].split('_')[0], result[0][1])
		top2 = '2. Species: %s, Disease: %s'%(result[1][0].split('_')[0], result[1][1])
		top3 = '3. Species: %s, Disease: %s'%(result[2][0].split('_')[0], result[2][1])

		predictions = [{ 'pred':top1 , "prob" : round(result[0][2]*100,2) , "color" : "success"}, { 'pred':top2 , "prob" : round(result[1][2]*100,2) , "color" : "warning"}, { 'pred':top3 , "prob" : round(result[2][2]*100,2) , "color" : "danger"}]
		context['predictions'] = predictions 

		fs = FileSystemStorage()
		filename = fs.save(unploaded_file.name, unploaded_file)
		uploaded_file_url = fs.url(filename)
		context['url'] = uploaded_file_url


		return render(req, 'core/plantdisease.html', context)

def plantinfo(req):
	context = {
        "plantinfo": "active font-weight-bold" 
    }
	if req.method == 'GET' :
		return render(req,'core/plantinfo.html',context)

	if( req.method == 'POST'):

		unploaded_file = req.FILES['plant_leaf']
		image = unploaded_file.read()

		result = classify_image(image)
        #Select the top three predictions according to their probabilities

		predictions = [{ 'pred':result[0][0].split('_')[0] , "prob" : round(result[0][2]*100,2) , "color" : "success"}, { 'pred':result[1][0].split('_')[0] , "prob" : round(result[1][2]*100,2) , "color" : "warning"}, { 'pred':result[2][0].split('_')[0] , "prob" : round(result[2][2]*100,2) , "color" : "danger"}]
		context['predictions'] = predictions  

		fs = FileSystemStorage()
		filename = fs.save(unploaded_file.name, unploaded_file)
		uploaded_file_url = fs.url(filename)
		context['url'] = uploaded_file_url

		return render(req, 'core/plantinfo.html', context)
	

@login_required(login_url='login')
def community(req):
	if req.method == 'POST':
		user = req.user
		image = req.FILES.get('image_upload')
		content = req.POST['content']
		new_post = PostMessage.objects.create(user=user, image=image, content=content)
		new_post.save()
		print(user,image,content)
	posts = PostMessage.objects.all().order_by('-date_added')
	context = {
        "community": "active font-weight-bold" ,
		'posts' : posts
    }
	return render(req,'core/community.html',context)

@csrf_protect
def signup(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'core/signup.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def commentPage(request,postId):
	post = PostMessage.objects.get(id=postId)
	if request.method == 'POST':
		user = request.user
		comment_content = request.POST['comment']
		print(comment_content)
		new_comment = comment.objects.create(user=user,content=comment_content,message=post)
		new_comment.save()
	if post is not None:
		comments = comment.objects.filter(message=post)
		image = post.image.url
		post_content = post.content
		context = {
			'image':image,
			'content':post_content,
			'user':post.user,
			'comments':comments,
			"community": "active font-weight-bold" ,
		}
		return render(request,'core/commentPage.html',context)

