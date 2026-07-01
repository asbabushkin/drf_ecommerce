from autoslug import AutoSlugField
from django.db import models

from apps.common.models import BaseModel


class Category(BaseModel):
    """
    Represents a product category.

    Attributes:
        name (str): The category name, unique for each instance.
        slug (str): The slug generated from the name, used in URLs.
        image (ImageField): An image representing the category.

    Methods:
        __str__():
            Returns the string representation of the category name.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"