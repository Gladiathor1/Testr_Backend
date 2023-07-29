import csv
import os
from datetime import date,datetime
from django.core.files.storage import FileSystemStorage

from rest_framework import permissions

import logging

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets
from question.models import *
from question.serializers import *

from .mixin import *
from django.http import HttpResponse, HttpResponseRedirect
from .mypermission import IsOwnerOrReadOnly, IsVerifier


class DisciplineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows paper to be viewed or edited.
    """
    queryset = Discipline.objects.all().order_by('-created')
    serializer_class = DisciplineSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows paper to be viewed or edited.
    """
    queryset = Subject.objects.all().order_by('-created')
    serializer_class = SubjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows paper to be viewed or edited.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class PaperViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows paper to be viewed or edited.
    """
    serializer_class = PaperSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Optionally restricts the returned paper to a given code,
        by filtering against a `code` query parameter in the URL.
        """
        code_value = self.request.query_params.get('code')
        if code_value is not None:
            queryset = Paper.objects.filter(code=code_value)
        else:
            queryset = Paper.objects.all().order_by('-created')

        return queryset


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows paper to be viewed or edited.
    """
    queryset = Tag.objects.all().order_by('-created')
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows paper to be viewed or edited.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class QuestionViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """
    queryset = Question.objects.all().order_by('-created')
    read_serializer_class = QuestionReadSerializer
    write_serializer_class = QuestionWriteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)



    def get_queryset(self):
        """
        Optionally restricts the returned paper to a given code,
        by filtering against a `code` query parameter in the URL.
        """
        ys = self.request.query_params.get('ys')
        ye = self.request.query_params.get('ye')
        mtag = self.request.query_params.get('tag')
        mdis = self.request.query_params.get('discipline')
        msub = self.request.query_params.get('subject')
        mses = self.request.query_params.get('session')
        mtype = self.request.query_params.get('type')
        mdiff = self.request.query_params.get('difficulty')

        queryset = Question.objects.all()
        queryset = queryset.filter(verify__icontains='Published',)
        if ys is not None:
            queryset = queryset.filter(paper__year__gte=ys, )
        if ye is not None:
            queryset = queryset.filter(paper__year__lte=ye, )
        if mtag is not None:
            if "," in mtag:
                mmtag = mtag.split(",")
            else:
                mmtag = [mtag]

            queryset = queryset.filter(tag__name__in=mmtag, )
            queryset = queryset.distinct()

        if mdis is not None:
            if "," in mdis:
                mmdis = mdis.split(",")
            else:
                mmdis = [mdis]
            queryset = queryset.filter(discipline__title__in=mmdis, )
            queryset = queryset.distinct()

        if msub is not None:
            if "," in msub:
                mmsub = msub.split(",")
            else:
                mmsub = [msub]

            queryset = queryset.filter(subject__title__in=mmsub, )
            queryset = queryset.distinct()

        if mses is not None:
            if "," in mses:
                mmses = mses.split(",")
            else:
                mmses = [mses]

            queryset = queryset.filter(paper__session__in=mmses, )
            queryset = queryset.distinct()

        if mtype is not None:
            if "," in mtype:
                mmtype = mtype.split(",")
            else:
                mmtype = [mtype]

            queryset = queryset.filter(type__in=mmtype, )
            queryset = queryset.distinct()

        if mdiff is not None:
            if "," in mdiff:
                mmdiff = mdiff.split(",")
            else:
                mmdiff = [mdiff]
            queryset = queryset.filter(difficulty__in=mmdiff, )
            queryset = queryset.distinct()

        return queryset


class myQuestionViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows questions to be viewed or edited.
    """
    queryset = Question.objects.all().order_by('-created')
    read_serializer_class = QuestionReadSerializer
    write_serializer_class = QuestionWriteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Question.objects.filter(author=user)


class VerfierViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows paper to be viewed or edited.
    """
    queryset = Question.objects.filter(verify="In review")
    read_serializer_class = QuestionReviewSerializer
    write_serializer_class = QuestionWReviewSerializer
    permission_classes = (permissions.IsAuthenticated, IsVerifier)


