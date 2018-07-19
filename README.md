# Introduction #


A Django app to validate cell phone numbers through SMS messages.

 It uses Django Rest to implement a couple of endpoints to confirm the number and django-sendsms to send messages.


## Installation ##


1. Install package:

        pip install django_phone_confirmation

2. Add phone_confirmation app to INSTALLED_APPS in your django settings.py:

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

1. User inputs cell phone number.
1. The app/page make a POST request to the **phone-confirmation/confirmation/** endpoint with the phone number entered by the user.
1. An SMS message is sent to the phone number with a 4 number code.
1. The user enter the code on the App/Page
1. The app/page make a POST request to the **phone-confirmation/activation-key/** endpoint with the code entered by the user.
     The response is a signed activation key if the code is correct, or a 400 status response otherwise.
1. Then the app/page can use the phone number or save the activation key to use it later.


## Endpoints ##

### phone-confirmation/confirmation/ ###

Request example:

    curl -X POST \
      http://localhost:8000/phone-confirmation/confirmation/ \
      -H 'cache-control: no-cache' \
      -H 'content-type: application/json' \
      -d '{
    	"phone_number": "+1-202-555-1234"
    }'

Response example:

    {"phone_number": "+12025551234"}

And the code 6108 (just a example, the code is picked randomly) is sent by SMS to the phone.


### phone-confirmation/activation-key/ ###


Request example:

    curl -X POST \
      http://localhost:8000/phone-confirmation/activation-key/ \
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


### phone-confirmation/activation-key/{activation key}/ ###

Request example:


    curl -X GET \
      http://localhost:8000/phone-confirmation/activation-key/eyJwaG9uZV9udW1iZXIiOiIrMTIwMjU1NTEyMzQifQ:1dHsio:RvZd7XLwZPvWrN0OI4jA2R5PT8Q/ \
      -H 'cache-control: no-cache' \
      -H 'content-type: application/json'


Response example:

    {"phone_number": "+12025551234"}



## Settings ##

  These are the default settings:

    PHONE_CONFIRMATION = {
        "SALT": "phonenumber",
        "ACTIVATION_TIMEOUT": 15,
        "SMS_MESSAGE": "Your confirmation code is %(code)s",
        "FROM_NUMBER": "",
        "MAX_CONFIRMATIONS": 10
    }


**SALT**

  Used as salt when creating activation keys.

**ACTIVATION_TIMEOUT**

  How many seconds the user have to confirm the number after the initial requesting

**SMS_MESSAGE**
  The SMS message that will be send to users. The default message is "Your confirmation code is %(code)s".
  Use %{code}s variable to indicate where the confirmation code should be placed.

**FROM_NUMBER**

  The number to use as sender of the SMS messages. You should use the number provided by your SMS gateway. This is the only required setting.

**MAX_CONFIRMATIONS**

  The maximum number of confirmations to keep in database for each phone number. When this amount is reached, the oldest confirmation is removed.


   **NOTE:** As we use the django-sendsms package you need to configure it with your SMS Gateway in order to delivery SMS messages.

**SILENT_CONFIRMATIONS_FILTER**

  A callable with a single argument to ignore fake tests numbers. If it returns True the SMS won't be send.

    Example:
    SILENT_CONFIRMATIONS_FILTER = lambda to: to[:8] == '+1212555'  # Ignore numbers starting with +1212555.


## Throttle Scope ##

  - phone-number-confirmation: Endpoint to request a phone number confirmation (Wiil sent SMS)
  - phone-confirmation-activation-key: Endpoints to validate codes and activation keys.


## Changelog ##

0.3.3 - Changed settings ACTIVATION_MINUTES to ACTIVATION_TIMEOUT and the period time to seconds. Changed settingg SMS_TEMPLATE to SMS_MESSAGE.
0.3.4 - Add activation_key_created signal.
