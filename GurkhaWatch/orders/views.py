from django.http import HttpResponse, request
from django.shortcuts import redirect, render
from stripe.api_resources import line_item, payment_method
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct
import datetime
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views import generic
from django.urls import reverse


# Create your views here.
# for payment
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class CreateCheckoutSessionView(generic.View):
    def post(self, request, *args, **kwargs):
        host = self.request.get_host()
        current_user = request.user.first_name

    # when cart count is less than or equal to 0, then redirect back to shop
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        if cart_count <= 0:
            return redirect('shop')
        grand_total = 0
        tax = 0
        total = 0
        quantity = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (10 * round(total, 2))/100
        grand_total = int(total + tax)
        order_id = self.request.POST.get('order-id')
        order = Order.objects.get(id=order_id)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'aud',
                        'unit_amount': grand_total,
                        'product_data': {
                            'name': current_user,
                        },
                    },
                    'quantity': 1,
                },
            ],
            payment_method_types=[
                'card',
            ],
            mode='payment',
            success_url='http://{}{}'.format(host,
                                             reverse('payment-success')),
            cancel_url='http://{}{}'.format(host,
                                            reverse('payment-cancel')),
        )
        return redirect(checkout_session.url, code=303)


def paymentSuccess(request):
    context = {
        'payment_status': 'success'
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

    if event['type'] == ' checkout.session.completed':
        session = event['data']['object']
        if session.payment_status == 'paid':
            line_item = session.list_line_items(session.id, limit=1).data[0]
            order_id = line_item['description']
            fulfill_order(order_id)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order():
    order = Order.objects.get(id=order_id)
    order.ordered = True
    order.orderDate = datetime.datetime.now()
    order.save()

    for item in order.items.all():
        order.product.stock -= item.quantity
        order.product.save()


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # when cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (10 * total)/100
    grand_total = total + tax
    if request.method == "POST":
        form = OrderForm(request.POST)
        print(request.POST)
        print("I am outside validation")
        print(request.POST.get('first_name'))
        if form.is_valid():
            # store billing information in the order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.street_address = form.cleaned_data['street_address']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_notes = form.cleaned_data['order_notes']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20211028
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': 'total',
                'tax': tax,
                'grand_total': grand_total,
            }
            print("I am here")
            return render(request, 'payment.html', context)
        else:
            return HttpResponse('Invalid Data')
    else:
        return redirect('checkout')
