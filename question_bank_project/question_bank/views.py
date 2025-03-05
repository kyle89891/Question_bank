from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.shortcuts import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm



#user  signup

def add_show(req):
    if req.method=="POST":
        fm=Signup(req.POST)
        if fm.is_valid():
            fm.save()
            fm=Signup()
    else:
        fm=Signup()
    stud=User.objects.all() #show fetch data into same time in template 

    return render(req,'question_bank/add.html',{'form':fm,'stu':stud}) 




#user login

def login_view(request):
    if request.method == 'POST':
        fm=AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            passw = fm.cleaned_data['password']
            user = authenticate(username=uname, password=passw)
            if user is not None:
                login(request, user)
                return redirect('submit_answers')
    else:
        fm = AuthenticationForm()
    return render(request, 'question_bank/login.html', {'form': fm})
    

#user logout     

def logout_page(req):
    logout(req)
    return redirect('login')





#questions
@login_required(login_url='/login')
def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_forms = OptionForm(request.POST)
        ##print(dict(option_forms.data))
        option_forms = [OptionForm(request.POST, prefix=str(i)) for i in range(3)]  # Create three OptionForm instances
        if question_form.is_valid() and all(option_form.is_valid() for option_form in option_forms):
            question = question_form.save()
            for option_form in option_forms:
                option = option_form.save(commit=False)
                option.question = question
                option.save()
            return redirect('submit_answers')

    else:
        question_form = QuestionForm()
        option_forms = [OptionForm(prefix=str(i)) for i in range(3)]  # Create three empty OptionForm instances
    stud=Question.objects.all()
    return render(request, 'question_bank/question_form.html', {'question_form': question_form, 'option_forms': option_forms,'stud':stud})


@login_required(login_url='/login')
def question_detail(request, pk):
    # question = get_object_or_404(Question, pk=pk)
    # return render(request, 'question_bank/question_detail.html', {'question': question,})

    question_instance = None
    
    if pk:
        question_instance = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question_instance)
        option_forms = [OptionForm(request.POST, prefix=str(i), instance=question_instance.option_set.all()[i]) for i in range(3)]
        
        if question_form.is_valid() and all(option_form.is_valid() for option_form in option_forms):
            question = question_form.save()
            for i, option_form in enumerate(option_forms):
                option = option_form.save(commit=False)
                option.question = question
                option.save()
            return redirect('question_detail', pk=question.pk)
    else:
        question_form = QuestionForm(instance=question_instance)
        option_forms = [OptionForm(prefix=str(i), instance=question_instance.option_set.all()[i] if question_instance else None) for i in range(3)]
    
    return render(request, 'question_bank/question_detail.html', {'question_form': question_form, 'option_forms': option_forms,})

def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('submit_answers')  # Redirect to home or any other appropriate URL
    return render(request, 'question_bank/question_confirm_delete.html', {'question': question})





#this function will delete
@login_required(login_url='/login')
def delete_data(req,id):
    if req.method=='POST':
        pi=User.objects.get(pk=id)
        pi.delete()
        return  HttpResponseRedirect('/')
    
#this function will update data
    

@login_required(login_url='/login')
def update_data(req,id):
    if req.method=='POST':
        pi=User.objects.get(pk=id)
        fm=Signup(req.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=User.objects.get(pk=id)
        fm=Signup(instance=pi)
    return render(req,'question_bank/update.html',{'form':fm})






from django.contrib import messages

@login_required(login_url='/login')
def submit_answers(request):
    if request.method == 'POST':
        #print(request.POST.get)
        num_questions = int(request.POST.get('num_questions', 0))
        #print('number of questions:', num_questions)
        max_question_id = 0  

        # Find the maximum question ID
        for key in request.POST.keys():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])  # Extract numerical part of the key
                # print(question_id)
                max_question_id = max(max_question_id, question_id)
        #print(max_question_id)

        total_marks = 0

        # Iterate until the maximum question ID
        for question_id in range(1, max_question_id + 1):
            option_id = request.POST.get(f'question_{question_id}')
            #print(option_id)    

            # Skip processing if no option is selected or if the option selected is 'None'
            if option_id == 'None':
                continue
            try:
                option = Option.objects.get(pk=option_id, question_id=question_id)
            except Option.DoesNotExist:
                messages.error(request, f'Option with ID {option_id} for question {question_id} does not exist.')
                continue 

            if option.is_correct:
                total_marks += 1
            #print(total_marks)
            
            if num_questions<1:
                incorrect=0
            else:
                incorrect=num_questions-total_marks

            # if not incorrect:
            # incorrect=0

            percentage=((total_marks/num_questions)*100)

        return render(request,'question_bank/result.html',{'total':num_questions,'correct':total_marks,
                                                           'wrong':incorrect,'percent':percentage,'score':total_marks})
    else:
        question_form = QuestionForm()
        option_forms = [OptionForm(prefix=str(i)) for i in range(3)]  # Create three empty OptionForm instances
    stud=Question.objects.filter(subject_id=1)
    return render(request, 'question_bank/question.html', {'stud':stud,})



