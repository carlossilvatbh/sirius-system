#!/usr/bin/env python
"""
Test script to create sample data for dashboard testing
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/home/ubuntu/sirius-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirius_project.settings')
django.setup()

from django.contrib.auth.models import User
from sales.models import StructureRequest, StructureApproval, Partner
from corporate.models import Structure, Entity, EntityOwnership
from parties.models import Party
from django.utils import timezone
from datetime import timedelta

def create_test_data():
    """Create test data for dashboard"""
    print("Creating test data for dashboard...")
    
    # Create test user if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@sirius.com', 'admin123')
        print("✅ Created admin user")
    
    # Create test parties (UBOs)
    party1, created = Party.objects.get_or_create(
        name='John Smith',
        defaults={
            'person_type': 'NATURAL_PERSON',
            'nationality': 'US',
            'birth_date': '1980-01-01'
        }
    )
    if created:
        print("✅ Created Party: John Smith")
    
    party2, created = Party.objects.get_or_create(
        name='Maria Silva',
        defaults={
            'person_type': 'NATURAL_PERSON',
            'nationality': 'BR',
            'birth_date': '1985-05-15'
        }
    )
    if created:
        print("✅ Created Party: Maria Silva")
    
    party3, created = Party.objects.get_or_create(
        name='Bob Johnson',
        defaults={
            'person_type': 'NATURAL_PERSON',
            'nationality': 'US',
            'birth_date': '1975-12-10'
        }
    )
    if created:
        print("✅ Created Party: Bob Johnson")
    
    # Create test partners
    partner1, created = Partner.objects.get_or_create(
        party=party1,
        defaults={
            'company_name': 'Smith Holdings LLC',
            'address': '123 Wall Street, New York, NY'
        }
    )
    if created:
        print("✅ Created Partner: Smith Holdings LLC")
    
    # Create test entities
    entity1, created = Entity.objects.get_or_create(
        name='Delaware Holding Corp',
        defaults={
            'entity_type': 'Corporation',
            'jurisdiction': 'US',
            'us_state': 'Delaware',
            'total_shares': 1000,
            'tax_classification': 'C-Corp'
        }
    )
    if created:
        print("✅ Created Entity: Delaware Holding Corp")
    
    entity2, created = Entity.objects.get_or_create(
        name='Brazil Subsidiary Ltda',
        defaults={
            'entity_type': 'Limited Liability Company',
            'jurisdiction': 'BR',
            'br_state': 'São Paulo',
            'total_shares': 10000,
            'tax_classification': 'Ltda'
        }
    )
    if created:
        print("✅ Created Entity: Brazil Subsidiary Ltda")
    
    entity3, created = Entity.objects.get_or_create(
        name='Cayman Investment Fund',
        defaults={
            'entity_type': 'Investment Fund',
            'jurisdiction': 'KY',
            'total_shares': 5000,
            'tax_classification': 'Exempt Company'
        }
    )
    if created:
        print("✅ Created Entity: Cayman Investment Fund")
    
    # Create test structure requests
    request1, created = StructureRequest.objects.get_or_create(
        description='International holding structure with Delaware parent controlling Brazilian and Cayman subsidiaries',
        defaults={
            'point_of_contact_party': party1,
            'status': 'SUBMITTED',
            'submitted_at': timezone.now() - timedelta(days=2)
        }
    )
    if created:
        request1.requesting_parties.add(party1, party2)
        print("✅ Created StructureRequest: International holding structure")
    
    request2, created = StructureRequest.objects.get_or_create(
        description='Trust foundation setup for asset protection and tax optimization',
        defaults={
            'point_of_contact_party': party2,
            'status': 'IN_REVIEW',
            'submitted_at': timezone.now() - timedelta(days=5)
        }
    )
    if created:
        request2.requesting_parties.add(party2)
        print("✅ Created StructureRequest: Trust foundation setup")
    
    request3, created = StructureRequest.objects.get_or_create(
        description='Investment fund structure for private equity operations',
        defaults={
            'point_of_contact_party': party3,
            'status': 'IN_PROGRESS',
            'submitted_at': timezone.now() - timedelta(days=10)
        }
    )
    if created:
        request3.requesting_parties.add(party3)
        print("✅ Created StructureRequest: Investment fund structure")
    
    # Create test structures
    structure1, created = Structure.objects.get_or_create(
        name='International Holding Structure',
        defaults={
            'description': 'Multi-jurisdictional holding structure with Delaware parent',
            'status': 'DRAFTING'
        }
    )
    if created:
        print("✅ Created Structure: International Holding Structure")
    
    structure2, created = Structure.objects.get_or_create(
        name='Private Equity Fund Structure',
        defaults={
            'description': 'Cayman-based investment fund for PE operations',
            'status': 'SENT_FOR_APPROVAL'
        }
    )
    if created:
        print("✅ Created Structure: Private Equity Fund Structure")
    
    # Create test entity ownerships
    ownership1, created = EntityOwnership.objects.get_or_create(
        structure=structure1,
        owned_entity=entity1,
        owner_ubo=party1,
        defaults={
            'corporate_name': 'John Smith Holdings',
            'hash_number': 'JSH001',
            'owned_shares': 600,
            'ownership_percentage': 60.0,
            'share_value_usd': 100.0
        }
    )
    if created:
        print("✅ Created EntityOwnership: John Smith → Delaware Holding Corp (60%)")
    
    ownership2, created = EntityOwnership.objects.get_or_create(
        structure=structure1,
        owned_entity=entity1,
        owner_ubo=party2,
        defaults={
            'corporate_name': 'Maria Silva Holdings',
            'hash_number': 'MSH001',
            'owned_shares': 400,
            'ownership_percentage': 40.0,
            'share_value_usd': 100.0
        }
    )
    if created:
        print("✅ Created EntityOwnership: Maria Silva → Delaware Holding Corp (40%)")
    
    ownership3, created = EntityOwnership.objects.get_or_create(
        structure=structure1,
        owned_entity=entity2,
        owner_entity=entity1,
        defaults={
            'corporate_name': 'Delaware Holdings Brazil',
            'hash_number': 'DHB001',
            'owned_shares': 10000,
            'ownership_percentage': 100.0,
            'share_value_usd': 50.0
        }
    )
    if created:
        print("✅ Created EntityOwnership: Delaware Holding Corp → Brazil Subsidiary (100%)")
    
    # Create completed request for metrics
    completed_request, created = StructureRequest.objects.get_or_create(
        description='Completed structure for testing metrics',
        defaults={
            'point_of_contact_party': party1,
            'status': 'COMPLETED',
            'submitted_at': timezone.now() - timedelta(days=15),
            'updated_at': timezone.now() - timedelta(days=1)
        }
    )
    if created:
        completed_request.requesting_parties.add(party1)
        print("✅ Created completed StructureRequest for metrics")
    
    print("\n🎉 Test data creation completed!")
    print("\nDashboard should now show:")
    print(f"- {StructureRequest.objects.filter(status='SUBMITTED').count()} pending requests")
    print(f"- {StructureRequest.objects.filter(status='IN_PROGRESS').count()} in progress")
    print(f"- {Structure.objects.filter(status='SENT_FOR_APPROVAL').count()} pending approvals")
    print(f"- {StructureRequest.objects.filter(status='COMPLETED').count()} completed requests")
    print(f"- {Structure.objects.count()} total structures")
    print(f"- {Entity.objects.count()} total entities")

if __name__ == '__main__':
    create_test_data()

