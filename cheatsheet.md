### project setup

    [reference]
    https://www.django-rest-framework.org/#installation

    [pip install]
    pip install djangorestframework

    [settings.py]
    INSTALLED_APPS => 'rest_framework'

    REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
    }

    [urls.py]
    path('api-auth/', include('rest_framework.urls'))

### Overview

    [models.py]

        class Post(models.Model):
            title = models.CharField(max_length = 100)
            def __str__(self):
                return self.title

    [serializers.py] (python object => Json & querysets => Json & Json => python objects)

        class PostSerializer(serializers.ModelSerializer):
            class Meta:
                model = Post
                fields = ('title',)

    [views.py]

        class PostView(APIView):
            permission_classes = (AllowAny,)
            def get(self,request,*args,**kwargs):
                queryset = Post.objects.all()
                serializer = PostSerializer(queryset,many =True) # true because parsing many instances to serializer
                return Response(serializer.data)

    [urls.py]

        path('api/posts/', PostView.as_view(),name='post-list')

    [settings.py]

        INSTALLED_APPS = 'posts'

### Serializers part1

![serializae image](https://preview.redd.it/7qj8tye6t7111.png?width=556&format=png&auto=webp&s=662c96d2d49deb4728fd4cb10abea3a9c7da6dd2)

    [additional notes]
    models.CharField(max_length=3,choices = CATEROGY_CHOICES) # will not check in save method

    [python manage.py shell]
    from posts.models import Post
    from posts.serializers import PostSerializer
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser
    post = Post(title="sth new",custom_id =333,category='D')
    post.save()
    serializer = PostSerializer(post)
    serializer.data
    content = JSONRenderer().render(serializer.data) #convert to string
    content#  b'{"title":"sth new","custom_id":333,"category":"Dj"}

    import io
    stream = io.BytesIO(content)
    #convert to data
    data = JSONParser().parse(stream)
    serializer = PostSerializer(data=data)
    serializer.is_valid()
    serializer.validated_data
    serializer.save() # will not be saved it is not valid

### Serializers part2

    [crud under the hood]
        @csrf_exempt
        def post_list(request):
            if request.method == 'GET':
                queryset = Post.objects.all()
                serializer = PostSerializer(queryset,many =True)
                return JsonResponse(serializer.data,safe =False) #orderdict

            if request.method == 'POST':
                data = JSONParser.parse(request)
                serializer = PostSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data,status=201) #orderdict
                return JsonResponse(serializer.errors, status=400) #orderdict


        @csrf_exempt
        def post_detail(request,pk):

            try:
                post = Post.objects.get(pk =pk)

            except Post.DoesNotExist:
                return HttpResponse(status = 404)

            if request.method == 'GET':
                serializer = PostSerializer(post)
                return JsonResponse(serializer.data) #orderdict

            elif request.method == 'PUT':
                data = JSONParser.parse(request)
                serializer = PostSerializer(post, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors, status=400) #orderdict

            elif request.method == 'DELETE':
                post.delete()
                return HttpResponse(status = 204)

    [pip install] # testing just like postman
    pip install httpie

    [cmd]
    http http://127.0.0.1:8000/api/post-list/
    http http://127.0.0.1:8000/api/posts/1/

### Request- response-intro

    [function based]
    from django.http import HttpResponse,JsonResponse
    from rest_framework.parsers import JSONParser
    from rest_framework.renderers import JSONRenderer

### DRF - class based views

    #[classed based with APIView]

    from rest_framework.views import APIView
    from rest_framework.response import Response

### DRF - Mixins

    #[classed based with GenericAPIView and mixins]

    mixins adding generic view

    class PostListView(generics.ListAPIView):

        #get_queryset
        queryset = Post.objects.all()
        serializer_class =PostSerializer

### DRF - Generic

    [classed based with SpecificGenericAPIView ]
    https://testdriven.io/blog/drf-views-part-2/


    rest api: even with same url, there are different http request
    PostListView vs  PostListCreateAPIView has different UI in drf, thus its different.

### DRF - Permissions

    https://stackoverflow.com/questions/44625661/django-how-to-limit-model-list-access-permission-to-its-owner

    [permissions.py]

        class IsOwnerPermission(permissions.BasePermission):

        #(override)
        def has_object_permission(self, request, view, obj):
            print('obj.owner',obj.owner)
            print('request.user',request.user)
            return obj.owner == request.user

    [models.py]
    User =get_user_model()

    class Post(models.Model):
        owner = models.ForeignKey(User,on_delete=models.CASCADE)

    [views.py]
    class PostListView(generics.ListAPIView):
        queryset = Post.objects.all()
        serializer_class =PostSerializer
        permission_classes = (IsAuthenticated,IsOwnerPermission)

### HyperLink

    https://stackoverflow.com/questions/31566675/for-django-rest-framework-what-is-the-difference-in-use-case-for-hyperlinkedrel

    [serializers.py]

    owner = serializers.HyperlinkedRelatedField(queryset = User.objects.all(),view_name='owner-detail',many=False)

    [urls.py]

    path('api/owner/<pk>', OwnerDetailView.as_view(),name='owner-detail'),

    [views.py]

    class OwnerDetailView(generics.RetrieveAPIView):
        queryset = User.objects.all()
        serializer_class =OwnerSerializer

### Routers and viewsets

    ViewSet includes several views in it and it needs to include router

    [views.py]

        class PostViewSet(viewsets.ModelViewSet):
            queryset = Post.objects.all()
            serializer_class = PostSerializer
            permission_classes = (AllowAny,)


    [posts/urls.py]

        router = DefaultRouter()
        router.register('posts',PostViewSet)

        # customize
        post_detail = PostViewSet.as_view({'get':'list','post':'create'})

        urlpatterns = [
            path('',include(router.urls)),
            path('custom/',post_detail,name="custom")
        ]

    [urls.py]

        path('api/',include('posts.urls'))

## Linking to frontend

### List view part 2

    [serializers.py]

    username = serializers.SerializerMethodField()
    def get_username(self, obj):
        return obj.user.username

    not done? does not save, why creating a PostCreateSerializer
    https://stackoverflow.com/questions/63241552/how-to-update-with-serializermethodfield-in-django-rest-framework
    A read-only field that get its representation from calling a method
