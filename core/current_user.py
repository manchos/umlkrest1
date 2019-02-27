from profiles.models import CustomUser


class Current(object):

    region = None
    region_user = None

    def is_region(self, user):

        if self.region_user:
            return True
        else:
            if (user is not None and
                    user.groups.filter(name='федеральный округ').exists()):
                self.region_user = CustomUser.objects.get(pk=user.id)
                self.region = self.region_user.region
                return True
            else:
                return False

current = Current()
