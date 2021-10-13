from django.contrib import admin

# Register your models here.
from django.contrib import admin
from work_logger.models import Project, SubProject, ShootingDay, Terms, CrewMember
# Register your models here.
admin.site.register(Project)
admin.site.register(SubProject)
admin.site.register(ShootingDay)
admin.site.register(Terms)
admin.site.register(CrewMember)


