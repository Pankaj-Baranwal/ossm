from rest_framework import permissions


class IsTeamMember(permissions.BasePermission):
    """
    Object-level permission to only allow members of a team to access it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ('HEAD', 'OPTIONS', 'GET'):
            return request.user in [obj.first_member, obj.second_member]
        return obj.first_member == request.user
