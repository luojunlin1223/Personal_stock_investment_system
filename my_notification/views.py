from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from notifications.models import Notification


def read_notifications(request):
    notifications=Notification.objects.filter(recipient=request.user)
    return render(request, 'my_notification/notification.html',{'data':notifications})
def delete_notifications(request):
    deleteValues=request.POST.get('deleteValues').split(',')
    for item in deleteValues:
        if item=='':
            pass
        else:
            Notification.objects.filter(id=item)[0].delete()
    return HttpResponseRedirect('/notifications/read')
def sign_to_read(request):
    signValues=request.POST.get('signValues').split(',')
    for item in signValues:
        if item=='':
            pass
        else:
            Notification.objects.filter(id=item)[0].mark_as_read()
    return HttpResponseRedirect('/notifications/read')