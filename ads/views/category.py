import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

from ads.models import Category


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListCreateView(View):
    def get(self, request):
        categories = Category.objects.all()
        response = []
        for cat in categories:
            response.append({'id': cat.pk, 'name': cat.name})
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):
        data = json.loads(request.body)
        cat = Category.objects.create(**data)
        return JsonResponse({'id': cat.pk,
                             'name': cat.name
                             }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        category = get_object_or_404(Category, name=data['category'])
        cat = Category.objects.create(name=data['name'])

        return JsonResponse({'id': Category.pk,
                             'name': Category.name
                             }, safe=False)

class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.object_list.order_by('name')
        return JsonResponse({'id': cat.pk, 'name': cat.name}, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        if 'name' in data:
            self.object.name = data['name']

        return JsonResponse({'id': self.object.pk,
                             'name': self.object.name
                             }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=204)