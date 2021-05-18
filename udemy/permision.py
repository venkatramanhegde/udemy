from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    message = "This user does not have permission."

    def has_permission(self, request, view):
        instructor = request.user.is_instructor == True
        return instructor


class IsStudents(BasePermission):
    message = "This user does not have permission."

    def has_permission(self, request, view):
        students = request.user.is_student == True
        return students