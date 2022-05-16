from multiprocessing.connection import Client
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe


USERNAME = "testuser"
PASSWORD = "afasfsadf876868(/&(/&(/&/("

RECIPES = [
    {
        "url": "https://www.k-ruoka.fi/reseptit/liha-makaronilaatikko",
        "comments": "Varsin maukasta",
        "title": "Liha-makaronilaatikko",
    },
    {
        "url": "https://www.valio.fi/reseptit/kaalilaatikko-1/",
        "comments": "Hieman yököttävää",
        "title": "Kaalilaatikko",
    },
]


def create_user(username=USERNAME, password=PASSWORD):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()


def login(client: Client):
    client.login(username=USERNAME, password=PASSWORD)


def create_recipe(title: str, url: str, comments: str):
    return Recipe.objects.create(url=url, title=title, comments=comments)


def create_recipe_by_index(index: int):
    recipe = RECIPES[index]
    return create_recipe(
        title=recipe["title"], url=recipe["url"], comments=recipe["comments"]
    )


class RecipeIndexViewTests(TestCase):
    def setUp(self):
        create_user()
        login(self.client)

    def test_no_recipes(self):
        response = self.client.get(reverse("recipe:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes available.")
        self.assertQuerysetEqual(response.context["recipe_list"], [])

    def test_single_recipe(self):
        recipe = create_recipe_by_index(0)
        response = self.client.get(reverse("recipe:index"))
        self.assertQuerysetEqual(
            response.context["recipe_list"],
            [recipe],
        )

    def test_two_recipes(self):
        recipe0 = create_recipe_by_index(0)
        recipe1 = create_recipe_by_index(1)
        response = self.client.get(reverse("recipe:index"))
        self.assertQuerysetEqual(
            response.context["recipe_list"],
            [recipe1, recipe0],
        )


class RecipeDetailViewTests(TestCase):
    def setUp(self):
        create_user()
        login(self.client)

    def test_recipe_not_exist(self):
        url = reverse("recipe:detail", kwargs={"pk": 123})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_existing_recipe(self):
        recipe = create_recipe_by_index(0)
        url = reverse("recipe:detail", kwargs={"pk": recipe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, recipe.title)
        self.assertContains(response, recipe.comments)
