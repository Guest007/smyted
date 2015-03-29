from rest_framework import serializers


from django.apps import apps
app = apps.get_app_config('app')
Users = app.get_model('users')


class UsersSerializer(serializers.ModelSerializer):
# class UsersSerializer(serializers.Serializer):
    # title = serializers.CharField(required=False,
    #                               max_length=100)
    # id = serializers.IntegerField()
    class Meta:
        model = Users
        # fields = ('id',)
