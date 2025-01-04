from django import template

register = template.Library()

@register.filter
def dict_key(value, key):
    """
    辞書から指定されたキーの値を取得するテンプレートフィルタ
    """
    try:
        return value.get(key, "")
    except AttributeError:
        return ""