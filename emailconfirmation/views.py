from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from emailconfirmation.models import EmailConfirmation

## Hacking in some login stuff


from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from models import EmailAddress
def confirm_email(request, confirmation_key):
    confirmation_key = confirmation_key.lower()
    email_address = EmailConfirmation.objects.confirm_email(confirmation_key)
    if email_address:
        user = email_address.user
        # stupid hack because we don't know the user's password
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        request.user.message_set.create(
            message=_("Successfully logged in as %(username)s.") % {
            'username': user.username
        })
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponse("Invalid email confirmation") #TODO: FIX THIS
    
    # return render_to_response("emailconfirmation/confirm_email.html", {
    #     "email_address": email_address,
    # }, context_instance=RequestContext(request))