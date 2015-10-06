from django import template


register = template.Library()


@register.assignment_tag
def unfeatured_posts_categories(posts):
    """Return a list of Categories, in alphabetical order, representing
    the Categories attached to the unfeatured posts in `posts`.
    """
    category_dict = {}
    for post in posts:
        if post.feature:
            continue
        category_dict[post.category.name] = post.category
    category_list = []
    for category in sorted(category_dict):
        category_list.append(category)
    return category_list