@login_required(login_url='/login')
def submit_answers2(request):
    if request.method == 'POST':
        #print(request.POST.get)
        num_questions = int(request.POST.get('num_questions', 0))
        #print('number of questions:', num_questions)
        max_question_id = 0  

        # Find the maximum question ID
        for key in request.POST.keys():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])  # Extract numerical part of the key
                # print(question_id)
                max_question_id = max(max_question_id, question_id)
        #print(max_question_id)

        total_marks = 0

        # Iterate until the maximum question ID
        for question_id in range(1, max_question_id + 1):
            option_id = request.POST.get(f'question_{question_id}')
            #print(option_id)    

            # Skip processing if no option is selected or if the option selected is 'None'
            if option_id == 'None':
                continue
            try:
                option = Option.objects.get(pk=option_id, question_id=question_id)
            except Option.DoesNotExist:
                messages.error(request, f'Option with ID {option_id} for question {question_id} does not exist.')
                continue 

            if option.is_correct:
                total_marks += 1
            #print(total_marks)
            

            incorrect=num_questions-total_marks

            percentage=((total_marks/num_questions)*100)

        return render(request,'question_bank/result.html',{'total':num_questions,'correct':total_marks,
                                                           'wrong':incorrect,'percent':percentage,'score':total_marks})
    else:
        question_form = QuestionForm()
        option_forms = [OptionForm(prefix=str(i)) for i in range(3)]  # Create three empty OptionForm instances
    stud=Question.objects.filter(subject_id=3)
    return render(request, 'question_bank/question.html', {'stud':stud,})



@login_required(login_url='/login')
def submit_answers3(request):
    if request.method == 'POST':
        #print(request.POST.get)
        num_questions = int(request.POST.get('num_questions', 0))
        #print('number of questions:', num_questions)
        max_question_id = 0  

        # Find the maximum question ID
        for key in request.POST.keys():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])  # Extract numerical part of the key
                # print(question_id)
                max_question_id = max(max_question_id, question_id)
        #print(max_question_id)

        total_marks = 0

        # Iterate until the maximum question ID
        for question_id in range(1, max_question_id + 1):
            option_id = request.POST.get(f'question_{question_id}')
            #print(option_id)    

            # Skip processing if no option is selected or if the option selected is 'None'
            if option_id == 'None':
                continue
            try:
                option = Option.objects.get(pk=option_id, question_id=question_id)
            except Option.DoesNotExist:
                messages.error(request, f'Option with ID {option_id} for question {question_id} does not exist.')
                continue 

            if option.is_correct:
                total_marks += 1
            #print(total_marks)
            

            incorrect=num_questions-total_marks

            percentage=((total_marks/num_questions)*100)

            return render(request,'question_bank/result.html',{'total':num_questions,'correct':total_marks,
                                                           'wrong':incorrect,'percent':percentage,'score':total_marks})
    else:
        question_form = QuestionForm()
        option_forms = [OptionForm(prefix=str(i)) for i in range(3)]  # Create three empty OptionForm instances
    stud=Question.objects.filter(subject_id=2)
    return render(request, 'question_bank/question.html', {'stud':stud,})


####################################################################################
#api 

from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getSub(req):
    if req.method=='GET':
        stu=Subject.objects.all()
        serializer=SubjectSerializers(stu,many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
def getoneSub(req):
    if req.method=='POST':
        subid=req.data.get("id")
        stu=Subject.objects.get(id=subid)
        serializer=SubjectSerializers(stu)
        return Response(serializer.data)
    
@api_view(['POST'])
def addSub(req):
    if req.method=='POST':
        serializer=SubjectSerializers(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"data posted!!"})
        return Response(serializer.errors)
    
#update
# @api_view(['POST'])
# def upt(req):
#     if req.method=='POST':
#         id_obj=req.data.get('id')
#         stu=Subject.objects.get(id=id_obj)
#         serializer=SubjectSerializers(instance=stu,data=req.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':"data posted!!"})
#         return Response(serializer.errors)
    
@api_view(['POST'])
def removesub(req):
    if req.method=='POST':
        subid=req.data.get("id")
        stu=Subject.objects.get(id=subid)
        stu.delete()
        return Response({'msg':"data deleted!!"})
