from django.shortcuts import render

from alfa.decorators import *
from alfa.forms import HomePostForm, NewCarouselElementForm, EditCarouselElementForm
from alfa.models import HomePost, CarouselElement, ImageText

n = 5


def home_page(request):
    context = {}
    template_name = 'home/home_page.html'
    page = request.GET.get('page')
    if page is None or page == '-1':
        page = 0
    page = int(page)
    context['page'] = page
    context['next_page'] = page + 1
    context['prev_page'] = page - 1
    all_posts = HomePost.objects.all()
    print(ImageText.objects.count())
    if ImageText.objects.count() <= (page + 1) * n:
        context['next_page'] = -1
    context['all_posts'] = all_posts[page * n:(page + 1) * n]
    context['home_posts'] = ImageText.objects.filter(type='home')[page * n:(page + 1) * n]
    all = CarouselElement.objects.filter(location='home')
    print(context)
    if all.count() == 0:
        return render(request, template_name, context)
    context['active_element'] = all[0]
    context['carousel'] = all[1:]
    return render(request, template_name, context)


@has_premission()
def new_home_page(request):
    context = {}
    template_name = 'home/new_home_page.html'
    if request.method == 'POST':
        form = HomePostForm(request.POST)
        if form.is_valid():
            post = HomePost()
            post.text = form.cleaned_data['text']
            post.title = form.cleaned_data['title']
            post.url = form.cleaned_data['url']
            post.save()
            return HttpResponseRedirect(reverse('home_url'))
        else:
            context['error'] = True
            context['form'] = HomePostForm()
            context['error_message'] = 'Неверно заполнена форма.'
            return render(request, template_name, context)
    else:
        context['form'] = HomePostForm()
        return render(request, template_name, context)


@has_premission()
def remove_home_post_page(request, id):
    context = {}
    try:
        post = HomePost.objects.get(id=id)
    except HomePost.DoesNotExist:
        return HttpResponseRedirect(reverse('home_url'))
    if request.method == 'POST':
        post.delete()
        return HttpResponseRedirect(reverse('home_url'))
    else:
        context['back_url'] = reverse('home_url')
        context['text'] = 'Действительно удалить пост \"' + str(post) + '\"' + '?'
        return render(request, 'admin/really_remove_page.html', context)


@has_premission()
def new_carousel_element_page(request):
    context = {}
    template_name = 'home/new_carousel_element_page.html'
    try:
        if request.method == 'POST':
            form = NewCarouselElementForm(request.POST, request.FILES)
            if form.is_valid():
                element = form.save(commit=False)
                element.location = 'home'
                element.save()
                return HttpResponseRedirect(reverse('edit_carousel_element_url', kwargs={'id': element.id}))
            else:
                context['error'] = True
                context['form'] = NewCarouselElementForm()
                context['error_message'] = 'Неверно заполнена форма.'
                return render(request, template_name, context)
        else:
            context['form'] = NewCarouselElementForm()
            return render(request, template_name, context)
    except Exception as e:
        context['error'] = True
        context['error_message'] = 'Произошла ошибка.<br>' + str(e)
        context['form'] = NewCarouselElementForm()
        return render(request, template_name, context)


@has_premission()
def edit_carousel_element_page(request, id):
    context = {}
    template_name = 'home/new_carousel_element_page.html'
    try:
        element = CarouselElement.objects.get(id=id)
    except CarouselElement.DoesNotExist:
        return HttpResponseRedirect(reverse('home_url'))
    try:
        if request.method == 'POST':
            form = EditCarouselElementForm(request.POST, request.FILES, instance=element)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('home_url'))
            else:
                context['error'] = True
                context['error_message'] = 'Произошла ошибка.<br>' + str(form.error)
                context['form'] = form
                return render(request, template_name, context)
        else:
            context['form'] = EditCarouselElementForm(instance=element)
            return render(request, template_name, context)
    except Exception as e:
        context['error'] = True
        context['error_message'] = 'Произошла ошибка.<br>' + str(e)
        context['form'] = EditCarouselElementForm(instance=element)
        return render(request, template_name, context)


