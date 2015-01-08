# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


PURCHASE_STATES = (
    ('incomplete', _('Purchase incomplete')),
    ('new', _('new')),
    ('invoice_created', _('invoice created')),
    ('payment_received', _('payment received')),
    ('canceled', _('canceled'))
)

PAYMENT_METHOD_CHOICES = (
    ('invoice', _('Invoice')),
    ('creditcard', _('Credit card')),
    ('elv', _('ELV')),
)

GENDER_CHOICES = (
    ('female', _('female')),
    ('male', _('male')),
)


class VoucherTypeManager(models.Manager):
    use_in_migrations = True


class VoucherType(models.Model):
    conference = models.ForeignKey(
        "conference.Conference", verbose_name="conference", null=True,
        on_delete=models.PROTECT)
    name = models.CharField(_('voucher type'), max_length=50)

    objects = VoucherTypeManager()

    class Meta(object):
        verbose_name = _('voucher type')
        verbose_name_plural = _('voucher types')


class VoucherManager(models.Manager):
    use_in_migrations = True


class Voucher(models.Model):
    code = models.CharField(
        _('Code'), max_length=12, blank=True,
        help_text=_('Can be left blank, code will be created when you save.'))
    remarks = models.CharField(_('Remarks'), max_length=254, blank=True)
    date_valid = models.DateTimeField(
        _('Date (valid)'), blank=False,
        help_text=_('The voucher is valid until this date'))
    is_used = models.BooleanField(_('Is used'), default=False)
    type = models.ForeignKey('VoucherType', verbose_name=_('voucher type'),
                             null=True)

    objects = VoucherManager()

    class Meta:
        verbose_name = _('Voucher')
        verbose_name_plural = _('Vouchers')


class TicketTypeManager(models.Manager):
    use_in_migrations = True


class TicketType(models.Model):
    conference = models.ForeignKey(
        "conference.Conference", verbose_name="conference", null=True,
        on_delete=models.PROTECT)
    product_number = models.IntegerField(
        _('Product number'), blank=True,
        help_text=_('Will be created when you save the first time.'))

    name = models.CharField(_('Name'), max_length=50)
    fee = models.FloatField(_('Fee'), default=0)

    max_purchases = models.PositiveIntegerField(
        _('Max. purchases'),
        default=0, help_text=_('0 means no limit'))

    is_active = models.BooleanField(_('Is active'), default=False)
    is_on_desk_active = models.BooleanField(_('Allow on desk purchase'), default=False)

    date_valid_from = models.DateTimeField(_('Sale start'), blank=False)
    date_valid_to = models.DateTimeField(_('Sale end'), blank=False)

    valid_on = models.DateField(_('Valid on'), blank=True, null=True)

    vouchertype_needed = models.ForeignKey('VoucherType', null=True, blank=True,
        verbose_name=_('voucher type needed'))
    tutorial_ticket = models.BooleanField(_('Tutorial ticket'), default=False)

    remarks = models.TextField(_('Remarks'), blank=True)

    # Various settings for making tickets editable
    allow_editing = models.NullBooleanField(_('Allow editing'))
    editable_fields = models.TextField(_('Editable fields'), blank=True)
    editable_until = models.DateTimeField(_('Editable until'), blank=True, null=True)

    prevent_invoice = models.BooleanField(_("Conditionally prevent invoice to user"),
        default=False, blank=True,
        help_text=_('If checked, a purchase, that contains only tickets of '
                    'ticket types where this is checked, will not be send to '
                    'the user. This can be useful for e.g. sponsor tickets'))

    content_type = models.ForeignKey('contenttypes.ContentType', blank=False, verbose_name=_('Ticket to generate'))

    objects = TicketTypeManager()

    class Meta:
        ordering = ('tutorial_ticket', 'product_number', 'vouchertype_needed',)
        verbose_name = _('Ticket type')
        verbose_name_plural = _('Ticket type')
        unique_together = [('product_number', 'conference')]


class PurchaseManager(models.Manager):
    use_in_migrations = True


