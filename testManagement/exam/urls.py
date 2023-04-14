from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.index,name="home"),
    path("signup",views.signupUser,name="signup"),
    path("login",views.loginUser,name="login"),
    path("logout",views.logoutUser,name="logout"),
    path("signup/student",views.studentSignup,name="studentSignup"),    
    path("signup/teacher",views.teacherSignup,name="teacherSignup"),
    path("uploadtest",views.uploadtest,name="uploadtest"),
    path("studentview",views.studentview,name="studentview"),    
    path("teacherview",views.teacherview,name="teacherview"),
    path("delete/<int:id>",views.delete,name="delete")
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)