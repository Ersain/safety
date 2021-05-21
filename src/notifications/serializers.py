from rest_framework import serializers

from .models import Notification, Achievement


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title', 'body', 'is_read', 'created_at')


class AchievementSerializer(serializers.ModelSerializer):
    is_done = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = ('id', 'title', 'body', 'is_done', 'created_at')

    def get_is_done(self, obj):
        request = self.context.get('request')
        user = request.user.profile
        if obj in user.achievements.all():
            return True
        return False
