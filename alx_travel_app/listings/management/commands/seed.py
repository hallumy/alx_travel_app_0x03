from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        host, created = User.objects.get_or_create(username='hostuser')
        if created:
            host.set_password('password')
            host.save()
            self.stdout.write(self.style.SUCCESS('Created host user'))

        for index in range(5):
            listing, created = Listing.objects.get_or_create(
                name=f"Sample Listing {index+1}",
                defaults={
                    'description': f"This is a sample listing #{index+1}",
                    'location': random.choice(['New York', 'San Francisco', 'Los Angeles', 'Chicago']),
                    'price_per_night': round(random.uniform(50, 300), 2),
                    'host': host,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {listing.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {listing.name}"))
