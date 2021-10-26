from django.db import models
from django.conf import settings
# Create your models here.
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('subprojects-view', args=(self.pk, ))

    def get_delete_url(self):
        return reverse('delete_project_view', args=(self.pk, ))

    def get_update_url(self):
        return reverse('update_project_view', args=(self.pk,))

    def __str__(self):
        return self.name


class SubProject(models.Model):
    parent = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    terms = models.ForeignKey('Terms', null=True, on_delete=models.SET_NULL)
    crew_members = models.ManyToManyField('CrewMember')
    description = models.CharField(max_length=512, null=True)

    def get_absolute_url(self):
        return reverse('shooting-days-view', args=(self.pk, ))

    def get_delete_url(self):
        return reverse('delete_subproject_view', args=(self.pk,))

    def get_update_url(self):
        return reverse('update_subproject_view', args=(self.pk,))

    def get_detail_url(self):
        return reverse('subproject_detail_view', args=(self.pk,))

    def __str__(self):
        return self.name


PAY_PERIODS = (
    ('', 'Select Pay Period'),
    (1, "Daily"),
    (2, "Weekly"),
    (3, "Monthly"),
    (4, "Per Job"),
)

WORKING_HOURS = (
    ('', 'Select Working Hours'),
    (1, "10hr Continuous Day"),
    (2, "11hr Day"),
    (3, "12hr Day")
)


class Terms(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pay_period = models.IntegerField(choices=PAY_PERIODS)
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    ot_rate = models.DecimalField(max_digits=10, decimal_places=2)
    camera_ot_rate = models.DecimalField(max_digits=10, decimal_places=2)
    extras = models.DecimalField(max_digits=10, decimal_places=2)
    working_hours = models.IntegerField(choices=WORKING_HOURS)
    description = models.CharField(max_length=512, null=True)

    # def get_absolute_url(self):
    #     return reverse('detail_terms_view', args=(self.pk,))

    def __str__(self):
        return self.name

    def get_delete_url(self):
        return reverse('delete_terms', args=(self.pk,))

    def get_update_url(self):
        return reverse('update_terms', args=(self.pk,))


class CrewMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    position = models.CharField(max_length=128)
    contact_info = models.TextField(null=True)

    def get_update_url(self):
        return reverse('update_crew_member', args=(self.pk,))

    def get_delete_url(self):
        return reverse('delete_crew_member', args=(self.pk,))

    def __str__(self):
        return f"{self.name} {self.surname}"


class ShootingDay(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField()
    description = models.CharField(max_length=512, null=True)
    start_hour = models.DateTimeField()
    end_hour = models.DateTimeField()
    ot = models.IntegerField()
    camera_ot = models.IntegerField()
    toc = models.IntegerField()
    extras = models.DecimalField(max_digits=10, decimal_places=2)
    subproject = models.ForeignKey(SubProject, on_delete=models.CASCADE)

    def get_delete_url(self):
        return reverse('delete_shootingday_view', args=(self.pk,))

    def get_update_url(self):
        return reverse('update_shootingday_view', args=(self.pk,))

    def get_absolute_url(self):
        return reverse('shootingday_detail_view', args=(self.pk,))

    def __str__(self):
        return f"{self.date} - {self.name}"
