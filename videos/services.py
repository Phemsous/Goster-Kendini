from .models import Video, Comment, VideoReaction


def create_video_service(user, title, video_url, category):
    return Video.objects.create(
        user=user,
        title=title,
        video_url=video_url,
        category=category
    )


def create_comment_service(user, video, content):
    return Comment.objects.create(
        user=user,
        video=video,
        content=content
    )


def react_to_video_service(user, video, reaction_type):
    reaction, created = VideoReaction.objects.get_or_create(
        user=user,
        video=video,
        defaults={'reaction_type': reaction_type}
    )

    if not created:
        if reaction.reaction_type == reaction_type:
            return reaction
        reaction.reaction_type = reaction_type
        reaction.save()

    like_count = VideoReaction.objects.filter(video=video, reaction_type='like').count()
    dislike_count = VideoReaction.objects.filter(video=video, reaction_type='dislike').count()

    video.like_count = like_count
    video.dislike_count = dislike_count
    video.save()

    return reaction