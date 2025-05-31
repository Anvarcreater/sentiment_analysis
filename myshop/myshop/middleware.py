from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthUserMiddle:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        # check user is authenticated
        if request.user.is_authenticated:
            # list of path to check
            path_to_redirect=[reverse('myshop:login'),reverse('myshop:signup')]

            if request.path in path_to_redirect:
                return redirect(reverse('myshop:home'))  # redirected to home page
        res=self.get_response(request)
        return res
    
class RedirectNonAuthUserMiddle:

    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):

        path=[reverse('myshop:dashboard')]

        if not request.user.is_authenticated and request.path in path:
            return redirect(reverse('myshop:login'))
        res=self.get_response(request)
        return res

          