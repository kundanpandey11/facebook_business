from django.shortcuts import render
# from .scrap_facebook import get_all_page_url, get_comments_form_page_url
from .models import UserModel, CreateRequest
from utilities.scrap_facebook import get_comments_form_page_url


# def get_page_url(request):
#     if request.user.is_authenticated:
#         username = request.user.username

#         # get json file created and saved in the usermodel
#         json_file = get_all_page_url(username=username)
#         usermodel = UserModel()
#         usermodel.user = request.user
#         usermodel.page_url_json = json_file
#         usermodel.save()
#         return render(request, "index.html", {'username':username})
#     else: 
#         return render(request, 'login.html')

amitabh = "https://www.facebook.com/amitabhbachchan"

def get_page_url(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else: 
        return render(request, 'login.html')

def sentiment_and_graph(request):
    url = request.POST.get('URL')


#page_url, name
#create a request 
def create_request(request):
    if request.method == "POST":
        name = request.POST['name']
        # email = request.POST['user-email']

        page_url = request.POST['page_url']
        post_count = request.POST['post_count']
        print(name, page_url, post_count)
        # req = CreateRequest(
        #     name=name, 
        #     page_url = page_url, 
        #     post_count =post_count

        # )
        # req.save()
        render(request, "request_accepted.html")
        return get_comments_form_page_url(page_url=page_url, name=name, post_count=int(post_count))
        # return 
    else:
        return render(request, "create_request.html")
    
    


    
