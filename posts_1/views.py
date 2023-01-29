from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post,Comment
from .serializers import PostSerializer,OwnerSerializer,CommentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import mixins
from rest_framework import generics
from .permissions import IsOwnerPermission
from rest_framework import viewsets


User = get_user_model()
#easy => hard

#[classed based with SpecificGenericAPIView ]

class PostListCreateAPIView(generics.ListCreateAPIView):
    # only the first time will list all 
    queryset = Post.objects.all()
    serializer_class =PostSerializer

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class =PostSerializer
    permission_classes = (IsAuthenticated,)

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class =PostSerializer

class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class =PostSerializer

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class =PostSerializer
    permission_classes = (IsAuthenticated,IsOwnerPermission,)

class PostDestroyView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class =PostSerializer    

class OwnerDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class =OwnerSerializer

class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class =CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

##############################################################################

#[classed based with GenericAPIView and mixins]

# class PostMixinListView(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class =PostSerializer

#     def get(self,request,pk=None,*args,**kwargs):
#         return self.list(self,request,pk=None,*args,**kwargs)

#     def post(self,request,pk=None,*args,**kwargs):
#         return self.create(self,request,pk=None,*args,**kwargs)

##############################################################################

#[classed based with APIView]


#Create your views here. all in CRUD+L
# class PostAPIView(APIView):
#     permission_classes = (AllowAny,)
#     def get(self,request,pk=None,*args,**kwargs):

#         queryset = Post.objects.all()
#         serializer = PostSerializer(queryset,many =True) # true because parsing many instances to serializer
#         return Response(serializer.data)

#     def post (self,request,*args,**kwargs):
#         serializer = PostSerializer(data = request.data) # not only for post method
#         if serializer.is_valid():#use valid only if one instance 
#             serializer.save()
#             return Response(serializer.data,status = HTTP_201_CREATED)
#         return Response(serializer.errors,status = HTTP_400_BAD_REQUEST)

#     def put(self,request,pk=None,*args,**kwargs):
#         post = Post.objects.get(pk =pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status = HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk=None,*args,**kwargs):
#         post = Post.objects.get(pk =pk)
#         post.delete()
#         return Response(status =HTTP_204_NO_CONTENT)



##############################################################################

#[function based]

# @csrf_exempt
# def post_list(request):
#     if request.method == 'GET':
#         queryset = Post.objects.all()
#         serializer = PostSerializer(queryset,many =True) 
#         return JsonResponse(serializer.data,safe =False) #orderdict

#     if request.method == 'POST':
#         data = JSONParser.parse(request)
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data,status=201) #orderdict
#         return JsonResponse(serializer.errors, status=400) #orderdict


# @csrf_exempt
# def post_detail(request,pk):

#     try:
#         post = Post.objects.get(pk =pk)
    
#     except Post.DoesNotExist:
#         return HttpResponse(status = 404)

#     if request.method == 'GET':
#         serializer = PostSerializer(post) 
#         return JsonResponse(serializer.data) #orderdict

#     elif request.method == 'PUT':
#         data = JSONParser.parse(request)
#         serializer = PostSerializer(post, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400) #orderdict

#     elif request.method == 'DELETE':
#         post.delete()
#         return HttpResponse(status = 204)




# not discussed with decorators
# @api_view(['GET','POST'])
# def post_list(request):
#     if request.method == "GET":
#         pass