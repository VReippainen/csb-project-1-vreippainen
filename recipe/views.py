from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from recipe.forms import RecipeForm
from recipe.models import Recipe, Profile
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from recipe.utils.scraper import scrape_reciped
import logging


def get_active_recipes():
    return Recipe.objects.filter(active=True).order_by("-updated_at")


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "recipe/index.html"
    context_object_name = "recipe_list"

    def get_queryset(self):
        """
        Returns active recipes sorter by update date.
        """
        return get_active_recipes().order_by("-updated_at")


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Recipe
    template_name = "recipe/detail.html"
    logger = logging.getLogger(__name__)

    def get_queryset(self):
        """
        Excludes inactive recipes.
        """
        return get_active_recipes()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = context["object"].url
        try:
            metadata = scrape_reciped(url)
            context["metadata"] = metadata
        except:
            self.logger.warning("Scraping following url failed %s" % url)

        return context


@login_required
def edit(request, pk):
    recipe_id = pk
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe.url = form.cleaned_data["url"]
            recipe.title = form.cleaned_data["title"]
            recipe.comments = form.cleaned_data["comments"]
            recipe.save()
            return HttpResponseRedirect(
                reverse("recipe:detail", kwargs={"pk": recipe_id})
            )
    else:
        form = RecipeForm(instance=recipe)
        return render(
            request, "recipe/edit.html", {"form": form, "recipe_id": recipe_id}
        )


@login_required
def add(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, user__pk=request.user.id)
            recipe = Recipe(
                url=form.cleaned_data["url"],
                title=form.cleaned_data["title"],
                updated_by=profile,
                owner=profile,
                comments=form.cleaned_data["comments"],
            )
            recipe.save()
            return redirect("/recipe/%d/detail" % recipe.id)
    else:
        form = RecipeForm()
        return render(request, "recipe/add.html", {"form": form})
