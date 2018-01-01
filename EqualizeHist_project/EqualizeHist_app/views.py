from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings


from EqualizeHist_app.forms import ImageForm
from EqualizeHist_app.models import Image, EqualizedImage
from EqualizeHist_app.models import Histogram, EqualizedHistogram

import matplotlib
matplotlib.use('Agg')

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image as PythImage
from django.core.files import File
from skimage.exposure import equalize_hist
from matplotlib.pyplot import imread

import os
import glob
import sys

# Create your views here.
class HomePage(TemplateView):
    template_name = 'index.html'

class SuccessPage(TemplateView):
    template_name = 'success.html'



@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            instance = Image(imageFile = request.FILES.get('image'))
            instance.imageName = request.FILES.get('image').name
            instance.save()
            return render_to_response('success.html', {'image': instance})
    else:
        form = ImageForm()
        return render_to_response('upload_page.html', {'form' : form})

def create_hist_plot(image, histogram_name, equalized):
    figure = plt.figure()

    plt.hist(image.ravel(),256,[0,256])

    if equalized:
        figure.suptitle("Image Histogram (Equalized)")
    else:
        figure.suptitle("Image Histogram (Not Equalized)")

    plt.xlabel("Color Weight [0, 256]")
    plt.ylabel("Frequency")

    figure.savefig(settings.MEDIA_ROOT + '/' + histogram_name)



@csrf_exempt
def display_histogram(request):
    name = os.path.join(settings.MEDIA_ROOT, Image.objects.latest('id').imageName)

    n = Image.objects.latest('id').imageName
    histogram_name = n[:n.index('.')] + '_histogram' + n[n.index('.'):]

    create_hist_plot(cv2.imread(name, 0), histogram_name, False)

    full_path = get_histogram_from_dir(settings.MEDIA_ROOT, n)
    (f_path, f_name) = os.path.split(full_path)

    f = open(full_path, 'r')

    histogram_instance = Histogram()
    histogram_instance.image_id = Image.objects.latest('id').id
    histogram_instance.imageHist.name = histogram_name
    histogram_instance.histName = histogram_name

    histogram_instance.save()

    return render_to_response('notEqualized.html', {'histogram' : histogram_instance, 'image': Image.objects.latest('id')})

def get_histogram_from_dir(dir, image_name):
    image_name = dir + '/' + image_name
    for filename in glob.glob(dir + '/*.*'):
        res = filename.find('_histogram')

        if res != -1:
            exactName = filename.replace('_histogram', '')
            if exactName == image_name:
                return filename
            else:
                continue

def download(request):
    f_path = os.path.join(settings.MEDIA_ROOT,  request.GET['filename'])

    if os.path.exists(f_path):
        with open(f_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/jpeg')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(f_path)
            return response
    else: raise Http404("Not Found")

def equalize_histogram(request):
    image_path = os.path.join(settings.MEDIA_ROOT,  request.GET['original'])
    (i_path, i_name) = os.path.split(image_path)

    image_original = imread(image_path)
    image_equalized = np.asarray(equalize_hist(image_original) * 255, dtype='uint8')

    hist_name = i_name[:i_name.index('.')] + '_histogramEQ' + i_name[i_name.index('.'):]

    create_hist_plot(image_equalized, hist_name, True)

    eq_hist_instance = EqualizedHistogram(histogram_id = Histogram.objects.latest('id').image_id)
    eq_image_instance = EqualizedImage(image_id = Image.objects.latest('id').id)

    eq_hist_instance.eqHist.name = hist_name
    eq_hist_instance.eqName = hist_name

    imageN = Image.objects.latest('id').imageName
    imageEq_name = imageN[:imageN.index('.')] + '_EQUALIZED' + i_name[imageN.index('.'):]

    eq_image_instance.eqImageName = imageEq_name

    image_equalized = PythImage.fromarray(image_equalized)
    image_equalized.save(settings.MEDIA_ROOT + '/' + imageEq_name)

    eq_image_instance.eqImage.name = imageEq_name

    eq_hist_instance.save()
    eq_image_instance.save()

    return render_to_response('equalized.html',
                            {'eq_image' : eq_image_instance, 'eq_hist' : eq_hist_instance})

def compare_images(request):
    image = Image.objects.latest('id')
    equalized_image = EqualizedImage.objects.latest('image_id')

    return render_to_response('compare.html',
                              {'image': image, 'equalized_image': equalized_image})
