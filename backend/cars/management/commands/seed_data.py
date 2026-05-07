from django.core.management.base import BaseCommand
from cars.models import Car, Seller
from users.models import User


SELLERS_DATA = [
    {'id': 1, 'name': 'Premium Motors Paris', 'seller_type': 'pro', 'avatar': 'PM', 'rating': 4.9, 'review_count': 142, 'location': 'Paris, 75016', 'phone': '+33 1 42 00 00 01', 'is_verified': True},
    {'id': 2, 'name': 'Élite Auto Lyon', 'seller_type': 'pro', 'avatar': 'EA', 'rating': 4.7, 'review_count': 89, 'location': 'Lyon, 69006', 'phone': '+33 4 72 00 00 02', 'is_verified': True},
    {'id': 3, 'name': 'Jean-Marc Dubois', 'seller_type': 'particulier', 'avatar': 'JD', 'rating': 4.5, 'review_count': 12, 'location': 'Bordeaux, 33000', 'phone': '+33 5 56 00 00 03', 'is_verified': False},
    {'id': 4, 'name': 'AutoLux Marseille', 'seller_type': 'pro', 'avatar': 'AL', 'rating': 4.8, 'review_count': 67, 'location': 'Marseille, 13008', 'phone': '+33 4 91 00 00 04', 'is_verified': True},
]