@has_premission()
def edit_carousel_page(request):
    context = {}
    template_name = 'home/carousel_elements_page.html'
    context['carousel'] = CarouselElement.objects.filter(location='home')
    return render(request, template_name, context)


@has_premission()
def carousel_element_move_up_page(request, id):
    try:
        item = CarouselElement.objects.get(id=id)
    except CarouselElement.DoesNotExist:
        return HttpResponseRedirect(reverse('edit_carousel_url'))
    items = CarouselElement.objects.filter(location='home', number__lte=item.number).order_by('-number')
    if items.count() > 1:
        one = items[0]
        two = items[1]
        tmp = one.number
        one.number = two.number
        two.number = tmp
        one.save()
        two.save()
    return HttpResponseRedirect(reverse('edit_carousel_url'))


@has_premission()
def carousel_element_move_down_page(request, id):
    try:
        item = CarouselElement.objects.get(id=id)
    except CarouselElement.DoesNotExist:
        return HttpResponseRedirect(reverse('edit_carousel_url'))
    items = CarouselElement.objects.filter(location='home', number__gte=item.number).order_by('-number')
    if items.count() > 1:
        one = items[0]
        two = items[1]
        tmp = one.number
        one.number = two.number
        two.number = tmp
        one.save()
        two.save()
    return HttpResponseRedirect(reverse('edit_carousel_url'))


@has_premission()
def remove_carousel_element_page(request, id):
    try:
        item = CarouselElement.objects.get(id=id)
    except CarouselElement.DoesNotExist:
        return HttpResponseRedirect(reverse('edit_carousel_url'))
    item.delete()
    return HttpResponseRedirect(reverse('edit_carousel_url'))


@has_premission()
def new_partner_page(request):
    context = {}
    template_name = 'partners/new_partner_page.html'
    try:
        if request.method == 'POST':
            form = PartnerForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('partners_url'))
            else:
                context['error'] = True
                context['error_message'] = 'Неверно заполнена форма.<br>' + str(form.errors)
                context['form'] = form
                return render(request, template_name, context)
        else:
            context['form'] = PartnerForm()
            return render(request, template_name, context)
        return HttpResponseRedirect(reverse('for_patients_url'))
    except Exception as e:
        context['error'] = True
        context['error_message'] = 'Произошла ошибка.<br>' + str(e)
        context['form'] = PartnerForm()
        return render(request, template_name, context)


@has_premission()
def edit_partner_page(request, id):
    context = {}
    template_name = 'partners/new_partner_page.html'
    try:
        document = Partner.objects.get(id=id)
    except Partner.DoesNotExist:
        return HttpResponseRedirect(reverse('partners_url'))
    try:
        if request.method == 'POST':
            form = PartnerForm(request.POST, request.FILES, instance=document)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('partners_url'))
            else:
                context['error'] = True
                context['error_message'] = 'Неверно заполнена форма.<br>' + str(form.errors)
                context['form'] = form
                return render(request, template_name, context)
        else:
            context['form'] = PartnerForm(instance=document)
            return render(request, template_name, context)
        return HttpResponseRedirect(reverse('partners_url'))
    except Exception as e:
        context['error'] = True
        context['error_message'] = 'Произошла ошибка.<br>' + str(e)
        context['form'] = DocumentForm(instance=document)
        return render(request, template_name, context)


@has_premission()
def remove_partner_page(request, id):
    try:
        obj = Partner.objects.get(id=id)
    except Partner.DoesNotExist:
        return HttpResponseRedirect(reverse('partners_url'))
    context = {}
    context['text'] = 'Действительно удалить партнёра \"' + obj.name + '\"' + '?'
    context['back_url'] = reverse('partners_url')
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect(context['back_url'])
    return render(request, 'admin/really_remove_page.html', context)
