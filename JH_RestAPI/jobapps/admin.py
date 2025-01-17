from django.contrib import admin
from .models import JobApplication, ApplicationStatus, Source, GoogleMail, SourceType
from utils.export_csv import ExportCsv

# Register your models here.
@admin.register(JobApplication)
class CompanyAdmin(admin.ModelAdmin, ExportCsv):
    list_display = ("user", "applicationStatus", "position",
                    'companyObject', 'app_source', 'isDeleted')
    list_filter = ("user", "applicationStatus", "position",
                   'companyObject', 'app_source')
    actions = ["export_as_csv"]


@admin.register(GoogleMail)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "job_post", "subject", "app_source")
    list_filter = ("user", "job_post", "subject", "app_source")


admin.site.register(ApplicationStatus)
admin.site.register(Source)
admin.site.register(SourceType)
