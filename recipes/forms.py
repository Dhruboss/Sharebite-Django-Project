from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'prep_time', 
                  'cook_time', 'servings', 'difficulty', 'image', 'leftover_friendly', 
                  'waste_reduction_tip']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'rows': 6, 'class': 'form-control', 
                                                  'placeholder': 'Enter each ingredient on a new line'}),
            'instructions': forms.Textarea(attrs={'rows': 8, 'class': 'form-control', 
                                                   'placeholder': 'Enter step-by-step instructions'}),
            'waste_reduction_tip': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class RecipeSearchForm(forms.Form):
    query = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Search recipes...',
            'class': 'form-control'
        })
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'All Difficulties')] + list(Recipe.DIFFICULTY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    leftover_friendly = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

