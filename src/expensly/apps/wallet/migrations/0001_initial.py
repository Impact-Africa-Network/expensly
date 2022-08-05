# Generated by Django 4.0 on 2022-08-05 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ian_account', '0004_basemodel_remove_organization_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTransaction',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ian_account.user')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ian_account.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('basetransaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wallet.basetransaction')),
                ('transaction_type', models.CharField(choices=[('DE', 'Deposit'), ('WI', 'Withdraw')], default='DE', max_length=20)),
                ('transaction_status', models.CharField(choices=[('pending', 'pending'), ('successful', 'successful'), ('canceled', 'canceled'), ('failed', 'failed')], default='pending', max_length=20)),
                ('metadata', models.JSONField(default=dict)),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recepient', to='ian_account.user')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
            bases=('wallet.basetransaction',),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('request_type', models.CharField(choices=[('pre_payment', 'pre_payment'), ('reimbursement', 'reimbursement')], default=[('pre_payment', 'pre_payment'), ('reimbursement', 'reimbursement')], max_length=20)),
                ('request_status', models.CharField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('approved', 'approved'), ('paid_successful', 'paid_successful')], default='pre_payment', max_length=20)),
                ('purpose', models.CharField(max_length=200)),
                ('file', models.FileField(null=True, upload_to='receipts')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ian_account.user')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ian_account.organization')),
                ('transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_transaction', to='wallet.transaction')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
    ]
