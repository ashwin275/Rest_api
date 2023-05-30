from rest_framework import serializers,validators
from users.models import CustomUser


class UserSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','password','email']
        extra_kwargs = {
            'password':{'write_only':True},
             'email':{
                'required':True,
                'allow_blank':False,
                'validators':[
                    validators.UniqueValidator(
                        CustomUser.objects.all(),'A user with this Email is already exists'
                    )
                ]
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
    


class UserLIstSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','profile']


        def update(self,instance,validated_data):
            image = validated_data.pop('profile',None)
            instance = super().update(instance,validated_data)

            if image:
                instance.image = image
                instance.save()
                return instance