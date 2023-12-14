from django.urls import path

from main.apps import MainConfig
from main.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, MailingCreateView, \
    MailingUpdateView, MailingDeleteView, MailingListView, MailingDetailView, HomeView, MessageCreateView, \
    MessageListView, MessageUpdateView, MessageDeleteView, LogsListView, MyMailing

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my_mailing', MyMailing.as_view(), name='my_mailing'),
    path('client_list', ClientListView.as_view(), name='client_list'),
    path('create_client', ClientCreateView.as_view(), name='create_client'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('create_mailing', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing_list', MailingListView.as_view(), name='mailing_list'),
    path('mailing_detail/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('update_mailing/<int:pk>', MailingUpdateView.as_view(), name='update_mailing'),
    path('delete_mailing/<int:pk>', MailingDeleteView.as_view(), name='delete_mailing'),

    path('create_message', MessageCreateView.as_view(), name='create_message'),
    path('msg_list', MessageListView.as_view(), name='msg_list'),
    path('update_message/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),

    path('logfile_list/', LogsListView.as_view(), name='logfile_list'),
]