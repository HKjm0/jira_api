from rest_framework import permissions


class OwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):  # override
        if request.method in permissions.SAFE_METHODS:  # GETメソッドなどデータの内容を変えたりするメソッドではない物にあたる
            return True  # Trueは許可するという意味
        return obj.owner.id == request.user.id  # データを返るようなメソッドがきた場合はownerがログインユーザーであればTrueを返す
