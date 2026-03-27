from django import forms
from .models import Feedback, FeedbackComment
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'comment'] 

        # widgets = {
        #     'number': forms.TextInput(attrs={'class': "form-control"}),
        #     'date': forms.DateInput(attrs={'type': 'date', 'class':"form-control"}),
        # }

        # labels = {
        #     'number': 'Номер документа',
        #     'date': 'Дата документа',
        #     'organization': 'Организация',
        #     'comment': 'Коментарий',
        # }

# class FeedbackForm(forms.Form):
#     name = forms.CharField(
#         max_length=30,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'})
#     )
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
#     )
#     comment = forms.CharField(
#         widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваше сообщение'})
#     )

#     def __init__(self, *args, **kwargs):
#         super(FeedbackForm, self).__init__(*args, **kwargs)
#         self.fields['name'].label = "Имя пользователя"
#         self.fields['email'].label = "Электронная почта"
#         self.fields['comment'].label = "Комментарий"

#     # def clean_comment(self):
#     #     comment = self.cleaned_data.get('comment')
#     #     if Feedback.objects.filter(comment=comment).exists() :
#     #         raise forms.ValidationError("Комментарий такой уже существует.")
#     #     return comment 

class BaseChildrenFormset(BaseInlineFormSet):
    pass

FeedbackCommentFormSet = inlineformset_factory(
    parent_model=Feedback,  # Родительская модель
    model=FeedbackComment,  # Модель, которая будет редактироваться через inline-формы
    formset=BaseChildrenFormset,
    fields='__all__',  # Поля, доступные для изменения
    extra=1,  # Количество дополнительных пустых форм
    #can_delete=True, # Возможность удалять связанные объекты
)