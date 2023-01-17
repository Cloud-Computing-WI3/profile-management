from allauth.account.adapter import DefaultAccountAdapter


# Subclassing the DefaultAccountAdapter from the allauth library
class AccountAdapter(DefaultAccountAdapter):

    # overriding the save_user method
    def save_user(self, request, user, form, commit=False):
        # call the parent class's save_user method to perform default behavior
        user = super().save_user(request, user, form, commit)
        # retrieve additional data from the form's cleaned_data attribute
        data = form.cleaned_data
        # set the given_name, family_name, and picture fields received from google-auth on the user object
        user.given_name = data.get("given_name")
        user.family_name = data.get("family_name")
        user.picture = data.get("picture")
        # save the user object to the database
        user.save()
        # return the user object
        return user
