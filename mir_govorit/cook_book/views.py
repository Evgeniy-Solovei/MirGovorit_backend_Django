from itertools import chain

from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from .models import Product, Recipe, Ingredient


class AddProductToRecipeView(View):
    def get(self, request, recipe_id, product_id, weight):
        # Проверяем все ли параметры переданы в запрос или возвращаем сообщение.
        if not recipe_id or not product_id or not weight:
            return HttpResponseBadRequest("Отсутствуют необходимые параметры.")

        # Пытаемся получить объект рецепта из базы данных или возвращаем ошибку 404.
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # Пытаемся получить объект продукта из базы данных или возвращаем ошибку 404.
        product = get_object_or_404(Product, id=product_id)

        # Пытаемся получить объект ингредиента из базы данных.
        # Если ингредиент уже существует в рецепте, обновляем его вес, иначе создаем новый.
        try:
            ingredient = Ingredient.objects.select_related('product').get(recipe=recipe, product=product)
            ingredient.weight += int(weight)
            ingredient.save()
        except Ingredient.DoesNotExist:
            Ingredient.objects.create(recipe=recipe, product=product, weight=int(weight))

        # Возвращаем успешный HTTP-ответ
        return HttpResponse("Продукт успешно добавлен в рецепт.")


class CookRecipeView(View):
    def get(self, request, recipe_id):
        # Пытаемся получить объект рецепта из базы данных или возвращаем ошибку 404.
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # Получаем все ингредиенты, связанные с этим рецептом.
        ingredients = recipe.ingredients.all()

        # Проходим по каждому ингредиенту в рецепте.
        # Увеличиваем количество приготовленных блюд для продукта, связанного с этим ингредиентом.
        # Сохраняем изменения в базе данных для продукта.
        changes_to_save = []
        for ingredient in ingredients:
            ingredient.product.count += 1
            ingredient.product.save()

        # Возвращаем успешный HTTP-ответ.
        return HttpResponse("Успешно увеличено количество приготовленных блюд для продукта.")


class ShowRecipesWithoutProductView(View):
    def get(self, request, product_id):
        # Пытаемся получить объект продукта из базы данных или возвращаем ошибку 404.
        product = get_object_or_404(Product, id=product_id)

        # Получаем все рецепты, которые не содержат указанный продукт или содержат его менее чем 10 грамм
        recipes_without_product = Recipe.objects.exclude(products__id=product_id)
        recipes_without_product_2 = Recipe.objects.filter(
            Q(products__id=product_id) & Q(ingredients__weight__lte=10))

        combined_recipes = list(chain(recipes_without_product, recipes_without_product_2))

        context = {'combined_recipes': combined_recipes, 'product': product}
        print(combined_recipes)

        return render(request, 'cook_book/product_in_orders.html', context)
