from django.contrib import admin
from .models import TypeProduct, NewOrder, CompanyUser, OfferResponse, Payment, Category, Newsletter, Coments, \
    PrivacyPolicy, ChangeLog, Chat, CustomUser, AdditionalOrderDetails, Parametrs

def duplicate(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate.short_description = "Skopjuj wybrane elementy"

class AdminDuplicate(admin.ModelAdmin):
    actions = [duplicate]


admin.site.register(TypeProduct)
admin.site.register(NewOrder)
admin.site.register(CompanyUser)
admin.site.register(OfferResponse)
admin.site.register(Payment)
admin.site.register(Category)
admin.site.register(Newsletter, AdminDuplicate)
admin.site.register(Coments)
admin.site.register(PrivacyPolicy)
admin.site.register(ChangeLog)
admin.site.register(Chat)
admin.site.register(CustomUser)
admin.site.register(AdditionalOrderDetails)
admin.site.register(Parametrs)