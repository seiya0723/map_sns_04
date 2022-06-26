from django.shortcuts import render,redirect
from django.views import View

from .models import Park,Category,Tag
from .forms import ParkForm,CategorySearchForm,TagSearchForm

from django.db.models import Q
from django.db.models import Count


class IndexView(View):

    
    #重複を除去する。
    def distinct(self,obj):

        id_list     = []
        new_obj     = []

        for o in obj:
            if o.id in id_list:
                continue

            id_list.append(o.id)
            new_obj.append(o)

        return new_obj
        


    def get(self, request, *args, **kwargs):

        context = {}
        context["categories"]   = Category.objects.all()
        context["tags"]         = Tag.objects.all()

        #TODO:ここで公園を検索するバリデーションを行う。

        #公園名の検索
        query   = Q()


        if "search" in request.GET:
            search      = request.GET["search"]

            raw_words   = search.replace("　"," ").split(" ")
            words       = [ w for w in raw_words if w != "" ]

            for w in words:
                query &= Q(name__contains=w)


        #カテゴリの検索
        form    = CategorySearchForm(request.GET)

        if form.is_valid():
            cleaned = form.clean()
            query &= Q(category=cleaned["category"].id)
        else:
            print("カテゴリ検索エラー")

        #多対多の検索
        form    = TagSearchForm(request.GET)

        if form.is_valid():
            cleaned = form.clean()

            #指定したタグのいずれかを含む検索
            query &= Q(tag__in=cleaned["tag"])


            #TIPS:指定したタグの全てを含む検索をする場合はfilterを数珠つなぎにするかannotateを使うしかない。(クエリビルダのANDは通用しない)
            #https://stackoverflow.com/questions/8618068/django-filter-queryset-in-for-every-item-in-list/8637972#8637972

            #context["parks"]    = self.distinct( Park.objects.filter(query, tag__in=cleaned["tag"]).annotate(num_tags=Count('tag')).filter(num_tags=2).order_by("-dt") )



        #ここでループしてモデルオブジェクト比較し、重複除去をする。
        context["parks"]    = self.distinct( Park.objects.filter(query).order_by("-dt") )


        #print(request.GET.getlist("tag"))

        return render(request, "sns/index.html", context)

    def post(self, request, *args, **kwargs):

        form    = ParkForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        return redirect("sns:index")

index   = IndexView.as_view()
