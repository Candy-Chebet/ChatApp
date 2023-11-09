from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # Import the CSRF exemption decorator

from .models import Room, Message

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)

    if request.method == 'POST':
        # Handle the HTTP POST request for sending a message
        message_content = request.POST.get('content', '')

        if message_content:
            # Save the message to the database
            message = Message.objects.create(user=request.user, room=room, content=message_content)

            # Respond with a JSON success status
            return JsonResponse({'status': 'success', 'message_id': message.id})
        else:
            # Respond with a JSON error status
            return JsonResponse({'status': 'error', 'message': 'Message content is empty'})

    # Retrieve messages for the room
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'room/room.html', {'room': room, 'messages': messages})
