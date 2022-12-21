from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
import base64
from django.core.files.base import ContentFile
from .models import PhotoUpload
from .models import Comments
import json
from django.http import JsonResponse
from .models import Notification
import datetime

User = get_user_model()

fname =''
lname = ''
username = ''
password = ''
email = ''
section = ''

user_loged = None





i = 0

photo_id = 0

def base64_to_image(base64_string):
    format, imgstr = base64_string.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name=username+".png")


# for login page
def loginhandle(req):
    if req.user.is_authenticated:
        return redirect(f'/home/{req.user.section}')
    global user_loged
    if req.method == 'POST':
        u_name = req.POST.get('username')
        u_pass = req.POST.get('password')
        user_loged = authenticate(username = u_name, password = u_pass)

        if user_loged is not(None):
            login(req, user_loged)
            return redirect(f'/home/{req.user.section}')
        else:
            return render(req, 'login.html', {'err' : 'Invalid Credentials'})


    return render(req,'login.html')


#for signup page
def signuphandle(req):
    if req.user.is_authenticated:
        return redirect(f'/home/{req.user.section}')
    global fname, lname, username, password, email, section
    if req.method == 'POST':
        fname = req.POST.get('fname')
        lname = req.POST.get('lname')
        username = req.POST.get('username')
        password = req.POST.get('password')
        email = req.POST.get('email')
        section = req.POST.get('section')
        img_src = req.POST.get('imgurl')
        

        try:
            y = User.objects.get(username= username)
            l = User.objects.filter(email= email)
            return render(req,'signup.html', {'err': 'A user with this username or email already exist'})
        except User.DoesNotExist:
           user = User.objects.create_user(username, email, password)
           user.first_name = fname
           user.last_name = lname
           user.section = section
           user.img_src = base64_to_image(img_src)
           user.save()
           return redirect('/')
       
    return render(req,'signup.html')

#for home page
def homepage(req, section):
    if req.user.is_authenticated:
        number_of_notifications = 0
        tableObjects = PhotoUpload.objects.filter(section = section).order_by("-id")
        notification_numbers = Notification.objects.filter(for_user = req.user.username)
        for noti in notification_numbers:
            if noti.notify == True:
                number_of_notifications = number_of_notifications+1
        
        
        usersSection = User.objects.filter(section = section)
        context = {
            'username': req.user.username,
            'yourimage': req.user.img_src.url,
            'tableObjects': tableObjects,
            'usersSection': usersSection,
            'section': section,
            'notification_numbers': number_of_notifications
            }
        return render(req, 'home.html' , context)
       
    else:
         return redirect('/')

def logouthandle(req):
    logout(req)
    return redirect('/')

def profilepage(req):
    if req.user.is_authenticated:
        yourFeed = PhotoUpload.objects.filter(user_name = req.user.username).order_by('-id')
        context = {
            'username': req.user.username,
            'fname': req.user.first_name,
            'lname': req.user.last_name,
            'imgsrc' : req.user.img_src.url,
            'yourFeed': yourFeed,
            'section': req.user.section,
            'bio': req.user.bio
        }
        if req.method == 'POST':
            logout(req)
            return redirect('/')
      
        

        


        return render(req, 'profile.html', context)
    else:
        return redirect('/')

def uploadpage(req):
    if req.method == 'GET':
        if req.user.is_authenticated:
            return render(req, 'upload.html')
        else:
            return redirect('/')
    elif req.method == 'POST':
        user_name = req.user.username
        user_img_url = req.user.img_src.url
        section = req.user.section
        photo_url = req.POST['url']
        global photo_id
        photo_id = photo_id + 1
        photostr = photo_url.split(';base64,')[1]
        photofile = ContentFile(base64.b64decode(photostr), f'{user_name}_memories.png')
        caption = req.POST.get('caption')
        caption_split = caption.split(' ')
        new_word_caption = []
        for word in caption_split:
            if word.startswith('@'):
                index = word.index("@")
                api = word[index+1: len(word)]
            
                if req.user.username != api:
                    notification = Notification(for_user = api, notification = f"<a href = 'profile/{req.user.username}'>@{req.user.username}</a> have mentioned you in their recent post" , notification_img_src = f"{photo_url}", notify = True )
                    notification.save()
                    link = '<a href = "{url "profile_one" {{api}} }">{{word}}</a>'
                    #link = f'<a href = "/profile/{api}">{word}</a>'
                    
                elif req.user.username == api:
                    link = f'<a href = "/profile">{word}</a>'
                
                new_word_caption.append(link)
            else:
                new_word_caption.append(word)
        
        new_caption = " ".join(new_word_caption)



        photoupload = PhotoUpload(photo_id = photo_id, user_name = user_name, user_img_url = user_img_url , section = section , photo =  photofile, caption = new_caption)
        photoupload.save()

        return redirect(f'/home/{req.user.section}')
    
def other_profile(req, user_name):
    if req.method == 'GET':
        if req.user.is_authenticated:
            this_user = User.objects.filter(username = user_name)
            this_user_uploads = PhotoUpload.objects.filter(user_name = user_name).order_by('-id')

            context = {
                'fname': this_user[0].first_name,
                'lname':  this_user[0].last_name,
                'username': this_user[0].username,
                'profileimg': this_user[0].img_src.url,
                'section':  this_user[0].section,
                'this_user_uploads': this_user_uploads
               
            }
            return render(req , "userprofile.html" , context)

