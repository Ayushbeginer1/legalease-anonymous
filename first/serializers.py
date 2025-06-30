from rest_framework import serializers
from .models import AnonymousTip
class AnonymousTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousTip
        fields = '__all__'