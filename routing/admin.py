from django.contrib import admin
from .models import Location, RiskScore, Route, RouteSegment

admin.site.register(Location)
admin.site.register(RiskScore)
admin.site.register(Route)
admin.site.register(RouteSegment)
