from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from accounts.models import User
from .models import Message


@login_required
def inbox(request):
    sent_to = Message.objects.filter(
        sender=request.user
    ).values_list('receiver_id', flat=True).distinct()

    received_from = Message.objects.filter(
        receiver=request.user
    ).values_list('sender_id', flat=True).distinct()

    partner_ids = set(list(sent_to) + list(received_from))
    partners = User.objects.filter(id__in=partner_ids)

    conversations = []
    for partner in partners:
        last_msg = Message.objects.filter(
            Q(sender=request.user, receiver=partner) |
            Q(sender=partner, receiver=request.user)
        ).order_by('-created_at').first()

        unread = Message.objects.filter(
            sender=partner,
            receiver=request.user,
            is_read=False
        ).count()

        conversations.append({
            'user': partner,
            'last_message': last_msg,
            'unread_count': unread,
        })

    conversations.sort(
        key=lambda x: x['last_message'].created_at if x['last_message'] else 0,
        reverse=True
    )

    return render(request, 'messaging/inbox.html', {
        'conversations': conversations
    })


@login_required
def conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect('inbox')

    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at').select_related('sender', 'receiver')

    chat_messages.filter(
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

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
        'chat_messages': chat_messages,
    })


@login_required
def unread_count(request):
    count = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()
    return JsonResponse({'count': count})