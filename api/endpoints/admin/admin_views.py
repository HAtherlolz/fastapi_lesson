from sqladmin import ModelView

from api.models.profile import Profile


class ProfileAdmin(ModelView, model=Profile):
    name = "Profile"
    name_plural = "Profiles"
    icon = "fa-solid fa-person"
    column_list = [Profile.id, Profile.email, Profile.first_name]
    column_searchable_list = [Profile.id, Profile.email, Profile.first_name]




admin_models = [
    ProfileAdmin
]
