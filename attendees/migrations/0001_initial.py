# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import attendees.models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0001_initial'),
        ('sponsorship', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietaryPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('company_name', models.CharField(max_length=100, verbose_name='Company', blank=True)),
                ('first_name', models.CharField(max_length=250, verbose_name='First name')),
                ('last_name', models.CharField(max_length=250, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('street', models.CharField(max_length=100, verbose_name='Street and house number')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Zip code')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('country', models.CharField(max_length=100, verbose_name='Country')),
                ('vat_id', models.CharField(max_length=16, verbose_name='VAT-ID', blank=True)),
                ('date_added', models.DateTimeField(verbose_name='Date (added)')),
                ('state', models.CharField(max_length=25, verbose_name='Status', choices=[('incomplete', 'Purchase incomplete'), ('new', 'new'), ('invoice_created', 'invoice created'), ('payment_received', 'payment received'), ('canceled', 'canceled')], default='incomplete')),
                ('comments', models.TextField(verbose_name='Comments', blank=True)),
                ('payment_method', models.CharField(max_length=20, verbose_name='Payment method', choices=[('invoice', 'Invoice'), ('creditcard', 'Credit card'), ('elv', 'ELV')], default='invoice')),
                ('payment_transaction', models.CharField(max_length=255, verbose_name='Transaction ID', blank=True)),
                ('payment_total', models.FloatField(null=True, verbose_name='Payment total', blank=True)),
                ('exported', models.BooleanField(verbose_name='Exported', default=False)),
                ('invoice_number', models.IntegerField(null=True, verbose_name='Invoice number', blank=True)),
                ('invoice_filename', models.CharField(null=True, verbose_name='Invoice filename', max_length=255, blank=True)),
                ('conference', models.ForeignKey(to='conference.Conference', on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='conference')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Purchase',
                'verbose_name_plural': 'Purchases',
            },
            managers=[
                ('objects', attendees.models.PurchaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date_added', models.DateTimeField(verbose_name='Date (added)')),
                ('canceled', models.BooleanField(verbose_name='Canceled', default=False)),
            ],
            options={
                'ordering': ('ticket_type__tutorial_ticket', 'ticket_type__product_number'),
            },
            managers=[
                ('objects', attendees.models.TicketManager()),
            ],
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('product_number', models.IntegerField(help_text='Will be created when you save the first time.', verbose_name='Product number', blank=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('fee', models.FloatField(verbose_name='Fee', default=0)),
                ('max_purchases', models.PositiveIntegerField(help_text='0 means no limit', verbose_name='Max. purchases', default=0)),
                ('is_active', models.BooleanField(verbose_name='Is active', default=False)),
                ('is_on_desk_active', models.BooleanField(verbose_name='Allow on desk purchase', default=False)),
                ('date_valid_from', models.DateTimeField(verbose_name='Sale start')),
                ('date_valid_to', models.DateTimeField(verbose_name='Sale end')),
                ('valid_on', models.DateField(null=True, verbose_name='Valid on', blank=True)),
                ('tutorial_ticket', models.BooleanField(verbose_name='Tutorial ticket', default=False)),
                ('remarks', models.TextField(verbose_name='Remarks', blank=True)),
                ('allow_editing', models.NullBooleanField(verbose_name='Allow editing')),
                ('editable_fields', models.TextField(verbose_name='Editable fields', blank=True)),
                ('editable_until', models.DateTimeField(null=True, verbose_name='Editable until', blank=True)),
                ('prevent_invoice', models.BooleanField(help_text='If checked, a purchase, that contains only tickets of ticket types where this is checked, will not be send to the user. This can be useful for e.g. sponsor tickets', verbose_name='Conditionally prevent invoice to user', default=False)),
                ('conference', models.ForeignKey(to='conference.Conference', on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='conference')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', verbose_name='Ticket to generate')),
            ],
            options={
                'ordering': ('tutorial_ticket', 'product_number', 'vouchertype_needed'),
                'verbose_name': 'Ticket type',
                'verbose_name_plural': 'Ticket type',
            },
            managers=[
                ('objects', attendees.models.TicketTypeManager()),
            ],
        ),
        migrations.CreateModel(
            name='TShirtSize',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('size', models.CharField(max_length=100, verbose_name='Size')),
                ('sort', models.IntegerField(verbose_name='Sort order', default=999)),
                ('conference', models.ForeignKey(to='conference.Conference', on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='conference')),
            ],
            options={
                'ordering': ('sort',),
                'verbose_name': 'T-Shirt size',
                'verbose_name_plural': 'T-Shirt sizes',
            },
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.CharField(help_text='Can be left blank, code will be created when you save.', verbose_name='Code', max_length=12, blank=True)),
                ('remarks', models.CharField(max_length=254, verbose_name='Remarks', blank=True)),
                ('date_valid', models.DateTimeField(help_text='The voucher is valid until this date', verbose_name='Date (valid)')),
                ('is_used', models.BooleanField(verbose_name='Is used', default=False)),
            ],
            options={
                'verbose_name': 'Voucher',
                'verbose_name_plural': 'Vouchers',
            },
            managers=[
                ('objects', attendees.models.VoucherManager()),
            ],
        ),
        migrations.CreateModel(
            name='VoucherType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='voucher type')),
                ('conference', models.ForeignKey(to='conference.Conference', on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='conference')),
            ],
            options={
                'verbose_name': 'voucher type',
                'verbose_name_plural': 'voucher types',
            },
            managers=[
                ('objects', attendees.models.VoucherTypeManager()),
            ],
        ),
        migrations.CreateModel(
            name='SIMCardTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(to='attendees.Ticket', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=250, verbose_name='First name')),
                ('last_name', models.CharField(max_length=250, verbose_name='Last name')),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('gender', models.CharField(max_length=6, verbose_name='Gender', choices=[('female', 'female'), ('male', 'male')])),
                ('hotel_name', models.CharField(help_text='Name of your hotel or host for your stay.', verbose_name='Host', max_length=100, blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('street', models.CharField(max_length=100, verbose_name='Street and house number of host')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Zip code of host')),
                ('city', models.CharField(max_length=100, verbose_name='City of host')),
                ('country', models.CharField(max_length=100, verbose_name='Country of host')),
                ('phone', models.CharField(help_text='Please supply the phone number of your hotel or host.', verbose_name='Host phone number', max_length=100)),
                ('sim_id', models.CharField(help_text='The IMSI of the SIM Card associated with this account.', verbose_name='IMSI', max_length=20, blank=True)),
            ],
            options={
                'verbose_name': 'SIM Card',
                'verbose_name_plural': 'SIM Cards',
            },
            bases=('attendees.ticket',),
            managers=[
                ('objects', attendees.models.TicketManager()),
            ],
        ),
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(to='attendees.Ticket', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Support Ticket',
                'verbose_name_plural': 'Support Tickets',
            },
            bases=('attendees.ticket',),
            managers=[
                ('objects', attendees.models.TicketManager()),
            ],
        ),
        migrations.CreateModel(
            name='VenueTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(to='attendees.Ticket', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=250, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=250, verbose_name='Last name', blank=True)),
                ('organisation', models.CharField(max_length=100, verbose_name='Organization', blank=True)),
                ('dietary_preferences', models.ManyToManyField(to='attendees.DietaryPreference', verbose_name='Dietary preferences', blank=True)),
                ('shirtsize', models.ForeignKey(to='attendees.TShirtSize', verbose_name='Desired T-Shirt size', null=True, blank=True)),
                ('sponsor', models.ForeignKey(to='sponsorship.Sponsor', verbose_name='Sponsor', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Conference Ticket',
                'verbose_name_plural': 'Conference Tickets',
            },
            bases=('attendees.ticket',),
            managers=[
                ('objects', attendees.models.TicketManager()),
            ],
        ),
        migrations.AddField(
            model_name='voucher',
            name='type',
            field=models.ForeignKey(to='attendees.VoucherType', null=True, verbose_name='voucher type'),
        ),
        migrations.AddField(
            model_name='tickettype',
            name='vouchertype_needed',
            field=models.ForeignKey(to='attendees.VoucherType', verbose_name='voucher type needed', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='purchase',
            field=models.ForeignKey(to='attendees.Purchase'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(to='attendees.TicketType', verbose_name='Ticket type'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, related_name='attendees_ticket_tickets'),
        ),
        migrations.AddField(
            model_name='venueticket',
            name='voucher',
            field=models.ForeignKey(to='attendees.Voucher', verbose_name='Voucher', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='tickettype',
            unique_together=set([('product_number', 'conference')]),
        ),
    ]
