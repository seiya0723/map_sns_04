#https://noauto-nolife.com/post/django-paginator/

from django import template
register = template.Library()

#検索時に指定したタグとモデルオブジェクトのtagのidが一致した場合はchecked文字列を返す。
@register.simple_tag()
def tag_checked(request, tag_id):

    tags    = request.GET.getlist("tag")

    for tag in tags:
        if tag == str(tag_id):
            print("checked")
            return "checked"

    

