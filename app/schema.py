import graphene
from graphene_django.types import DjangoObjectType
from .models import Device, Location


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device


class LocationType(DjangoObjectType):
    class Meta:
        model = Location


class DeviceWithLocationsType(graphene.ObjectType):
    device = graphene.Field(DeviceType)
    locations = graphene.List(LocationType)


class DeviceWithLastLocationType(graphene.ObjectType):
    device = graphene.Field(DeviceType)
    last_location = graphene.Field(LocationType)


class Query(graphene.ObjectType):
    device = graphene.Field(DeviceType, id=graphene.Int(required=True))
    all_devices = graphene.List(DeviceType)
    get_device_locations = graphene.Field(
        DeviceWithLocationsType,
        id=graphene.ID(required=True)
    )

    all_devices_with_last_location = graphene.List(DeviceWithLastLocationType)

    def resolve_device(self, info, id):
        return Device.objects.get(pk=id)

    def resolve_all_devices(self, info):
        return Device.objects.filter(is_active=True)

    def resolve_get_device_locations(self, info, id):
        try:
            device = Device.objects.get(pk=id)
            return DeviceWithLocationsType(
                device=device,
                locations=device.location_set.filter(
                    is_active=True).order_by('-created_on')
            )
        except Device.DoesNotExist:
            return DeviceWithLocationsType(
                device=None,
                locations=[]
            )

    def resolve_all_devices_with_last_location(self, info):
        devices = Device.objects.all()
        result = []
        for device in devices:
            last_location = device.latest_location()
            result.append({
                'device': device,
                'last_location': last_location
            })
        return result


class CreateDevice(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    device = graphene.Field(DeviceType)

    def mutate(self, info, name):
        device = Device(name=name)
        device.save()
        return CreateDevice(device=device)


class UpdateDevice(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    device = graphene.Field(DeviceType)

    def mutate(self, info, id, name):
        device = Device.objects.get(pk=id)
        device.name = name
        device.save()
        return UpdateDevice(device=device)


class DeleteDevice(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        device = Device.objects.get(pk=id)
        device.soft_delete()
        return DeleteDevice(success=True)


class Mutation(graphene.ObjectType):
    create_device = CreateDevice.Field()
    update_device = UpdateDevice.Field()
    delete_device = DeleteDevice.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
