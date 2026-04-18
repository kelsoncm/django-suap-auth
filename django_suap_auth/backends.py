from django.contrib.auth import get_user_model

from .utils import apply_user_attr_map, get_suap_settings


class SuapAuthBackend:
    """
    Django authentication backend for SUAP OAuth2.

    Looks up or creates a Django user based on the profile info returned by SUAP.

    By default the matricula is used as the Django ``username``. Customize the field
    mapping via ``SUAP_USER_LOOKUP_FIELD`` and ``SUAP_USER_ATTR_MAP`` in your
    Django settings — see the documentation for details.
    """

    def authenticate(self, request, suap_user_info=None, **kwargs):
        if suap_user_info is None:
            return None

        cfg = get_suap_settings()
        lookup_field = cfg["user_lookup_field"]
        attr_map = cfg["user_attr_map"]
        json_field = cfg["json_field"]

        User = get_user_model()
        attrs = apply_user_attr_map(suap_user_info, attr_map)

        if json_field:
            attrs[json_field] = suap_user_info

        lookup_value = attrs.get(lookup_field)
        if not lookup_value:
            return None

        defaults = {k: v for k, v in attrs.items() if k != lookup_field}
        defaults.setdefault("is_active", True)

        user, created = User.objects.get_or_create(
            **{lookup_field: lookup_value},
            defaults=defaults,
        )

        if not created:
            changed = False
            for field, value in defaults.items():
                if getattr(user, field, None) != value:
                    setattr(user, field, value)
                    changed = True
            if not user.is_active:
                user.is_active = True
                changed = True
            if changed:
                user.save()

        return user

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
