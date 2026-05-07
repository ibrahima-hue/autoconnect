from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import User, AuditLog, PlatformSettings
from .serializers import UserSerializer
from cars.models import Car, Seller, Appointment, Report
from datetime import datetime


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.user_type == 'admin')


# ── Global stats ──────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_stats(request):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)

    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    total_users = User.objects.count()
    new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
    total_cars = Car.objects.count()
    active_cars = Car.objects.filter(is_available=True).count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    confirmed_appointments = Appointment.objects.filter(status='confirmed').count()
    total_sellers = Seller.objects.count()
    verified_sellers = Seller.objects.filter(is_verified=True).count()
    pending_reports = Report.objects.filter(status='pending').count()
    banned_users = User.objects.filter(is_banned=True).count()

    buyers = User.objects.filter(user_type='buyer').count()
    sellers = User.objects.filter(user_type='seller').count()

    # Fuel breakdown
    fuel_stats = list(Car.objects.values('fuel').annotate(count=Count('id')).order_by('-count'))

    # Location breakdown
    location_stats = list(Car.objects.values('location').annotate(count=Count('id')).order_by('-count')[:5])

    # Recent activity (last 10 appointments)
    recent_appts = Appointment.objects.select_related('car', 'buyer', 'seller').order_by('-created_at')[:10]
    activity = [{
        'id': a.id,
        'type': 'appointment',
        'date': a.created_at.strftime('%d/%m/%Y %H:%M'),
        'text': f"{a.buyer.get_full_name() or a.buyer.email} → {a.car.make} {a.car.model}",
        'status': a.status,
    } for a in recent_appts]

    return Response({
        'users': {
            'total': total_users,
            'buyers': buyers,
            'sellers': sellers,
            'new_this_week': new_users_week,
        },
        'cars': {
            'total': total_cars,
            'active': active_cars,
            'inactive': total_cars - active_cars,
            'fuel_breakdown': fuel_stats,
            'top_locations': location_stats,
        },
        'appointments': {
            'total': total_appointments,
            'pending': pending_appointments,
            'confirmed': confirmed_appointments,
            'cancelled': Appointment.objects.filter(status='cancelled').count(),
        },
        'sellers': {
            'total': total_sellers,
            'verified': verified_sellers,
            'unverified': total_sellers - verified_sellers,
        },
        'reports': {
            'pending': pending_reports,
        },
        'security': {
            'banned_users': banned_users,
        },
        'recent_activity': activity,
    })


# ── User management ───────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users(request):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)

    users = User.objects.all().order_by('-date_joined')
    q = request.query_params.get('q', '')
    if q:
        users = users.filter(Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
    user_type = request.query_params.get('type', '')
    if user_type:
        users = users.filter(user_type=user_type)

    data = [{
        'id': u.id,
        'email': u.email,
        'name': u.get_full_name() or u.email,
        'user_type': u.user_type,
        'is_active': u.is_active,
        'is_staff': u.is_staff,
        'is_banned': u.is_banned,
        'ban_reason': u.ban_reason,
        'ban_until': u.ban_until.isoformat() if u.ban_until else None,
        'account_status': u.account_status,
        'date_joined': u.date_joined.strftime('%d/%m/%Y'),
        'avatar_initials': u.avatar_initials,
        'report_count': u.seller_profile.reports_received.count() if hasattr(u, 'seller_profile') else 0,
    } for u in users]
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_user_update(request, pk):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'Utilisateur introuvable'}, status=404)

    allowed = ['is_active', 'user_type', 'is_staff']
    for field in allowed:
        if field in request.data:
            setattr(user, field, request.data[field])
    user.save()
    AuditLog.objects.create(
        admin=request.user,
        action='update_user',
        target_type='user',
        target_id=user.pk,
        target_repr=str(user),
        note=f"Champs modifiés: {', '.join(k for k in request.data if k in allowed)}",
    )
    return Response({'success': True, 'user': UserSerializer(user).data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_user_delete(request, pk):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)
    if str(request.user.pk) == str(pk):
        return Response({'error': 'Impossible de supprimer votre propre compte'}, status=400)
    try:
        User.objects.get(pk=pk).delete()
    except User.DoesNotExist:
        return Response({'error': 'Introuvable'}, status=404)
    return Response(status=204)


# ── Car management ────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_cars(request):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)

    cars = Car.objects.select_related('seller').all().order_by('-created_at')
    q = request.query_params.get('q', '')
    if q:
        cars = cars.filter(Q(make__icontains=q) | Q(model__icontains=q))

    data = [{
        'id': c.id,
        'make': c.make, 'model': c.model, 'year': c.year,
        'price': float(c.price), 'mileage': c.mileage,
        'fuel': c.fuel, 'location': c.location,
        'image': c.image, 'badge': c.badge,
        'is_available': c.is_available,
        'seller_name': c.seller.name if c.seller else '—',
        'seller_verified': c.seller.is_verified if c.seller else False,
        'created_at': c.created_at.strftime('%d/%m/%Y'),
        'appointment_count': c.appointments.count(),
    } for c in cars]
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_car_update(request, pk):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response({'error': 'Voiture introuvable'}, status=404)
    if 'is_available' in request.data:
        car.is_available = request.data['is_available']
    car.save()
    return Response({'success': True})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_car_delete(request, pk):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)
    try:
        Car.objects.get(pk=pk).delete()
    except Car.DoesNotExist:
        return Response({'error': 'Introuvable'}, status=404)
    return Response(status=204)


