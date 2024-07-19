from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .models import Tweet
from .forms import TweetForm, UserRegistrationForm,SearchForm
# Create your views here.



def tweet_list(request):
    tweet = Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweet})

@login_required
def create_tweet(request):
    if request.method == "POST":
        form = TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            form.save()
            return redirect('tweet_list')
            
    else:
        form = TweetForm()
    return render(request,'tweet_form.html',{'form':form})

@login_required
def edit_tweet(request,tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})    


@login_required
def delete_tweet(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id, user= request.user)

    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})


@login_required
def search_tweet(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        tweets = []
        if form.is_valid():
            search = form.cleaned_data["search"]
            tweets = Tweet.objects.filter(text__icontains=search)
    return render(request,'search_tweet.html',{'form':form,'tweets':tweets})
    




def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            form.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})