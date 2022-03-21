from django.http import HttpResponse, request
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from stripe.api_resources import checkout, line_item, payment_method
from accounts.models import Account
from shop.models import Product
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct
import datetime
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views import generic
from django.urls import reverse
from .models import Payment
from gurkhawatch import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

# for payment
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class CreateCheckoutSessionView(generic.View):
    def post(self, request, *args, **kwargs):
        host = self.request.get_host()
        order_id = self.request.POST.get('order-id')
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        # when cart count is less than or equal to 0, then redirect back to shop
        if cart_count <= 0:
            return redirect('shop')
        service_charge = 0
        total = 0
        quantity = 0
        # check if discount present on product
        for cart_item in cart_items:
            if cart_item.product.discount_percent > 0:
                total += (cart_item.product.discount() * cart_item.quantity)
            else:
                total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        service_charge = int((10 * round(total, 2))/100)
        stripe_line_items = []
        for cart_item in cart_items:
            if cart_item.product.discount_percent > 0:
                amount = int(cart_item.product.discount())
            else:
                amount = cart_item.product.price
            stripe_line_items.append({
                'name': cart_item.product.product_name,
                'quantity': cart_item.quantity,
                'currency': 'aud',
                'amount': amount
            })
        stripe_line_items.append({
            'name': 'Service Charge',
            'quantity': 1,
            'currency': 'aud',
            'amount': service_charge,
        })
        checkout_session = stripe.checkout.Session.create(
            line_items=stripe_line_items,
            payment_method_types=[
                'card',
            ],
            mode='payment',
            metadata={
                'order_id': order_id
            },
            success_url=('http://{}{}' + f'?order_id={order_id}').format(host,
                                                                         reverse('payment-success')),
            cancel_url='http://{}{}'.format(host,
                                            reverse('payment-cancel')),
        )

        return redirect(checkout_session.url, code=303)


def paymentSuccess(request, total=0, quantity=0):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)

    context = {
        'payment_status': 'success',
        'order_number': order.order_number,
        'order_status': order.status
    }
    return render(request, 'confirmation.html', context)


def paymentCancel(request):
    context = {
        'payment_status': 'cancel'
    }
    return render(request, 'confirmation.html', context)


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.metadata.order_id

        if session.payment_status == 'paid':
            # Fulfill the purchase...
            fulfill_order(request, order_id=order_id, stripe_session=session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(request, order_id, stripe_session):
    order = Order.objects.get(id=order_id)
    order.is_ordered = True
    order.save()

    user = order.user

    payment = Payment()
    payment.user = user
    payment.payment_id = stripe_session.payment_intent
    payment.payment_method = 'stripe'
    payment.amount_paid = stripe_session.amount_total
    payment.status = stripe_session.payment_status
    payment.save()

    cart_items = CartItem.objects.filter(user=user)

    for item in cart_items:
        orderProduct = OrderProduct()
        orderProduct.order = order
        orderProduct.payment = payment
        orderProduct.user = user
        orderProduct.product = item.product
        orderProduct.quantity = item.quantity
        # check if discount present on product
        orderProduct.product_price = item.product.price
        orderProduct.ordered = True
        orderProduct.save()

        # decrement stock
        item.product.stock = item.product.stock - item.quantity
        item.product.save()

    cart_items.delete()
    # send order received email to the customer
    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_received_email.html', {
        'user': user,
        'order': order,
    })
    to_email = user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    # when cart count is less than or equal to 0, then redirect back to shop
    if cart_count <= 0:
        return redirect('shop')

    grand_total = 0
    service_charge = 0
    for cart_item in cart_items:
        if cart_item.product.discount_percent > 0:
            total += (cart_item.product.discount() * cart_item.quantity)
        else:
            total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    service_charge = int((10 * round(total, 2))/100)
    grand_total = total + service_charge
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # store billing information in the order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_notes = form.cleaned_data['order_notes']
            data.order_total = grand_total
            data.service_charge = service_charge
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            year = int(datetime.date.today().strftime('%Y'))
            month = int(datetime.date.today().strftime('%m'))
            day = int(datetime.date.today().strftime('%d'))
            # hour = int(datetime.date.today().strftime('%H'))
            # minute = int(datetime.date.today().strftime('%M'))
            # second = int(datetime.date.today().strftime('%S'))

            d = datetime.date(year, month, day)
            current_date = d.strftime("%Y%m%d")
            order_number = current_user.first_name[0].upper(
            ) + current_user.last_name[0].upper() + current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            context = {
                "order": order,
                "total": total,
                "quantity": quantity,
                "cart_items": cart_items,
                "service_charge": service_charge,
                "grand_total": grand_total,
            }
            return render(request, 'payment.html', context)
        else:
            return HttpResponse('Invalid Data')
    else:
        return redirect('checkout')