def upload_csv(request):
    # print("here")
    data = {}
    if "GET" == request.method:
        # print("get")
        return render(request, "index.html", data)
    # if not GET, then proceed
    try:
        # print("try1")
        # print(request.FILES["csv_file"])
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            # print("not a csv file")
            return HttpResponseRedirect(reverse("upload_csv"))

        myfile = request.FILES['csv_file']
        fs = FileSystemStorage(location='./CSV_Files')
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S-")
        filename = fs.save(dt_string+myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # print(dt_string+myfile.name)
        # print('./CSV_Files'+uploaded_file_url)


        # save_path = './CSV_Files'
        # if not os.path.exists(save_path):
        #     os.makedirs(save_path)
        # file_name = str(request.FILES["csv_file"])
        # fn = file_name.split(".")
        # completeName = os.path.join(save_path, file_name)
        # now = datetime.now()
        # dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        # print(dt_string)
        # newName = save_path + "/" + dt_string + "." +  fn[1]
        # file1 = open(completeName, "w")
        #
        # file1.close()
        # os.rename(completeName, newName)
        # print(completeName)
        # print(newName)

        # csv_file = request.FILES["csv_file"]

        #if file is too large, return
        # if csv_file.multiple_chunks():
        #     messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        #     return HttpResponseRedirect(reverse("upload_csv"))

        with open('./CSV_Files/'+dt_string+myfile.name) as f:
            reader = csv.reader(f)
            for row in reader:

                try:

                    s = Subject.objects.get(title=row[5])
                    d = Discipline.objects.get(title=row[6])

                    form = Paper(discipline=d, subject=s, year=row[4], session=row[3], code=row[7],
                                 title=row[1],file_name=row[2])
                    # if form.is_valid():
                    form.save()
                    # else:
                    #     logging.getLogger("error_logger").error(form.errors.as_json())
                    # print(fields[7])
                    # print(type(fields[7]))
                    # print(len(fields[7]))
                    # print(len(fields[7][:-1]))c
                    # print(len("Alevel"))
                    # print(fields[7][:-1]=="Alevel" or fields[7][:-1]=="Olevel")
                    # print(d)
                except Exception as e:
                    logging.getLogger("error_logger").error(repr(e))
                    pass

            # print("done")

        # file_data = csv_file.read().decode("utf-8")
        #
        # lines = file_data.split("\n")
        # #loop over the lines and save them in db. If error , store as string and then display
        # for line in lines:
        #     fields = line.split(",")
        #     s= Subject.objects.get(title=fields[5])
        #     d = Discipline.objects.get(title=fields[6][:-1])
        #     # d = Discipline.objects.all()
        #     # s = Subject.objects.all()
        #     try:
        #
        #         form = Paper(discipline=d,subject=s,year=fields[4],session=fields[3],code=fields[2],title=fields[1])
        #         # if form.is_valid():
        #         form.save()
        #         # else:
        #         #     logging.getLogger("error_logger").error(form.errors.as_json())
        #         # print(fields[7])
        #         # print(type(fields[7]))
        #         # print(len(fields[7]))
        #         # print(len(fields[7][:-1]))c
        #         #print(len("Alevel"))
        #         # print(fields[7][:-1]=="Alevel" or fields[7][:-1]=="Olevel")
        #         # print(d)
        #     except Exception as e:
        #         logging.getLogger("error_logger").error(repr(e))
        #         pass
        # csv_file.close()
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("upload_csv"))



def delete_all(request):
    Paper.objects.all().delete()
    return HttpResponse('success')

def upload_tags(request):
    # print("here")
    data = {}
    if "GET" == request.method:
        # print("get")
        return render(request, "tags.html", data)
    # if not GET, then proceed
    try:
        # print("try1")
        # print(request.FILES["csv_file"])
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            # print("not a csv file")
            return HttpResponseRedirect(reverse("upload_tags"))

        myfile = request.FILES['csv_file']
        fs = FileSystemStorage(location='./CSV_Files')
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S-")
        filename = fs.save(dt_string+myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # print(dt_string+myfile.name)
        # print('./CSV_Files'+uploaded_file_url)


        # save_path = './CSV_Files'
        # if not os.path.exists(save_path):
        #     os.makedirs(save_path)
        # file_name = str(request.FILES["csv_file"])
        # fn = file_name.split(".")
        # completeName = os.path.join(save_path, file_name)
        # now = datetime.now()
        # dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        # print(dt_string)
        # newName = save_path + "/" + dt_string + "." +  fn[1]
        # file1 = open(completeName, "w")
        #
        # file1.close()
        # os.rename(completeName, newName)
        # print(completeName)
        # print(newName)

        # csv_file = request.FILES["csv_file"]

        #if file is too large, return
        # if csv_file.multiple_chunks():
        #     messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        #     return HttpResponseRedirect(reverse("upload_tags"))
        with open('./CSV_Files/'+dt_string+myfile.name) as f:
            reader = csv.reader(f)
            for row in filter(None, reader):

                try:


                    s = Subject.objects.get(title=row[1])

                    form = Tag(name=row[0], subject=s,)
                    # if form.is_valid():
                    form.save()
                    # else:
                    #     logging.getLogger("error_logger").error(form.errors.as_json())
                    # print(fields[7])
                    # print(type(fields[7]))
                    # print(len(fields[7]))
                    # print(len(fields[7][:-1]))c
                    # print(len("Alevel"))
                    # print(fields[7][:-1]=="Alevel" or fields[7][:-1]=="Olevel")
                    # print(d)
                except Exception as e:
                    logging.getLogger("error_logger").error(repr(e))
                    pass

            # print("done")

        # file_data = csv_file.read().decode("utf-8")
        #
        # lines = file_data.split("\n")
        # #loop over the lines and save them in db. If error , store as string and then display
        # for line in lines:
        #     fields = line.split(",")
        #     s= Subject.objects.get(title=fields[5])
        #     d = Discipline.objects.get(title=fields[6][:-1])
        #     # d = Discipline.objects.all()
        #     # s = Subject.objects.all()
        #     try:
        #
        #         form = Paper(discipline=d,subject=s,year=fields[4],session=fields[3],code=fields[2],title=fields[1])
        #         # if form.is_valid():
        #         form.save()
        #         # else:
        #         #     logging.getLogger("error_logger").error(form.errors.as_json())
        #         # print(fields[7])
        #         # print(type(fields[7]))
        #         # print(len(fields[7]))
        #         # print(len(fields[7][:-1]))c
        #         #print(len("Alevel"))
        #         # print(fields[7][:-1]=="Alevel" or fields[7][:-1]=="Olevel")
        #         # print(d)
        #     except Exception as e:
        #         logging.getLogger("error_logger").error(repr(e))
        #         pass
        # csv_file.close()
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("upload_tags"))