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
                #Validaciones de seguridad
                if str(request.path).startswith('/administrator'):
                    if(request.user.rol.id < 2):
                        return None
                    else:
                        return redirect('/')
                if str(request.path).startswith('/manager'):
                    if(request.user.rol.id < 3):
                        return None
                    else:
                        return redirect('/')
                if str(request.path).startswith('/cashier'):
                    if(request.user.rol.id < 4 ):
                        return None
                    else:
                        return redirect('/')
                if str(request.path).startswith('/api'):
                    if(request.user.rol.id < 4 ):
                        return None
                    else:
                        return redirect('/')
                if str(request.path).startswith('/client'):
                    if(request.user.rol.id < 4 ):
                        return None
                    else:
                        return redirect('/')
        else:
            if str(request.path).startswith('/accounts'):
                return None
            else:
                return redirect('/accounts/login/')

