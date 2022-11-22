from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.given_name = data.get("given_name")
        user.family_name = data.get("family_name")
        user.picture = data.get("picture")
        user.save()
        return user