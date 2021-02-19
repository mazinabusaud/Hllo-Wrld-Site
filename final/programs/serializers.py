from programs.models import Program, ProgramCategory
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        user = UserSerializer()
        model = Program
        fields = '__all__'

class ProgramCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProgramCategory
        fields = '__all__'
