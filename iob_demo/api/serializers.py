from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rest_framework import serializers
from iob_demo.models import ItemsTakeIn, ItemsTakeOut, IOB


class StandardSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(StandardSerializer, self).get_field_names(
            declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class ItemsTakeInSerializer(StandardSerializer):
    keep_posting = serializers.BooleanField(default=False)

    class Meta:
        model = ItemsTakeIn
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop('keep_posting')
        obj = ItemsTakeIn.objects.create(**validated_data)
        return obj

    def validate_unit(self, value):
        try:
            iob = IOB.objects.get(client=self.context['request'].user,
                                  date=self.initial_data['date'], code=self.initial_data['code'])
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            return value
        if value != str.lower(iob.unit) and not self.initial_data['keep_posting']:
            raise serializers.ValidationError(
                "The unit field you provided is difference from previous, do you want to continue ?")
        return value


class ItemsTakeOutSerializer(StandardSerializer):
    class Meta:
        model = ItemsTakeOut
        fields = '__all__'


class IOBSerializer(StandardSerializer):
    take_ins = ItemsTakeInSerializer(many=True, read_only=True)
    take_outs = ItemsTakeOutSerializer(many=True, read_only=True)

    class Meta:
        model = IOB
        depth = 0
        fields = '__all__'
        extra_fields = ['begin',
                        'get_take_in',
                        'get_take_out',
                        'end', ]


class IOBDisplay(serializers.Serializer):
    code = serializers.CharField()
    take_in = serializers.IntegerField()
    take_out = serializers.IntegerField()
    price = serializers.IntegerField()
    unit = serializers.CharField()
