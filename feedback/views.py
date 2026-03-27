from django.shortcuts import render
#from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import FeedbackForm, FeedbackCommentFormSet  
from .models import Feedback

def feedback_post(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        form_table = FeedbackCommentFormSet(request.POST)
        if form.is_valid():
            feedback = Feedback(
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email'],
                # comment = form.cleaned_comment(form)
                comment = form.cleaned_data['comment']
            )
            feedback = feedback.save()
            table = form_table.save(commit=False)
            for item in table:
                item.feedback = feedback
                item.save()

            return HttpResponse("Спасибо за ваш отзыв!")
        else:
            return render(request, 'feedback.html', {'form': form, 'form_table':form_table})
    else:
        form = FeedbackForm()
        form_table = FeedbackCommentFormSet()

    return render(request, 'feedback.html', {'form': form, 'form_table':form_table})

def feedback_edit(request, pk):
    feedback = Feedback.objects.get(pk=pk)
    if request.method == 'POST':
        form = FeedbackForm(request.POST,instance=feedback)
        form_table = FeedbackCommentFormSet(request.POST,instance=feedback)
        if form.is_valid() and form_table.is_valid():
            feedback = form.save()
            table = form_table.save(commit=False)
            for item in table:
                item.feedback = feedback
                item.save()

            for item in form_table.deleted_objects:
                item.delete()
        
            return HttpResponse("Редактирование завешено!")
    
    form = FeedbackForm(instance=feedback)
    form_table = FeedbackCommentFormSet(instance=feedback)
    return render(request, 'feedback.html', {'form': form, 'form_table':form_table})
        
