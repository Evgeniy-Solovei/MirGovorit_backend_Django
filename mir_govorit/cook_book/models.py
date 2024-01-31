from django.db import models


class Product(models.Model):
    """
    Модель, представляющая продукт, который может быть использован в рецепте.

    Поля:
    - name: Название продукта.
    - count: Количество раз, сколько продукт был использован в рецептах.
    """
    name = models.CharField(max_length=200, verbose_name='Название продукта')
    count = models.IntegerField(default=0, verbose_name='Количество использования продукта')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель, представляющая рецепт блюда, состоящий из продуктов.

    Поля:
    - name: Название рецепта.
    - products: Множество продуктов, используемых в рецепте через модель Ingredient.
    """
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    products = models.ManyToManyField(Product, through='Ingredient', related_name='recipes',
                                      verbose_name='Продукты в рецепте')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель, представляющая ингредиенты в рецепте.

    Поля:
    - recipe: Ссылка на рецепт, к которому относится ингредиент.
    - product: Ссылка на продукт, используемый в рецепте.
    - weight: Вес продукта в граммах, используемого в рецепте.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Рецепт')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Продукт')
    weight = models.IntegerField(verbose_name='Вес продукта в граммах')

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        unique_together = ('recipe', 'product')

    def __str__(self):
        return f'Рецепт: {self.recipe.name}'