CARS_DATA = [
    {
        'seller_id': 1, 'make': 'BMW', 'model': 'Série 5', 'year': 2023, 'price': 58900,
        'mileage': 12000, 'fuel': 'Essence', 'transmission': 'Automatique',
        'power': '286 ch', 'color': 'Noir Saphir', 'doors': 4, 'seats': 5,
        'location': 'Paris, 75016',
        'tags': ['Garantie constructeur', 'Carnet entretien', '1er propriétaire'],
        'description': 'Superbe BMW Série 5 en parfait état. Véhicule de direction, entretenu exclusivement en concession BMW. Équipée du pack M Sport, toit ouvrant panoramique, sièges chauffants et ventilés, navigation Professional, affichage tête haute.',
        'features': ['Pack M Sport', 'Toit panoramique', 'Sièges chauffants', 'Navigation Pro', 'Head-up display', 'Parking assistant'],
        'gradient': 'linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0f1520 100%)',
        'accent_color': '#3b6fd4', 'badge': 'Premium',
        'image': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&w=800&q=80',
        'image_hero': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&w=1200&q=85',
    },
    {
        'seller_id': 2, 'make': 'Mercedes', 'model': 'Classe C AMG', 'year': 2022, 'price': 64500,
        'mileage': 18000, 'fuel': 'Hybride', 'transmission': 'Automatique',
        'power': '313 ch', 'color': 'Blanc Polaire', 'doors': 4, 'seats': 5,
        'location': 'Lyon, 69006',
        'tags': ['Hybride rechargeable', 'Garantie 2 ans', 'TVA récupérable'],
        'description': "Mercedes Classe C 300e AMG Line. Hybride rechargeable d'une puissance de 313ch.",
        'features': ['Hybride rechargeable', 'AMG Line', 'Caméra 360°', 'Burmester audio', 'Jantes 19"', 'Pack Nuit'],
        'gradient': 'linear-gradient(135deg, #1a1214 0%, #2e1a20 50%, #1a1214 100%)',
        'accent_color': '#c9a96e', 'badge': 'Coup de cœur',
        'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&w=800&q=80',
        'image_hero': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&w=1200&q=85',
    },
    {
        'seller_id': 3, 'make': 'Porsche', 'model': 'Cayenne', 'year': 2021, 'price': 82000,
        'mileage': 35000, 'fuel': 'Essence', 'transmission': 'Automatique',
        'power': '340 ch', 'color': 'Gris Craie', 'doors': 5, 'seats': 5,
        'location': 'Bordeaux, 33000',
        'tags': ['Sport Chrono', 'PDCC', 'Historique complet'],
        'description': 'Porsche Cayenne S en excellent état.',
        'features': ['Sport Chrono', 'PDCC', 'Suspension pneumatique', 'Cuir noir', 'Toit panoramique', 'BOSE audio'],
        'gradient': 'linear-gradient(135deg, #141a10 0%, #1e2a14 50%, #101a0e 100%)',
        'accent_color': '#7cb87a', 'badge': 'Luxe',
        'image': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&w=800&q=80',
        'image_hero': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&w=1200&q=85',
    },
    {
        'seller_id': 4, 'make': 'Audi', 'model': 'A6 Avant', 'year': 2023, 'price': 52400,
        'mileage': 8000, 'fuel': 'Diesel', 'transmission': 'Automatique',
        'power': '204 ch', 'color': 'Gris Manhattan', 'doors': 5, 'seats': 5,
        'location': 'Marseille, 13008',
        'tags': ['Quasi neuf', 'Full options', '1er main'],
        'description': 'Audi A6 Avant quattro quasi neuve.',
        'features': ['S-Line Competition', 'Matrix LED', 'Virtual Cockpit', 'B&O Premium', 'Quattro', 'Toit panoramique'],
        'gradient': 'linear-gradient(135deg, #1a1508 0%, #2e2510 50%, #1a1508 100%)',
        'accent_color': '#d4a843', 'badge': 'Quasi neuf',
        'image': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&w=800&q=80',
        'image_hero': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&w=1200&q=85',
    },
    {
        'seller_id': 1, 'make': 'Tesla', 'model': 'Model 3', 'year': 2023, 'price': 47900,
        'mileage': 5000, 'fuel': 'Électrique', 'transmission': 'Automatique',
        'power': '358 ch', 'color': 'Rouge Multi-Coat', 'doors': 4, 'seats': 5,
        'location': 'Paris, 75008',
        'tags': ['Long Range', 'Autopilot', 'Supercharger'],
        'description': 'Tesla Model 3 Long Range AWD.',
        'features': ['Long Range 602km', 'Autopilot avancé', 'FSD inclus', 'Intérieur blanc', 'Jantes 19" Photon', 'Vitres teintées'],
        'gradient': 'linear-gradient(135deg, #1a0a0a 0%, #2e1010 50%, #1a0808 100%)',
        'accent_color': '#e05c5c', 'badge': 'Électrique',
        'image': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&w=800&q=80',
        'image_hero': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&w=1200&q=85',
    },
    {
        'seller_id': 2, 'make': 'Range Rover', 'model': 'Sport', 'year': 2022, 'price': 94000,
        'mileage': 22000, 'fuel': 'Diesel', 'transmission': 'Automatique',
        'power': '350 ch', 'color': 'Bleu Portofino', 'doors': 5, 'seats': 5,
        'location': 'Lyon, 69003',
        'tags': ['HSE Dynamic', 'Meridian Audio', 'Full cuir'],
        'description': 'Range Rover Sport HSE Dynamic.',
        'features': ['HSE Dynamic', 'Meridian Surround', 'Terrain Response 2', 'Toit panoramique', 'Cuir Windsor', 'Air suspension'],
        'gradient': 'linear-gradient(135deg, #080f1a 0%, #10182e 50%, #080f1a 100%)',
        'accent_color': '#4a8fd4', 'badge': 'Prestige',
        'image': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&w=800&q=80',
        'image_hero': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&w=1200&q=85',
    },
]


class Command(BaseCommand):
    help = 'Seed initial data for AutoConnect'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding sellers...')
        seller_map = {}
        for data in SELLERS_DATA:
            original_id = data.pop('id')
            seller, created = Seller.objects.get_or_create(name=data['name'], defaults=data)
            if not created:
                for k, v in data.items():
                    setattr(seller, k, v)
                seller.save()
            seller_map[original_id] = seller
            self.stdout.write(f'  {"Created" if created else "Updated"}: {seller.name}')

        self.stdout.write('Seeding cars...')
        for data in CARS_DATA:
            seller_id = data.pop('seller_id')
            data['seller'] = seller_map[seller_id]
            car_name = f"{data['make']} {data['model']} {data['year']}"
            car, created = Car.objects.get_or_create(
                make=data['make'], model=data['model'], year=data['year'],
                seller=data['seller'], defaults=data
            )
            self.stdout.write(f'  {"Created" if created else "Exists"}: {car_name}')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
