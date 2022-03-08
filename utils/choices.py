class BaseChoiceClass:
    @classmethod
    def get_choice_list(self):
        return [x[0] for x in self.CHOICES]

    @classmethod
    def get_value_list(self):
        return [x[1] for x in self.CHOICES]

    @classmethod
    def get_value_display(self, choice):
        for x in self.CHOICES:
            if x[0] == choice:
                return x[1]
        return None


class Role(BaseChoiceClass):
    SUPERUSER = "SU"
    USER = "US"

    CHOICES = (
        (SUPERUSER, "Superuser"),
        (USER, "User"),
    )
