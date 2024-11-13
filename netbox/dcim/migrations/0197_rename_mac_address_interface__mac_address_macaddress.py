import dcim.fields
import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


def populate_macaddress_objects(apps, schema_editor):
    Interface = apps.get_model('dcim', 'Interface')
    VMInterface = apps.get_model('virtualization', 'VMInterface')
    MACAddress = apps.get_model('dcim', 'MACAddress')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    interface_ct = ContentType.objects.get_for_model(Interface)
    vminterface_ct = ContentType.objects.get_for_model(VMInterface)
    mac_addresses = []
    print()
    print('Converting MAC addresses...')
    for interface in Interface.objects.filter(_mac_address__isnull=False):
        mac_addresses.append(
            MACAddress(
                mac_address=interface._mac_address,
                assigned_object_type=interface_ct,
                assigned_object_id=interface.id,
                # interface=interface,
            )
        )
    for vminterface in VMInterface.objects.filter(_mac_address__isnull=False):
        mac_addresses.append(
            MACAddress(
                mac_address=vminterface._mac_address,
                assigned_object_type=vminterface_ct,
                assigned_object_id=vminterface.id,
                # vm_interface=vm_interface,
            )
        )
    MACAddress.objects.bulk_create(mac_addresses)
    print(f'Created {len(mac_addresses)} MAC address objects.')


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0196_qinq_svlan'),
        ('extras', '0122_charfield_null_choices'),
        ('virtualization', '0046_rename_mac_address_vminterface__mac_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interface',
            old_name='mac_address',
            new_name='_mac_address',
        ),
        migrations.CreateModel(
            name='MACAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('mac_address', dcim.fields.MACAddressField(blank=True, null=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('assigned_object_id', models.PositiveBigIntegerField(blank=True, null=True)),
                ('assigned_object_type', models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(models.Q(('app_label', 'dcim'), ('model', 'interface')), models.Q(('app_label', 'virtualization'), ('model', 'vminterface')), _connector='OR')), null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='contenttypes.contenttype')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
                'ordering': ('mac_address',)
            },
        ),
        migrations.RunPython(
            code=populate_macaddress_objects,
            reverse_code=migrations.RunPython.noop
        )
    ]
