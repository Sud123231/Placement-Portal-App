"""Cache key helpers and invalidation helpers for active cached endpoints."""

from extensions import cache


def cache_key_company_applications():
    return "companies:applications:all"


def cache_key_company_drives(company_id):
    return f"company:{company_id}:drives"


def cache_key_drive_applications(drive_id):
    return f"drive:{drive_id}:applications"


def cache_key_student_applications(student_id):
    return f"student:{student_id}:applications"


def cache_key_all_student_applications():
    return "students:applications:all"


def cache_key_student_applied_drives(student_id):
    return f"student:{student_id}:drives"


def cache_key_all_drives():
    return "drives:all"


def cache_key_all_companies():
    return "companies:all"


def cache_key_all_students():
    return "students:all"


def invalidate_drive_cache(drive_id=None):
    cache.delete(cache_key_all_drives())


def invalidate_company_drives_cache(company_id):
    cache.delete(cache_key_company_drives(company_id))


def invalidate_drive_applications_cache(drive_id):
    cache.delete(cache_key_drive_applications(drive_id))


def invalidate_student_applications_cache(student_id):
    cache.delete(cache_key_student_applications(student_id))


def invalidate_all_student_applications_cache():
    cache.delete(cache_key_all_student_applications())


def invalidate_student_applied_drives_cache(student_id):
    cache.delete(cache_key_student_applied_drives(student_id))