# ── Seller verification ───────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_sellers(request):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)

    sellers = Seller.objects.all().order_by('-is_premium', '-created_at')
    data = [{
        'id': s.id,
        'name': s.name,
        'seller_type': s.seller_type,
        'avatar': s.avatar,
        'rating': float(s.rating),
        'review_count': s.review_count,
        'location': s.location,
        'phone': s.phone,
        'is_verified': s.is_verified,
        'is_premium': s.is_premium,
        'premium_until': s.premium_until.isoformat() if s.premium_until else None,
        'premium_requested': s.premium_requested,
        'plan': s.plan,
        'car_count': s.cars.count(),
        'appointment_count': s.appointments.count(),
        'report_count': s.reports_received.count(),
    } for s in sellers]
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_seller_verify(request, pk):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)
    try:
        seller = Seller.objects.get(pk=pk)
    except Seller.DoesNotExist:
        return Response({'error': 'Vendeur introuvable'}, status=404)
    seller.is_verified = request.data.get('is_verified', not seller.is_verified)
    seller.save()
    return Response({'success': True, 'is_verified': seller.is_verified})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_seller_premium(request, pk):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)
    try:
        seller = Seller.objects.get(pk=pk)
    except Seller.DoesNotExist:
        return Response({'error': 'Vendeur introuvable'}, status=404)

    action = request.data.get('action', 'activate')
    months = int(request.data.get('months', 1))

    if action == 'activate':
        from django.utils import timezone as tz
        seller.is_premium = True
        seller.premium_requested = False
        if seller.premium_until and seller.premium_until > tz.now():
            seller.premium_until = seller.premium_until + timedelta(days=30 * months)
        else:
            seller.premium_until = tz.now() + timedelta(days=30 * months)
        AuditLog.objects.create(
            admin=request.user, action='activate_premium',
            target_type='seller', target_id=seller.pk,
            target_repr=seller.name,
            note=f"{months} mois — expire {seller.premium_until.strftime('%d/%m/%Y')}",
        )
    elif action == 'deactivate':
        seller.is_premium = False
        seller.premium_until = None
        seller.premium_requested = False
        AuditLog.objects.create(
            admin=request.user, action='deactivate_premium',
            target_type='seller', target_id=seller.pk,
            target_repr=seller.name, note='',
        )

    seller.save()
    return Response({'success': True, 'plan': seller.plan, 'is_premium': seller.is_premium, 'premium_until': seller.premium_until.isoformat() if seller.premium_until else None})


# ── Appointments management ───────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_appointments(request):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)

    appts = Appointment.objects.select_related('car', 'buyer', 'seller').order_by('-created_at')
    status_filter = request.query_params.get('status', '')
    if status_filter:
        appts = appts.filter(status=status_filter)

    data = [{
        'id': a.id,
        'car': f"{a.car.make} {a.car.model} {a.car.year}",
        'buyer': a.buyer.get_full_name() or a.buyer.email,
        'seller': a.seller.name,
        'date': str(a.date),
        'time': str(a.time)[:5],
        'status': a.status,
        'created_at': a.created_at.strftime('%d/%m/%Y'),
    } for a in appts]
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_appointment_update(request, pk):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)
    try:
        appt = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({'error': 'Introuvable'}, status=404)
    if 'status' in request.data:
        appt.status = request.data['status']
        appt.save()
    return Response({'success': True})


