import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from graphql import GraphQLError

from .models import Device, Location


class LocationType(DjangoObjectType):
    class Meta:
        model = Location


class DeviceType(DjangoObjectType):
    latest_location = graphene.Field(LocationType)
    locations = graphene.List(LocationType) 

    class Meta:
        model = Device

    def resolve_latest_location(self, info):
        return self.latest_location()
    
    def resolve_locations(self, info):
        return self.location_set.all()


class CreateDevice(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    device = graphene.Field(DeviceType)

    def mutate(self, info, name):
        device = Device(name=name)
        device.save()
        return CreateDevice(device=device)


class Mutation(graphene.ObjectType):
    create_device = CreateDevice.Field()


class Query(graphene.ObjectType):

    all_devices = graphene.List(DeviceType)

    device = graphene.Field(DeviceType, id=graphene.Int(required=True))
    # cihaza bağlı konumlar
    device_locations = graphene.List(LocationType, device_id=graphene.Int(required=True))


    all_locations = graphene.List(LocationType)

    location = graphene.Field(LocationType, id=graphene.Int(required=True))

    def resolve_all_devices(root, info):
        return Device.objects.all()

    def resolve_device(root, info, id):
        return Device.objects.get(pk=id)

    def resolve_all_locations(root, info):
        return Location.objects.all()

    def resolve_location(root, info, id):
        return Location.objects.get(pk=id)
    
    def resolve_device_locations(root, info, device_id):
        try:
            device = Device.objects.get(pk=device_id)
            return device.location_set.order_by('-created_on')
        except Device.DoesNotExist:
            raise GraphQLError('Device not found')


schema = graphene.Schema(query=Query, mutation=Mutation)