class Purchase(models.Model):
    conference = models.ForeignKey(
        "conference.Conference", verbose_name="conference", null=True,
        on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=_('User'))

    # Address in purchase because a user maybe wants to different invoices.
    company_name = models.CharField(_('Company'), max_length=100, blank=True)
    first_name = models.CharField(_('First name'), max_length=250)
    last_name = models.CharField(_('Last name'), max_length=250)
    email = models.EmailField(_('E-mail'))

    street = models.CharField(_('Street and house number'), max_length=100)
    zip_code = models.CharField(_('Zip code'), max_length=20)
    city = models.CharField(_('City'), max_length=100)
    country = models.CharField(_('Country'), max_length=100)
    vat_id = models.CharField(_('VAT-ID'), max_length=16, blank=True)

    date_added = models.DateTimeField(_('Date (added)'), blank=False)
    state = models.CharField(
        _('Status'), max_length=25, choices=PURCHASE_STATES,
        default=PURCHASE_STATES[0][0], blank=False)

    comments = models.TextField(_('Comments'), blank=True)

    payment_method = models.CharField(_('Payment method'), max_length=20,
                                      choices=PAYMENT_METHOD_CHOICES,
                                      default='invoice')
    payment_transaction = models.CharField(_('Transaction ID'), max_length=255,
                                           blank=True)
    payment_total = models.FloatField(_('Payment total'),
                                      blank=True, null=True)

    exported = models.BooleanField(_('Exported'), default=False)

    # Invoicing fields
    invoice_number = models.IntegerField(_('Invoice number'), null=True,
                                         blank=True)
    invoice_filename = models.CharField(_('Invoice filename'), null=True,
                                        blank=True, max_length=255)

    objects = PurchaseManager()

    class Meta:
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')


class TShirtSize(models.Model):
    conference = models.ForeignKey(
        "conference.Conference", verbose_name="conference", null=True,
        on_delete=models.PROTECT)
    size = models.CharField(max_length=100, verbose_name=_('Size'))
    sort = models.IntegerField(default=999, verbose_name=_('Sort order'))

    class Meta:
        verbose_name = _('T-Shirt size')
        verbose_name_plural = _('T-Shirt sizes')
        ordering = ('sort',)


class TicketManager(models.Manager):
    use_in_migrations = True


class Ticket(models.Model):
    purchase = models.ForeignKey(Purchase)
    ticket_type = models.ForeignKey(TicketType, verbose_name=_('Ticket type'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='%(app_label)s_%(class)s_tickets')

    date_added = models.DateTimeField(_('Date (added)'), blank=False)

    canceled = models.BooleanField(_('Canceled'), default=False, blank=True)

    objects = TicketManager()

    management_fields = ()

    class Meta:
        ordering = ('ticket_type__tutorial_ticket',
                    'ticket_type__product_number')


class SupportTicket(Ticket):

    objects = TicketManager()

    class Meta:
        verbose_name = _('Support Ticket')
        verbose_name_plural = _('Support Tickets')


class VenueTicket(Ticket):
    first_name = models.CharField(_('First name'), max_length=250, blank=True)
    last_name = models.CharField(_('Last name'), max_length=250, blank=True)
    organisation = models.CharField(
        _('Organization'), max_length=100, blank=True)

    shirtsize = models.ForeignKey(TShirtSize, blank=True, null=True,
                                  verbose_name=_('Desired T-Shirt size'))
    dietary_preferences = models.ManyToManyField('DietaryPreference',
        verbose_name=_('Dietary preferences'), blank=True)

    sponsor = models.ForeignKey('sponsorship.Sponsor', null=True, blank=True,
        verbose_name=_('Sponsor'))
    voucher = models.ForeignKey(
        'Voucher', verbose_name=_('Voucher'), blank=True, null=True)

    management_fields = ('sponsor', 'voucher',)

    objects = TicketManager()

    class Meta:
        verbose_name = _('Conference Ticket')
        verbose_name_plural = _('Conference Tickets')


class DietaryPreference(models.Model):
    name = models.CharField('Name', unique=True, max_length=30)


class SIMCardTicket(Ticket):
    first_name = models.CharField(_('First name'), max_length=250, blank=False)
    last_name = models.CharField(_('Last name'), max_length=250, blank=False)

    date_of_birth = models.DateField(_('Date of birth'))
    gender = models.CharField(_('Gender'), max_length=6, choices=GENDER_CHOICES)

    hotel_name = models.CharField(
        _('Host'), max_length=100, blank=True,
        help_text=_('Name of your hotel or host for your stay.'))
    email = models.EmailField(_('E-mail'), blank=False)

    street = models.CharField(_('Street and house number of host'), max_length=100)
    zip_code = models.CharField(_('Zip code of host'), max_length=20)
    city = models.CharField(_('City of host'), max_length=100)
    country = models.CharField(_('Country of host'), max_length=100)

    phone = models.CharField(
        _('Host phone number'), max_length=100, blank=False,
        help_text=_('Please supply the phone number of your hotel or host.'))

    sim_id = models.CharField(
        _('IMSI'), max_length=20, blank=True,
        help_text=_('The IMSI of the SIM Card associated with this account.'))

    objects = TicketManager()

    class Meta:
        verbose_name = _('SIM Card')
        verbose_name_plural = _('SIM Cards')