# ── Ban / Suspend user ────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_ban_user(request, pk):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)
    if str(request.user.pk) == str(pk):
        return Response({'error': 'Impossible de vous bannir vous-même'}, status=400)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'Utilisateur introuvable'}, status=404)

    action = request.data.get('action')  # 'ban', 'suspend', 'unban', 'unsuspend'
    reason = request.data.get('reason', '')
    duration_days = request.data.get('duration_days')

    if action == 'ban':
        user.is_banned = True
        user.ban_reason = reason
        user.ban_until = None
        user.is_active = True
        audit_action = 'ban_user'
    elif action == 'suspend':
        user.is_active = False
        user.is_banned = False
        user.ban_reason = reason
        user.ban_until = timezone.now() + timedelta(days=int(duration_days)) if duration_days else None
        audit_action = 'suspend_user'
    elif action == 'unban':
        user.is_banned = False
        user.ban_reason = ''
        user.ban_until = None
        audit_action = 'unban_user'
    elif action == 'unsuspend':
        user.is_active = True
        user.ban_reason = ''
        user.ban_until = None
        audit_action = 'unsuspend_user'
    else:
        return Response({'error': 'Action invalide'}, status=400)

    user.save()
    AuditLog.objects.create(
        admin=request.user,
        action=audit_action,
        target_type='user',
        target_id=user.pk,
        target_repr=str(user),
        note=reason,
    )
    return Response({'success': True, 'account_status': user.account_status})


# ── Reports management ────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_reports(request):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)

    reports = Report.objects.select_related('reporter', 'seller', 'car').order_by('-created_at')
    status_filter = request.query_params.get('status', '')
    if status_filter:
        reports = reports.filter(status=status_filter)

    data = [{
        'id': r.id,
        'reporter_email': r.reporter.email,
        'reporter_name': r.reporter.get_full_name() or r.reporter.email,
        'seller_id': r.seller.id,
        'seller_name': r.seller.name,
        'car_id': r.car.id if r.car else None,
        'car_label': f"{r.car.make} {r.car.model} {r.car.year}" if r.car else '—',
        'reason': r.reason,
        'reason_label': dict(Report.REASON_CHOICES).get(r.reason, r.reason),
        'description': r.description,
        'status': r.status,
        'admin_note': r.admin_note,
        'admin_action': r.admin_action,
        'created_at': r.created_at.strftime('%d/%m/%Y %H:%M'),
    } for r in reports]
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_report_update(request, pk):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)
    try:
        report = Report.objects.select_related('seller', 'car', 'seller__user').get(pk=pk)
    except Report.DoesNotExist:
        return Response({'error': 'Signalement introuvable'}, status=404)

    new_status = request.data.get('status', report.status)
    admin_note = request.data.get('admin_note', report.admin_note)
    admin_action = request.data.get('admin_action', report.admin_action)

    report.status = new_status
    report.admin_note = admin_note
    report.admin_action = admin_action
    report.save()

    # Apply action to the target
    if admin_action == 'suspend_car' and report.car:
        report.car.is_available = False
        report.car.save()
    elif admin_action == 'warn' and report.seller.user:
        pass  # notification system placeholder
    elif admin_action in ('suspend_user', 'ban_user') and report.seller.user:
        target_user = report.seller.user
        if admin_action == 'ban_user':
            target_user.is_banned = True
            target_user.ban_reason = admin_note or f"Signalement #{report.pk}"
        else:
            target_user.is_active = False
            target_user.ban_reason = admin_note or f"Signalement #{report.pk}"
        target_user.save()

    AuditLog.objects.create(
        admin=request.user,
        action=f'handle_report_{admin_action or new_status}',
        target_type='report',
        target_id=report.pk,
        target_repr=f"Report #{report.pk} — {report.seller.name}",
        note=admin_note,
    )
    return Response({'success': True})


# ── Platform settings ─────────────────────────────────────────────────────────

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def admin_platform_settings(request):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)

    cfg = PlatformSettings.get()

    if request.method == 'PATCH':
        changed = []
        if 'premium_enabled' in request.data:
            old = cfg.premium_enabled
            cfg.premium_enabled = bool(request.data['premium_enabled'])
            if cfg.premium_enabled != old:
                changed.append(f"premium_enabled → {cfg.premium_enabled}")
        cfg.updated_by = request.user
        cfg.save()

        if changed:
            AuditLog.objects.create(
                admin=request.user,
                action='update_platform_settings',
                target_type='settings',
                target_id=1,
                target_repr='PlatformSettings',
                note=', '.join(changed),
            )

    return Response({
        'premium_enabled': cfg.premium_enabled,
        'updated_at': cfg.updated_at.isoformat() if cfg.updated_at else None,
        'updated_by': cfg.updated_by.email if cfg.updated_by else None,
    })


# ── Audit log ─────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_audit_log(request):
    if not is_admin(request.user):
        return Response({'error': 'Accès refusé'}, status=403)

    logs = AuditLog.objects.select_related('admin').order_by('-created_at')[:100]
    data = [{
        'id': l.id,
        'admin': l.admin.email if l.admin else 'Système',
        'admin_name': l.admin.get_full_name() if l.admin else 'Système',
        'action': l.action,
        'target_type': l.target_type,
        'target_id': l.target_id,
        'target_repr': l.target_repr,
        'note': l.note,
        'created_at': l.created_at.strftime('%d/%m/%Y %H:%M'),
    } for l in logs]
    return Response(data)
