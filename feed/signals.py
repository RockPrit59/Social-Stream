from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Post, Message  # <--- Added Message here
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# 1. Trigger for LIKES (Existing)
@receiver(m2m_changed, sender=Post.likes.through)
def send_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        liker_id = list(pk_set)[0] 
        liker = User.objects.get(pk=liker_id)
        
        if instance.author != liker:
            channel_layer = get_channel_layer()
            group_name = f"notification_{instance.author.id}"
            
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "send_notification",
                    "message": f"❤️ {liker.username} liked your post!"
                }
            )

# 2. NEW: Trigger for MESSAGES
@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, created, **kwargs):
    # Only trigger if a new message is created
    if created:
        channel_layer = get_channel_layer()
        # Send to the RECEIVER'S notification group
        group_name = f"notification_{instance.receiver.id}"

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": f"💬 New message from {instance.sender.username}"
            }
        )