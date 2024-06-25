from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ImageCreateForm
from .models import Image

# Create your views here.
"""
we have created a view to store images on the site. We have added the login_
required decorator to the image_create view to prevent access to unauthenticated users
"""


@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item, to ensure who has uploaded each image
            new_image.user = request.user
            new_image.save()
            new_image.users_like.add(request.user)
            messages.success(request, 'Image added successfully')
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html',
                  {'section': 'images', 'form': form}
                  )


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html',
                  {'section': 'images', 'image': image}
                  )


"""
The require_POST decorator returns an HttpResponseNotAllowed
object (status code 405) if the HTTP request is not done via POST
"""


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_likes.add(request.user)
            else:
                image.users_likes.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
        return JsonResponse({'status': 'error'})
