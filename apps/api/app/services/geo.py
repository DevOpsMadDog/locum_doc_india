from app.core.config import settings


def within_service_area(lat: float, lng: float) -> bool:
    return (
        settings.service_area_min_lat <= lat <= settings.service_area_max_lat
        and settings.service_area_min_lng <= lng <= settings.service_area_max_lng
    )


def is_within_geofence(
    lat: float, lng: float, clinic_lat: float, clinic_lng: float, radius_m: float = 150
) -> bool:
    from math import cos, radians, sqrt

    meters_per_degree = 111_320
    dx = (lng - clinic_lng) * meters_per_degree * cos(radians((lat + clinic_lat) / 2))
    dy = (lat - clinic_lat) * meters_per_degree
    return sqrt(dx * dx + dy * dy) <= radius_m
