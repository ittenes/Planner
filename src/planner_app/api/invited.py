

from django.contrib import messages

#from django.contrib.auth import get_user_model

from invitations.models import Invitation
#from invitations.exceptions import AlreadyInvited, AlreadyAccepted, UserRegisteredEmail

from planner_app.models import AuthUser, UserCompany

class InvitationSend():
    """This invitatione is a class of django-invitations for rest_framework."""

    def __init__(self, user, email, request, *args, **kwargs):
        self.user = user #AuthUser.objects.get(pk=user)
        self.email = email
        self.request = request

    def invitations(self,):
        Invitation.create(email=self.email)
        invite = Invitation.objects.get(email= self.email)
        invite.inviter = self.request.user
        invite.save

        print ('invite', invite)
        invite.save
        invite.send_invitation(self.request)
