from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(verbose_name='modified', auto_now=True)

    class Meta:
        abstract = True


OCT_CHOICES = (
    ("1", "Main Company"),
    ("2", "Company"),
    ("3", "Purchase Organisation"),
    ("4", "Purchase Group"),
    ("5", "Location"),
    ("6", "Plants"),
    ("7", "Storage Locations"),
    ("8", "Cost Cermters"),
    ("9", "Departments"),
)


class LevelPermisions(TimeStampedModel):
    perm_name = models.CharField(max_length=50)
    category = models.CharField(
        choices=OCT_CHOICES, default='2', max_length=20)

    def __str__(self):
        return self.perm_name


class User(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def compute_permisions(self):

        obj_list = LevelMapping.objects.filter(
            ancestor=self.usermapping.level_map)

        return obj_list[0].get_levels([])


class Level(TimeStampedModel):
    level_name = models.CharField(max_length=100)
    category = models.CharField(
        choices=OCT_CHOICES, default='2', max_length=20)

    def __str__(self):
        return self.level_name


class Usermapping(TimeStampedModel):
    user = models.OneToOneField('User', on_delete=models.CASCADE, unique=True)
    level_map = models.OneToOneField('Level', on_delete=models.CASCADE)


class Permissionmapping(TimeStampedModel):
    perm = models.OneToOneField(
        'LevelPermisions', on_delete=models.CASCADE, unique=True)
    level_map = models.OneToOneField('Level', on_delete=models.CASCADE)


class LevelMapping(TimeStampedModel):
    ancestor = models.ForeignKey(
        'Level', on_delete=models.CASCADE, related_name='ancestor')
    child = models.ForeignKey(
        'Level', on_delete=models.CASCADE, related_name='child')

    def get_permission(self):
        perm = Permissionmapping.objects.filter(
            level_map=self.ancestor)
        return perm

    def get_levels(self, hierarchy=[]):
        prem = {}
        if self.child:
            prem[self.ancestor.level_name] = \
                self.ancestor.permissionmapping.perm.perm_name
            hierarchy.append(prem)
            child = LevelMapping.objects.filter(
                ancestor=self.child)
            if child:
                child[0].get_levels(hierarchy)
            else:
                prem = {}
                prem[self.child.level_name] = \
                    self.child.permissionmapping.perm.perm_name
                hierarchy.append(prem)
        return hierarchy
