from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # 오직 쓰기 전용으로 응답에 포함되지 않는 컬럼
    password = serializers.CharField(write_only=True)
    
    # 사용자를 생성 메서드
    def create(self, validated_data):
        user = User.objects.create(


            username=validated_data['username'],
            email=validated_data['email']
        )
        # 비밀번호를 해시 처리해서 저장
        user.set_password(validated_data['password'])
        # 유저 저장
        user.save()
        # 생성된 유저 반환
        return user

    class Meta:
        model = User
        # 직렬화 역직렬화에 포함할 필드 목록
        fields = ['username', 'email', 'password', 'first_name', 'last_name','bio',]