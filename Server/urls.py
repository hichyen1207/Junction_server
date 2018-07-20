from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from user import views as userViews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^checkUser/(?P<id>[\w\-]+)/$', userViews.CheckUser.as_view()),
    url(r'^user/$', userViews.UserList.as_view()),
    url(r'^user/(?P<id>[\w\-]+)/$', userViews.UserDetail.as_view()),
    url(r'^user/(?P<id>[\w\-]+)/friends/$', userViews.FriendsList.as_view()),
    url(r'^user/(?P<id>[\w\-]+)/card/$', userViews.CardDetail.as_view()),
    url(r'^inviteFriend/(?P<id>[\w\-]+)/$', userViews.FriendInvitation.as_view()),
    url(r'^user/(?P<id>[\w\-]+)/drawCardStatus/$', userViews.DrawCardStatus.as_view()),
    # Device Id
    url(r'^user/deviceSetting/(?P<id>[\w\-]+)/$', userViews.DeviceSetting.as_view()),
    # Invitation Code
    url(r'^invitationCode/(?P<linked_code>[\w\-]+)/$', userViews.InvitationCodeGetter.as_view()),
    url(r'^checkInvitationCode/(?P<invitation_code>[\w\-]+)/$', userViews.CheckInvitationCode.as_view()),
    # Message
    url(r'^message/messageDetail/(?P<id>[\w\-]+)/$', userViews.MessageDetail.as_view()),
    url(r'^message/readMessage/(?P<message_id>[\w\-]+)/$', userViews.ReadMessage.as_view()),
    url(r'^message/updateNotification/(?P<message_id>[\w\-]+)/$', userViews.UpdateMessageNotification.as_view()),
    # Applicant
    # url(r'^typeformApplicant/$', userViews.TypeformApplicant.as_view()),
    url(r'^checkApplicant/(?P<linked_code>[\w\-]+)/$', userViews.CheckApplicant.as_view()),
    url(r'^applicant/register/(?P<token>[\w\-]+)/$', userViews.ApplicantRegister.as_view()),
    url(r'^applicant/(?P<linked_code>[\w\-]+)/$', userViews.ApplicantDetail.as_view()),
    # Report
    url(r'^report/(?P<id>[\w\-]+)/$', userViews.UserReport.as_view()),
    # Feedback
    url(r'^feedback/beta/$', userViews.BetaFeedback.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)