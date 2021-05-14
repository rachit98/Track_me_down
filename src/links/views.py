from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Link
from .forms import AddLinkForm
from django.views.generic import DeleteView
import pywhatkit
import smtplib
import datetime

def home_view(request):
    no_discounted = 0
    error = None

    form = AddLinkForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
        except AttributeError:
            error = "Couldn't get the name or the price"
        except:
            error = "Something went wrong"

    form = AddLinkForm()

    qs = Link.objects.all()
    items_no = qs.count()

    if items_no > 0:
        discount_list = []
        for item in qs:
            if item.old_price > item.current_price:
                discount_list.append(item)
            no_discounted = len(discount_list)

    context = {
        'qs':qs,
        'items_no':items_no,
        'no_discounted': no_discounted,
        'form':form,
        'error':error,
    }

    return render(request,'links/main.html',context)

class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'links/confirm_del.html'
    success_url = reverse_lazy('home')

def update_prices(request):
    qs = Link.objects.all()
    for link in qs:
        if link.trigger >= link.current_price:
            #print('Price reduced for ',link.name,'-------------ph no ',link.phno)
            now = datetime.datetime.now()
            minu = now.minute + 2

            hour = 0
            if minu>59:
                minu = minu%60
                hour = 1
            hour+= now.hour
            if hour >23:
                hour=0
            pywhatkit.sendwhatmsg(link.phno, 'Price for '+link.name+' has decreased\nClick link '+link.url+' to buy product.',hour,minu)

            def send_mail():
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login("track.amazon123@gmail.com", "Qwerty*987")

                subject = "Price Notification"
                body = 'Price for '+link.name+' has decreased\nClick link '+link.url+' to buy product.'

                msg = f"Subject: {subject}\n\n\n{body}"
                server.sendmail('track.amazon123@gmail.com', link.email, msg)
                #print("Mail has been sent")
                server.quit()
            
            send_mail()

            link.delete()
        elif link.rating == 'OUT OF STOCK':
            def send_mail_():
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login("track.amazon123@gmail.com", "Qwerty*987")

                subject = "Item Update"
                body = 'Item '+link.name+' went OUT OF STOCK. Removing it from tracking'

                msg = f"Subject: {subject}\n\n\n{body}"
                server.sendmail('track.amazon123@gmail.com', link.email, msg)
                #print("Mail has been sent")
                server.quit()
            
            send_mail_()

            link.delete()
        else:
            link.save()
    return redirect('home')
