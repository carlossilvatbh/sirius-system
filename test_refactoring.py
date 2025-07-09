#!/usr/bin/env python
"""
Test script to validate SIRIUS system refactoring
Run this script to verify that all models and relationships work correctly
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirius_project.settings')
django.setup()

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Import all models
from corporate.models import Entity, Structure, EntityOwnership, MasterEntity, ValidationRule
from parties.models import Party, PartyRole, Passport, BeneficiaryRelation, DocumentAttachment
from sales.models import Partner, Contact, StructureRequest, StructureApproval
from corporate_relationship.models import File, Service, ServiceActivity
from financial_department.models import EntityPrice, IncorporationCost, ServicePrice, ServiceCost


def test_entity_model():
    """Test Entity model creation and validation"""
    print("Testing Entity model...")
    
    # Create a basic entity
    entity = Entity.objects.create(
        name="Test Corporation",
        entity_type="CORP",
        jurisdiction="US",
        us_state="DE"
    )
    
    assert entity.name == "Test Corporation"
    assert entity.get_entity_type_display() == "Corp"
    assert entity.get_full_jurisdiction_display() == "Delaware, United States"
    
    print("✓ Entity model test passed")


def test_party_model():
    """Test Party model creation and validation"""
    print("Testing Party model...")
    
    # Create a natural person
    party = Party.objects.create(
        name="John Doe",
        person_type="NATURAL_PERSON",
        email="john@example.com",
        nationality="US"
    )
    
    assert party.name == "John Doe"
    assert party.get_person_type_display() == "Natural Person"
    
    # Test party roles
    role = PartyRole.objects.create(
        party=party,
        role_type="ULTIMATE_BENEFICIAL_OWNER",
        context="Test Entity"
    )
    
    assert role.get_role_type_display() == "Ultimate Beneficial Owner"
    
    print("✓ Party model test passed")


def test_structure_model():
    """Test Structure model for corporate hierarchies"""
    print("Testing Structure model...")
    
    structure = Structure.objects.create(
        name="Test Corporate Structure",
        description="A test corporate structure",
        status="DRAFTING"
    )
    
    assert structure.name == "Test Corporate Structure"
    assert structure.get_status_display() == "Drafting"
    
    print("✓ Structure model test passed")


def test_entity_ownership():
    """Test EntityOwnership relationships"""
    print("Testing EntityOwnership model...")
    
    # Create entities
    parent_entity = Entity.objects.create(
        name="Parent Corp",
        entity_type="CORP",
        jurisdiction="US"
    )
    
    child_entity = Entity.objects.create(
        name="Child Corp",
        entity_type="CORP",
        jurisdiction="US"
    )
    
    # Create structure
    structure = Structure.objects.create(
        name="Ownership Structure",
        description="Test ownership structure"
    )
    
    # Create party
    party = Party.objects.create(
        name="Owner Person",
        person_type="NATURAL_PERSON"
    )
    
    # Test UBO ownership
    ownership = EntityOwnership.objects.create(
        structure=structure,
        owner_ubo=party,
        owned_entity=child_entity,
        total_shares=100,
        owned_shares=75,
        ownership_percentage=75.0
    )
    
    assert ownership.ownership_percentage == 75.0
    
    print("✓ EntityOwnership model test passed")


def test_partner_model():
    """Test Partner model (formerly Client)"""
    print("Testing Partner model...")
    
    # Create party first
    party = Party.objects.create(
        name="Business Partner",
        person_type="JURIDICAL_PERSON",
        is_partner=True
    )
    
    # Create partner
    partner = Partner.objects.create(
        party=party,
        company_name="Partner Company Inc.",
        address="123 Business St, City, State"
    )
    
    assert partner.company_name == "Partner Company Inc."
    assert partner.party.is_partner == True
    
    # Test contact
    contact = Contact.objects.create(
        partner=partner,
        name="Contact Person",
        role="Manager",
        email="contact@partner.com"
    )
    
    assert contact.partner == partner
    
    print("✓ Partner model test passed")


def test_financial_models():
    """Test Financial Department models"""
    print("Testing Financial Department models...")
    
    # Create entity
    entity = Entity.objects.create(
        name="Financial Test Entity",
        entity_type="CORP",
        jurisdiction="US"
    )
    
    # Create entity price
    entity_price = EntityPrice.objects.create(
        entity=entity,
        base_currency="USD",
        markup_type="PERCENTAGE",
        markup_value=15.0
    )
    
    # Create incorporation cost
    cost = IncorporationCost.objects.create(
        entity_price=entity_price,
        name="Legal Fees",
        cost_type="LEGAL_FEE",
        value=1000.00
    )
    
    assert entity_price.get_base_currency_display() == "US Dollar"
    assert cost.value == 1000.00
    
    print("✓ Financial Department models test passed")


def test_validation_rules():
    """Test ValidationRule model"""
    print("Testing ValidationRule model...")
    
    # Create entities
    entity1 = Entity.objects.create(
        name="Entity 1",
        entity_type="TRUST",
        jurisdiction="US"
    )
    
    entity2 = Entity.objects.create(
        name="Entity 2",
        entity_type="CORP",
        jurisdiction="US"
    )
    
    # Create validation rule
    rule = ValidationRule.objects.create(
        parent_entity=entity1,
        related_entity=entity2,
        relationship_type="RECOMMENDED",
        severity="INFO",
        description="Trust and Corp combination is recommended",
        tax_impacts="Favorable tax treatment in certain jurisdictions"
    )
    
    assert rule.get_relationship_type_display() == "Recommended Combination"
    assert rule.tax_impacts != ""
    
    print("✓ ValidationRule model test passed")


def test_passport_model():
    """Test Passport model with expiration tracking"""
    print("Testing Passport model...")
    
    from datetime import date, timedelta
    
    # Create party
    party = Party.objects.create(
        name="Passport Holder",
        person_type="NATURAL_PERSON"
    )
    
    # Create passport
    passport = Passport.objects.create(
        party=party,
        number="P123456789",
        issued_at=date.today() - timedelta(days=365),
        expires_at=date.today() + timedelta(days=30),  # Expires in 30 days
        issuing_country="US"
    )
    
    assert passport.is_expiring_soon() == True
    assert passport.is_expiring_soon(days=20) == False
    
    print("✓ Passport model test passed")


def run_all_tests():
    """Run all tests"""
    print("Starting SIRIUS System Refactoring Tests...")
    print("=" * 50)
    
    try:
        test_entity_model()
        test_party_model()
        test_structure_model()
        test_entity_ownership()
        test_partner_model()
        test_financial_models()
        test_validation_rules()
        test_passport_model()
        
        print("=" * 50)
        print("✅ All tests passed successfully!")
        print("The refactoring appears to be working correctly.")
        
    except Exception as e:
        print("=" * 50)
        print(f"❌ Test failed with error: {e}")
        print("Please check the model implementations.")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()

