# Generated by Django 4.2.13 on 2024-05-18 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dcls_month', models.DateField()),
                ('fin_co_no', models.CharField(max_length=100)),
                ('kor_co_nm', models.CharField(max_length=100)),
                ('fin_prdt_cd', models.CharField(max_length=100)),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('join_way', models.CharField(max_length=100)),
                ('mtrt_int', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('spcl_cnd', models.TextField(blank=True, null=True)),
                ('join_deny', models.IntegerField(blank=True, null=True)),
                ('join_member', models.TextField(blank=True, null=True)),
                ('etc_note', models.TextField(blank=True, null=True)),
                ('max_limit', models.IntegerField(blank=True, null=True)),
                ('dcls_strt_day', models.CharField(max_length=100)),
                ('dcls_end_day', models.CharField(max_length=100)),
                ('fin_co_subm_day', models.CharField(max_length=100)),
                ('intr_rate_type', models.CharField(max_length=1)),
                ('intr_rate_type_nm', models.CharField(max_length=2)),
                ('sava_trm', models.CharField(max_length=3)),
                ('intr_rate', models.FloatField(null=True)),
                ('intr_rate2', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Saving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dcls_month', models.DateField()),
                ('fin_co_no', models.CharField(max_length=100)),
                ('kor_co_nm', models.CharField(max_length=100)),
                ('fin_prdt_cd', models.CharField(max_length=100)),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('join_way', models.CharField(max_length=100)),
                ('mtrt_int', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('spcl_cnd', models.TextField(blank=True, null=True)),
                ('join_deny', models.IntegerField(blank=True, null=True)),
                ('join_member', models.TextField(blank=True, null=True)),
                ('etc_note', models.TextField(blank=True, null=True)),
                ('max_limit', models.IntegerField(blank=True, null=True)),
                ('dcls_strt_day', models.CharField(max_length=100)),
                ('dcls_end_day', models.CharField(max_length=100)),
                ('fin_co_subm_day', models.CharField(max_length=100)),
                ('intr_rate_type', models.CharField(max_length=1)),
                ('intr_rate_type_nm', models.CharField(max_length=2)),
                ('rsrv_type', models.CharField(max_length=5)),
                ('sava_trm', models.CharField(max_length=3)),
                ('intr_rate', models.FloatField(null=True)),
                ('intr_rate2', models.FloatField(null=True)),
            ],
        ),
    ]
