from rest_framework import serializers
from .models import User,Role



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields='__all__' 

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(  # Accepts a list of role names as input
        child=serializers.CharField(max_length=50),  # Ensure each role is a string
        write_only=True  # Roles will only be used during creation or update, not in the output
    )
    assigned_roles = serializers.SerializerMethodField(read_only=True)  # Read-only field to show roles

    class Meta:
        model = User
        fields = ['username', 'firstname', 'lastname', 'password', 'email', 'roles', 'assigned_roles']

    def get_assigned_roles(self, obj):
        """Retrieve roles assigned to the user as a list of role names."""
        return [role.role for role in obj.roles.all()]

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        user = User.objects.create(**validated_data)
        #user.set_password('password')
        # Create or get roles and assign them to the user
        for role_name in roles:
            role, created = Role.objects.get_or_create(role=role_name)
            user.roles.add(role)
        return user

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles', None)

        
        instance.username = validated_data.get('username', instance.username)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Updating roles if provided
        if roles is not None:
            role_instances = []
            for role_name in roles:
                role, created = Role.objects.get_or_create(role=role_name)
                role_instances.append(role)
            instance.roles.set(role_instances)
        return instance


