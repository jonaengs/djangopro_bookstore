import stripe
from django.contrib.auth.models import Permission
from django.shortcuts import render
from django.views.generic import TemplateView

from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class OrderPageView(TemplateView):
    template_name = 'orders/purchase.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        return context


def charge(request):
    special_permission = Permission.objects.get(codename='special_status')
    if request.method == 'POST':
        _ = stripe.Charge.create(
            amount=3900,
            currency='usd',
            description='Purchase all books',
            source=request.POST['stripeToken'],
        )
        request.user.user_permissions.add(special_permission)
        return render(request, 'orders/charge.html')