def commentpage(req):
    if req.method == "POST":
        photoid = req.POST.get('photoid')
        photourl = req.POST.get('photourl')
        photouser = req.POST.get('photouser')
        userimage = req.POST.get('userimage')
        candelete = False
        if photouser == req.user.username:
            candelete = True
        commentdb = Comments.objects.filter(commenting_photo_url = photourl).order_by('-id')
        context = {
            'photourl': photourl,
            'photouser':photouser,
            'userimage': userimage,
            'username': req.user.username,
            'commentdb': commentdb,
            'candelete': candelete,
            'photoid': photoid
        }

        return render(req, "photocomments.html", context)

def makecomments(req):

    if req.method == 'POST':
        photouser = req.POST.get('photouser')
        commenting_user = req.POST.get('commenting_user')
        commenting_photo_url = req.POST.get('commenting_photo_url')
        comment = req.POST.get('comment')
        a = comment.split(" ")
        new_word_array = []

        for words in a:
            if words.startswith("@"):
                index = words.index("@")
                api = words[index+1: len(words)]
                
                if req.user.username != api:
                    notification = Notification(for_user = api, notification = f"<a href = 'profile/{req.user.username}'>@{req.user.username}</a> have mentioned you in comment on the post of <a href = 'profile/{photouser}'>@{photouser}</a>" , notification_img_src = commenting_photo_url, notify = True )
                    notification.save()
                    link = f"<a href = /profile/{api}>{words}</a>"
                elif req.user.username == api:
                    link = f"<a href = /profile>{words}</a>"
                
                
                new_word_array.append(link)
            else:
                new_word_array.append(words)
        
        modified_comment = " ".join(new_word_array)

        global i
        i += 1
        com = Comments(comment_id = i, commenting_user_url = req.user.img_src.url, commenting_user = commenting_user, commenting_photo_url= commenting_photo_url, comment = modified_comment, date = datetime.datetime.now() )
        com.save()
        comments_return = Comments.objects.values().filter(commenting_photo_url = commenting_photo_url).order_by('-id')
        return JsonResponse({'commenting_user': list(comments_return)})
    
    if req.method == 'GET':
        commenting_user = req.GET.get('commenting_user')
        commenting_photo_url = req.GET.get('commenting_photo_url')
        comment = req.GET.get('comment')
        comments_return = Comments.objects.values().filter(commenting_photo_url = commenting_photo_url)
        return JsonResponse({'commenting_user': list(comments_return)})    
    
   
    
def makereply(req):
    if req.method == 'POST':
        
        commentId = req.POST.get('commentId')
        print(commentId)
        replyingUser = req.POST.get('replying_user')
        replyingUserReply = req.POST.get('replying_user_reply')
        

        thisjson = {
            'replyingUser': replyingUser, 
            'replyingUserReply':replyingUserReply
            }
        
        #cInstance = None
        
        cInstance = Comments.objects.get(comment_id = commentId)
        cInstance.replies += json.dumps(thisjson)+'},'
        cInstance.save()
        
        return JsonResponse({'all_replies': cInstance.replies})


def suggestions(req):

     if req.method == "POST":
       
       users_suggest = User.objects.values().filter(username__startswith = req.POST.get('search'))

       return JsonResponse({'data': list(users_suggest)})
        

def notificationhandler(req):
    if req.method == 'GET':
        if req.user.is_authenticated:
            user_notification = Notification.objects.filter(for_user = req.user.username)
            for noti in user_notification:
                if noti.notify == True:
                    noti.notify = False
                    noti.save()
            
            
            context = {
                'username': req.user.username,
                'notifications': user_notification
            }
            return render(req, 'notification.html', context)

user = None
photoupload = None
def editprofilepage(req):
   
    if req.method == 'GET':
        if req.user.is_authenticated:
            context = {
                'profileImage': req.user.img_src.url,
                'username': req.user.username,
                'fname': req.user.first_name,
                'lname': req.user.last_name,
                'bio': req.user.bio
            }
            global user
            global photoupload
            user = User.objects.get(username = req.user.username)
            photoupload = PhotoUpload.objects.filter(user_name = req.user.username )
            return render(req, "editpage.html", context)
    if req.method == 'POST':
        fname = req.POST.get('fname')
        lname = req.POST.get('lname')
        username = req.POST.get('username')
        croppedUser = req.POST.get('imgurl')
        bio = req.POST.get('bio')

        
        user.first_name = fname
        user.last_name = lname
        user.username = username
        user.bio = bio

        if croppedUser != '':
            user.img_src = base64_to_image(croppedUser)
        
        user.save()
        for photo in photoupload:
            photo.user_name = username
            photo.save()

        return redirect('/profile')

def deletephoto(req):
    if req.method == 'POST':
        thisinstance = req.POST.get('photoid')
        thisphoto = PhotoUpload.objects.filter(photo_id = thisinstance)
        print(thisphoto)
        thisphoto.delete()
        return redirect('/profile')

def deletecomment(req):
    if req.method == 'POST':
        comment = req.POST.get('comment')
        commenting_photo_url = req.GET.get('commenting_photo_url')
        com = Comments.objects.filter(comment = comment)
        com.delete()
       
        comments_return = Comments.objects.values().filter(commenting_photo_url = commenting_photo_url)
        return JsonResponse({'commenting_user': list(comments_return)})

def credits(req):
    return render(req, 'credits.html')
        


