from django import forms
from recipe.models import MAX_LENGTH, Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "url", "comments"]
