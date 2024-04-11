from .models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    conf_password = serializers.CharField(
        style={"input_style:password"}, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def save(self, **kwargs):
        validated_data = dict(self.validated_data)
        password = validated_data.pop('password')
        conf_password = validated_data.pop('conf_password')

        if password != conf_password:
            raise serializers.ValidationError("Passwords do not match")

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.verification_code = user.generate_verification()
        user.save()
        return user


def generate_verification():
    return 123456


class UserSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializerNormal(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ('password', "email")
