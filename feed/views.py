from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def api_post_list(request):
    """
    List all posts in JSON format.
    """
    posts = Post.objects.all().order_by('-date_posted')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)