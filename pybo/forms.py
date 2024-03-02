from django import forms
from pybo.models import Question, Answer

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget


class QuestionForm(forms.ModelForm):
    content = forms.CharField(
        label_suffix='',label='',
        widget=CKEditorWidget(
            attrs={
                'class':'form-control',
                'style':'width:100%; height:250%;',
            }
        )
    )


    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content','file_upload']  # QuestionForm에서 사용할 Question 모델의 속성

        labels = {
            'subject': '제목',
            'content': '내용',
            'file_upload':'첨부파일',
        }  


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }