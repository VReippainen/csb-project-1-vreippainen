from django import forms
from recipe.models import MAX_LENGTH, Recipe
from django.core.validators import URLValidator


class RecipeForm(forms.ModelForm):
    # FLAW 1: Fixed by validating the url
    # url = forms.URLField(label="URL", required=True)
    # javascript:alert(document.cookie)
    class Meta:
        model = Recipe
        fields = ["title", "url", "comments"]
