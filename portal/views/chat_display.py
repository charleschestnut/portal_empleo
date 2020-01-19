from ..models import Profile, LabourChat, ChatMessage
from ..forms import ChatMessageForm
from django.shortcuts import render, redirect
import datetime
from django.contrib.auth.decorators import login_required


@login_required
def chat_display(request, id):
    def remove_exceed_messages(list):
        if len(messages_list) > 10:
            for message in messages_list[:(len(messages_list) - 10)]:
                message.delete()
        return list

    def read_new_messages(list):
        im_worker = actual_profile == actual_chat.labour.worker
        print("I AM WORKER? -> " + str(im_worker))
        print("list before if:", list)
        if not im_worker:
            messages_to_read = list.filter(owner__id=actual_chat.labour.worker_id).filter(is_read=False)
            messages_to_read.update(is_read=True)
        else:
            messages_to_read = list.filter(owner__id=actual_chat.labour.creator_id).filter(is_read=False)
            messages_to_read.update(is_read=True)

        print("LIST: " + str(list))
        for messag in messages_to_read:
            print(messag.is_read)
            messag.save()
            print(messag.is_read)
        print("LIST AFTER SAVE:" +str(list))

    actual_profile = Profile.objects.get(user_id=request.user.id)
    actual_chat = LabourChat.objects.get(labour__id=int(id))

    if actual_profile == actual_chat.labour.worker or actual_profile == actual_chat.labour.creator:
        context = {}

        if actual_profile == actual_chat.labour.creator:
            title = "Chat with " + str(actual_chat.labour.worker.user.first_name)
        else:
            title = "Chat with " + str(actual_chat.labour.creator.user.first_name)
        context['title'] = title

        if request.method == 'POST':
            chat_message_form = ChatMessageForm(request.POST)

            if chat_message_form.is_valid():
                send_datetime = datetime.datetime.now()
                chat = actual_chat
                owner = actual_profile
                content = chat_message_form.cleaned_data['content']

                message = ChatMessage(
                    content=content,
                    send_datetime=send_datetime,
                    is_read=False,
                    chat=chat,
                    owner=owner
                )
                message.save()

            messages_list = ChatMessage.objects.filter(chat_id=actual_chat.id).order_by('send_datetime')

            # Nos quedamos sólo con los cinco últimos mensajes
            messages_list = remove_exceed_messages(messages_list)
            read_new_messages(messages_list)

            context['messages_list'] = messages_list
            return redirect('chat_display', id=int(id))
        else:

            chat_message_form = ChatMessageForm()
            messages_list = ChatMessage.objects.filter(chat_id=actual_chat.id).order_by('send_datetime')

            # Nos quedamos sólo con los cinco últimos mensajes
            messages_list = remove_exceed_messages(messages_list)
            read_new_messages(messages_list)

            context['chat_message_form'] = chat_message_form
            context['labour_id'] = int(id)
            context['messages_list'] = messages_list


            return render(request, 'chat_display.html', context)

    else:
        return redirect('searchlist')
