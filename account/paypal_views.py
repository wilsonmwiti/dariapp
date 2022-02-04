# from django.http.response import JsonResponse
from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
import os
from .models import Account, CashWithrawal, Currency
# import json
import random
import string
from .paypal_client import DPayPalClient
from paypalpayoutssdk.payouts import PayoutsPostRequest
# from paypalhttp.serializers.json_serializer import Json
# from paypalhttp.http_error import HttpError
# from paypalhttp.encoder import Encoder
from django.conf import settings

from django.contrib.auth.decorators import login_required

# Creating an environment
client_id = settings.PAYPAL_CLIENT_ID
if settings.DEBUG:
    environment = SandboxEnvironment(client_id=client_id, client_secret=settings.PAYPAL_CLIENT_SECRET)
else:
    environment = LiveEnvironment(client_id=client_id, client_secret=settings.PAYPAL_CLIENT_SECRET)

client = PayPalHttpClient(environment)



class CreatePayouts(DPayPalClient):

    """ Creates a payout batch with 5 payout items
    Calls the create batch api (POST - /v1/payments/payouts)
    A maximum of 15000 payout items are supported in a single batch request"""

    def __init__(self, amount, receiver):
        self.amount = amount
        self.receiver = receiver
        DPayPalClient.__init__(self)

    # @staticmethod
    def build_request_body(self, include_validation_failure = False):
        senderBatchId = str(''.join(random.sample(
            string.ascii_uppercase + string.digits, k=7)))
        amount = self.amount # if include_validation_failure else "1.00"
        return \
            {
                "sender_batch_header": {
                    "recipient_type": "EMAIL",
                    "email_message": "Darius Option Win Payout",
                    "note": "Enjoy your Payout!!",
                    "sender_batch_id": senderBatchId,
                    "email_subject": "Darius Option Wins Payout.Enjoy!"
                },
                "items": [{
                    "note": "Thanks for using Darius Option.Refer more for more payout!",
                    "amount": {
                        "currency": "USD",
                        "value": amount
                    },
                    "receiver": self.receiver,
                    "sender_item_id": "PayoutD"
                }]
            }

    def create_payouts(self, debug=False):
        request = PayoutsPostRequest()
        request.request_body(self.build_request_body(False))
        response = self.client.execute(request)

        if debug:
            print("Status Code: ", response.status_code)
            print("Payout Batch ID: " +
                  response.result.batch_header.payout_batch_id)
            print("Payout Batch Status: " +
                  response.result.batch_header.batch_status)
            print("Links: ")
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(
                    link.rel, link.href, link.method))

            # To toggle print the whole body comment/uncomment the below line
            #json_data = self.object_to_json(response.result)
            #print "json_data: ", json.dumps(json_data, indent=4)

        return response







# @login_required(login_url="/user/login")
# def accept_payment(request):
#     return render(request, "account/paypal/accept-payment.html",{"client_id":client_id})


# @csrf_exempt # security issue
# def payment_success(request):
#     if request.method == "POST":
#         import json
#         post_data = json.loads(request.body.decode("utf-8"))
#         amount=float(post_data["amount"])
#         try:
#             currency=Currency.objects.get(name="USD")
#         except Currency.DoesNotExist:
#             Currency.objects.create(name="USD",rate=100) 
#             currency=Currency.objects.get(name="USD")

#         try:
#             CashDeposit.objects.create(
#                 user=request.user,
#                 amount=amount,
#                 currency_id=currency,
#                 confirmed=True,#
#                 deposit_type="PAYPAL`",)
#         except Exception as e:
#             print(e)
#             print('paypal deposir_ISSUE!!')                

#         # print(post_data)#Debug

#         return JsonResponse({"success": True})



@login_required(login_url="/user/login")
def paypal_payout(request):
    if request.method == "POST":
        amount=float(request.POST['amount'])
        try:
            currency=Currency.objects.get(name="USD")
        except Currency.DoesNotExist:
            Currency.objects.create(name="USD",rate=100) ###
            currency=Currency.objects.get(name="USD")        

        try:
            create_response = CreatePayouts(str(amount), request.user.email).create_payouts(True)
        except Exception as e:   
            return render(request, "account/paypal/payment.html", {"msg": 'Failed try again.Connection issue'})


        if int(create_response.status_code) == 201:

            CashWithrawal.objects.create(
                user=request.user,
                amount=float(amount),
                currency=currency,
                approved=True,
                )

            msg=f'{amount} withrawned successfully.Check your paypal balance'       

            return render(request, "account/paypal/payment.html", {"msg": msg})
        msg=f'{amount} NOT withrawned successfully.Try again'    
        return render(request, "account/paypal/payment.html", {"msg": msg})    
    else:
        try:
            uf = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            uf = Account(user=request.user, balance=0).save()
        return render(request, "account/paypal/payment.html", {
            "uf": uf
        })
