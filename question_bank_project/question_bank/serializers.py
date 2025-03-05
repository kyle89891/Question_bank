from rest_framework import serializers
from  .models import *

class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields='__all__'

class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'

class OptionSerializers(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields='__all__'