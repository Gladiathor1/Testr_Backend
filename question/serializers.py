from rest_framework import serializers

import question
from authentication import serializers as user_serializers
from question import models
from django.contrib.auth.models import User
from django.conf import settings



# class UserSerializer(serializers.ModelSerializer):
#    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
#
#     class Meta:
#         model = User
#         # model = settings.AUTH_USER_MODEL
#         fields = ['id', 'username']

# class UserSerializer(serializers.ModelSerializer):
#     # questions = serializers.PrimaryKeyRelatedField(many=True, queryset=question.models.Question.objects.all())
#
#     class Meta:
#         model = settings.AUTH_USER_MODEL
#         fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = "__all__"


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discipline
        fields = ['id', 'title']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ['id', 'title']


class PaperSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    discipline = DisciplineSerializer()
    class Meta:
        model = models.Paper
        fields = ['id', 'discipline', 'subject', 'year', 'session', 'code', 'title']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'name', 'subject']


class QuestionReadSerializer(serializers.ModelSerializer):
    paper = PaperSerializer()
    tag = TagSerializer(many=True)
    subject = SubjectSerializer()
    discipline = DisciplineSerializer()
    author = user_serializers.UserSerializer()
    aimage = ImageSerializer(many=True)
    qimage = ImageSerializer(many=True)
    verifier = user_serializers.UserSerializer()

    class Meta:
        model = models.Question
        fields = ['id', 'paper', 'name', 'description', 'answer', 'difficulty', 'created', 'tag', 'subject',
                  'discipline', 'type', 'author','aimage','qimage','verify','verifier']


class QuestionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['id', 'paper', 'name', 'description', 'answer', 'difficulty', 'created', 'tag', 'subject',
                  'discipline', 'type', 'author','aimage','qimage']


class QuestionReviewSerializer(serializers.ModelSerializer):
    paper = PaperSerializer()
    tag = TagSerializer(many=True)
    subject = SubjectSerializer()
    discipline = DisciplineSerializer()
    aimage = ImageSerializer(many=True)
    qimage = ImageSerializer(many=True)
    class Meta:
        model = models.Question
        fields = ['id', 'paper', 'name', 'description', 'answer', 'difficulty', 'created', 'tag', 'subject',
                  'discipline', 'type', 'author','aimage','qimage','verify','verifier']

class QuestionWReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['id', 'paper', 'name', 'description', 'answer', 'difficulty', 'created', 'tag', 'subject',
                  'discipline', 'type', 'author','aimage','qimage','verify','verifier']