from django.shortcuts import redirect


class UsersPermissions():
    
    def __init__(self, get_response):
        self.get_response=get_response


    def __call__(self, request):
        #if str(request.user) != 'AnonymousUser' :
        response=self.get_response(request)
        return response
    

#Se ejecuta antes y despues 

    def process_view(self, request, view_fun, view_args, view_kwargs):
        if str(request.user) != 'AnonymousUser' :
            if str(request.path).startswith('/accounts/login'):
                return redirect('/')
        else:
            if str(request.path).startswith('/accounts'):
                return None
            else:
                return redirect('/accounts/login/')
