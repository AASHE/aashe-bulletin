from django import template


register = template.Library()


class PostCategoryIsNotSubcategory(Exception):
    pass


@register.assignment_tag
def unfeatured_posts_categories(posts):
    """Return a list of Categories, in alphabetical order, representing
    the Categories attached to the unfeatured posts in `posts` as
    primary categories.

    All Categories assigned to posts should be subcategories (i.e., their
    parent attribute should point to another Category object).
    """
    category_set = set()
    for post in posts:
        if post.feature:
            continue
        try:
            category_name = post.primary_category.parent.name
        except AttributeError:
            raise PostCategoryIsNotSubcategory(post.primary_category)
        category_set.add(category_name)
    return sorted(list(category_set))
