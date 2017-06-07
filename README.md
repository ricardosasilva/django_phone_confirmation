# Introduction #


A Django app to validate cell phone numbers through SMS messages.

 It uses Django Rest to implement a couple of endpoints to confirm the number and django-sendsms to send the messages.


## Installation ##


1. Install package:

        pip install django_phone_confirmation

2. Add django_phone_confirmation app to INSTALLED_APPS in your django settings.py:

        INSTALLED_APPS = (
            ...,
            'rest_framework',
            'phone_confirmation',
        )

3. Add in urls.py:

        urlpatterns = patterns('',
          url(r'^phone-confirmation/', include('phone_confirmation.urls', namespace='phone_confirmation')),
        )


## A basic flow ##

1.  User inputs cell phone number.
1.  The app/page make a POST request to the **confirm-phone/confirmation/** endpoint with the phone number entered by the user.
1. An SMS message is sent to the phone number with a 4 number code.
1. The user enter the code on the App/Page
1. The app/page make a POST request to the **confirm-phone/activation-key/** endpoint with the code entered by the user.
     The response is a signed activation key if the code is correct, or a 400 status response otherwise.
1. Then the app/page can use the phone number or save the activation key to use it later.


## Endpoints ##

### confirm-phone/confirmation/ ###

Request example:

    curl -X POST \
      http://localhost:8000/confirm-phone/confirmation/ \
      -H 'cache-control: no-cache' \
      -H 'content-type: application/json' \
      -d '{
    	"phone_number": "+1-202-555-1234"
    }'

Response example:

    {"phone_number": "+12025551234"}

And the code 6108 (just a example, the code is picked randomly) is sent by SMS to the phone.


### confirm-phone/activation-key/ ###


Request example:

    curl -X POST \
      http://localhost:8000/confirm-phone/activation-key/ \
      -H 'cache-control: no-cache' \
      -H 'content-type: application/json' \
      -d '{
    	"phone_number": "+1-202-555-1234",
    	"code": "6108"
    }'

Successful response example:

    {"activation_key":"eyJwaG9uZV9udW1iZXIiOiIrMTIwMjU1NTEyMzQifQ:1dHsio:RvZd7XLwZPvWrN0OI4jA2R5PT8Q"}

Fail response example:

    {"error": "Invalid activation key"}


### confirm-phone/activation-key/{activation key}/ ###

Request example:


    curl -X GET \
      http://localhost:8000/confirm-phone/activation-key/eyJwaG9uZV9udW1iZXIiOiIrMTIwMjU1NTEyMzQifQ:1dHsio:RvZd7XLwZPvWrN0OI4jA2R5PT8Q/ \
      -H 'cache-control: no-cache' \
      -H 'content-type: application/json'


Response example:

    {"phone_number": "+12025551234"}



## Settings ##

  These are the default settings:

    PHONE_CONFIRMATION = {
        "SALT": "phonenumber",
        "ACTIVATION_MINUTES": 15,
        "SMS_TEMPLATE": "django_phone_confirmation/message.txt",
        "FROM_NUMBER": "",
        "MAX_CONFIRMATIONS": 10
    }


**SALT**

  Used as salt when creating activation keys.

**ACTIVATION_MINUTES**

  How many minutes the user have to confirm the number after the initial requesting

**SMS_TEMPLATE**
  The template file for the message. The message on the default template is the i18n string: **Your confirmation code: {{ code }}**

**FROM_NUMBER**

  The number to use as sender of the SMS messages. You should use the number provided by your SMS gateway. This is the only required setting.

**MAX_CONFIRMATIONS**

  The maximum number of confirmations to keep in database for each phone number. When this amount is reached, the oldest confirmation is removed.


   **NOTE:** As we use the django-sendsms package you need to configure it with your SMS Gateway in order to delivery SMS messages.


## Throttle Scope ##


  phone-number-confirmation
