from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # post는 외래키로 적어줄 수 없기에 설정
        read_only_fields = ('post',)
        
    def to_representation(self, instance):
        # 상속받은 클래스의 오버라이딩
        ret =  super().to_representation(instance)
        ret.pop('post')
        return ret
    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        # ManyToMany 관계인 컬럼으로 읽기 전용으로 설정
        read_only_fields = ('like_users',)
        
class PostDetailSerializer(PostSerializer):
    # 댓글은 모두 읽기전용으로 설정
    # 상세 페이지에서 해당 글의 댓글을 조회할 수 있게 분할, 여러 개의 댓글이 있을 수 있기에 many = True 설정
    comments = CommentSerializer(many = True, read_only = True)
    comments_count = serializers.IntegerField(source = 'comments.count', read_only = True)
    read_only_fields = ()