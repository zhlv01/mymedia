from django import forms
from .models import Note
from core.models import Category


class NoteForm(forms.ModelForm):
    title = forms.CharField(label='标题', max_length=255)
    description = forms.CharField(label='描述', widget=forms.Textarea, required=False)
    cover_image = forms.ImageField(label='封面图', required=False)
    category = forms.ModelChoiceField(label='分类', queryset=None, required=False)
    tags = forms.CharField(label='标签', required=False, help_text='多个标签用逗号分隔')
    is_public = forms.BooleanField(label='公开分享', required=False)

    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 20,
                'class': 'form-control',
                'placeholder': '支持 Markdown 语法...'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
        
        if self.instance and self.instance.pk:
            self.fields['title'].initial = self.instance.media_item.title
            self.fields['description'].initial = self.instance.media_item.description
            self.fields['cover_image'].initial = self.instance.media_item.cover_image
            self.fields['category'].initial = self.instance.media_item.category
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.media_item.tags.all()])
            self.fields['is_public'].initial = self.instance.media_item.is_public
