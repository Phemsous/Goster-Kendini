from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import User
from .models import Message

@login_required
def inbox(request):
    # Kullanıcının konuşma yaptığı kişileri bul
    messages_qs = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )
    
    # Her konuşmadaki son mesajı bul
    conversations = {}
    for msg in messages_qs:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        if other_user.id not in conversations:
            conversations[other_user.id] = {
                'user': other_user,
                'last_message': msg,
                'unread_count': 0
            }
        else:
            conversations[other_user.id]['last_message'] = msg
    
    # Okunmamış mesaj sayısı
    for conv in conversations.values():
        conv['unread_count'] = Message.objects.filter(
            sender=conv['user'],
            receiver=request.user,
            is_read=False
        ).count()

    return render(request, 'messaging/inbox.html', {
        'conversations': conversations.values()
    })


@login_required
def conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        return redirect('inbox')

    # Mesajları getir
    messages_qs = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    )

    # Okunmamışları okundu yap
    messages_qs.filter(receiver=request.user, is_read=False).update(is_read=True)

    # Yeni mesaj gönder
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
        return redirect('conversation', user_id=user_id)

    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'messages': messages_qs,
    })


@login_required
def unread_count(request):
    from django.http import JsonResponse
    count = Message.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({'count': count})