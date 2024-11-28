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

        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update roles if provided
        if roles is not None:
            role_instances = []
            for role_name in roles:
                role, created = Role.objects.get_or_create(role=role_name)
                role_instances.append(role)
            instance.roles.set(role_instances)
        return instance


'''class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField( 
        slug_field='role',
        queryset=Role.objects.all(),  
        many=True 
    )

    class Meta:
        model=User
        fields=['username','firstname','lastname','password','email','roles']
        #fields='__all__'
    def validate_roles(self, roles):
        """
        Ensure roles exist in the database. If they don't, create them dynamically.
        """
        role_instances = []
        for role_name in roles:
            role, created = Role.objects.get_or_create(role=role_name)  # Create if not exists
            role_instances.append(role)
        return role_instances

    def create(self, validated_data): 
        roles = validated_data.pop('roles',[]) 
        validated_data['roles'] = self.validate_roles(roles)  # Create or get roles dynamically
        user = User.objects.create(**validated_data) 
        user.roles.set(validated_data['roles']) 
        return user    

    def update(self, instance, validated_data): 
        roles = validated_data.pop('roles', None) 
        if roles is not None:
            validated_data['roles'] = self.validate_roles(roles)  # Create or get roles dynamically
            instance.roles.set(validated_data['roles'])
        instance.username = validated_data.get('username', instance.username) 
        instance.firstname = validated_data.get('firstname', instance.firstname) 
        instance.lastname = validated_data.get('lastname', instance.lastname) 
        instance.email = validated_data.get('email', instance.email) 
        instance.save() 
        return instance
    -------------------------------------
    def create(self, validated_data): 
        roles = validated_data.pop('roles') 
        user = User.objects.create(**validated_data) 
        user.roles.set(roles) 
        return user    

    def update(self, instance, validated_data): 
        roles = validated_data.pop('roles', None) 
        instance.username = validated_data.get('username', instance.username) 
        instance.firstname = validated_data.get('firstname', instance.firstname) 
        instance.lastname = validated_data.get('lastname', instance.lastname) 
        instance.email = validated_data.get('email', instance.email) 
        instance.save() 
        if roles is not None: 
            # Ensure roles exist and create them if they don't 
            role_instances = [] 
            for role_name in roles: 
                role, created = Role.objects.get_or_create(role=role_name) 
                role_instances.append(role) 
            instance.roles.set(role_instances) 
        return instance
'''