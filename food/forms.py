from django import forms
from .models import FoodItem, Category


class FoodItemForm(forms.ModelForm):
    expiry_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = FoodItem
        fields = ['title', 'description', 'category', 'quantity', 'expiry_date',
                  'dietary_tags', 'image', 'pickup_location', 'instructions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'pickup_location': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }


class FoodSearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search food items...',
        'class': 'form-control'
    }))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    dietary_tags = forms.ChoiceField(choices=FoodItem.DIETARY_TAGS, required=False)