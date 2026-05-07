from rest_framework import serializers
from .models import Car, CarImage, Seller, Appointment, Favorite


class SellerSerializer(serializers.ModelSerializer):
    plan = serializers.ReadOnlyField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'seller_type', 'avatar', 'rating',
                  'review_count', 'location', 'phone', 'is_verified',
                  'is_premium', 'premium_until', 'premium_requested', 'plan']


class CarImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = CarImage
        fields = ['id', 'url', 'order', 'is_primary']

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class CarSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(), source='seller', write_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    car_images = CarImageSerializer(many=True, read_only=True)
    primary_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'seller', 'seller_id', 'make', 'model', 'year', 'price',
                  'mileage', 'fuel', 'transmission', 'power', 'color', 'doors',
                  'seats', 'location', 'description', 'features', 'tags', 'badge',
                  'gradient', 'accent_color', 'image', 'image_hero', 'is_available',
                  'is_favorited', 'car_images', 'primary_image_url', 'created_at']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, car=obj).exists()
        return False

    def get_primary_image_url(self, obj):
        request = self.context.get('request')
        primary = obj.car_images.filter(is_primary=True).first()
        if not primary:
            primary = obj.car_images.first()
        if primary and request:
            return request.build_absolute_uri(primary.image.url)
        if primary:
            return primary.image.url
        return obj.image or obj.image_hero or None


class AppointmentSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), source='car', write_only=True
    )
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'car', 'car_id', 'buyer_name', 'seller_name',
                  'date', 'time', 'status', 'note', 'cancellation_reason', 'created_at']
        read_only_fields = ['buyer_name', 'seller_name']

    def get_buyer_name(self, obj):
        return obj.buyer.get_full_name() or obj.buyer.email

    def get_seller_name(self, obj):
        return obj.seller.name

    def create(self, validated_data):
        request = self.context['request']
        validated_data['buyer'] = request.user
        car = validated_data['car']
        validated_data['seller'] = car.seller
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'car', 'created_at']
