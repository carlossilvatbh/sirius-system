#!/usr/bin/env python
"""
Test suite for SIRIUS MELHORIAS P2 - 100% Conformidade
Validates all implemented fixes and ensures complete compliance
"""

import os
import sys
import django
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import models

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirius_project.settings')
django.setup()

from corporate.models import Entity, Structure, EntityOwnership, ValidationRule
from parties.models import Party, PartyRole, BeneficiaryRelation


class ConformidadeTestCase(TestCase):
    """Test suite for 100% conformidade with SIRIUS MELHORIAS P2"""

    def setUp(self):
        """Set up test data"""
        # Create test entities
        self.entity1 = Entity.objects.create(
            name="Test Entity 1",
            entity_type="CORP",
            total_shares=1000
        )
        self.entity2 = Entity.objects.create(
            name="Test Entity 2", 
            entity_type="TRUST",
            total_shares=500
        )
        
        # Create test party
        self.party = Party.objects.create(
            name="Test Party",
            person_type="NATURAL_PERSON"
        )
        
        # Create test structure
        self.structure = Structure.objects.create(
            name="Test Structure",
            description="Test structure for conformidade"
        )

    def test_fase1_templates_field_not_json(self):
        """FASE 1: Test that templates field is TextField, not JSON"""
        entity_field = Entity._meta.get_field('implementation_templates')
        self.assertIsInstance(entity_field, models.TextField)
        self.assertTrue(entity_field.blank)  # Should be optional
        print("✓ FASE 1: Templates field is TextField (not JSON)")

    def test_fase1_total_shares_field(self):
        """FASE 1: Test that total_shares field exists in Entity"""
        entity_field = Entity._meta.get_field('total_shares')
        self.assertIsInstance(entity_field, models.PositiveIntegerField)
        self.assertTrue(entity_field.null)
        print("✓ FASE 1: total_shares field implemented")

    def test_fase2_corporate_name_hash_number(self):
        """FASE 2: Test Corporate Name and Hash Number implementation"""
        ownership = EntityOwnership.objects.create(
            structure=self.structure,
            owner_ubo=self.party,
            owned_entity=self.entity1,
            corporate_name="Test Corp Name",
            hash_number="HASH123",
            owned_shares=100,
            ownership_percentage=10.0
        )
        
        self.assertEqual(ownership.corporate_name, "Test Corp Name")
        self.assertEqual(ownership.hash_number, "HASH123")
        print("✓ FASE 2: Corporate Name and Hash Number implemented")

    def test_fase2_corporate_name_validation(self):
        """FASE 2: Test validation that Corporate Name or Hash Number is required"""
        with self.assertRaises(ValidationError):
            ownership = EntityOwnership(
                structure=self.structure,
                owner_ubo=self.party,
                owned_entity=self.entity1,
                # Missing both corporate_name and hash_number
                owned_shares=100
            )
            ownership.clean()
        print("✓ FASE 2: Corporate Name/Hash Number validation working")

    def test_fase3_shares_with_usd_eur_values(self):
        """FASE 3: Test shares with USD/EUR values"""
        ownership = EntityOwnership.objects.create(
            structure=self.structure,
            owner_ubo=self.party,
            owned_entity=self.entity1,
            corporate_name="Test Corp",
            owned_shares=100,
            share_value_usd=10.50,
            share_value_eur=9.25
        )
        
        self.assertEqual(ownership.share_value_usd, 10.50)
        self.assertEqual(ownership.share_value_eur, 9.25)
        self.assertEqual(ownership.total_value_usd, 1050.00)  # 100 * 10.50
        self.assertEqual(ownership.total_value_eur, 925.00)   # 100 * 9.25
        print("✓ FASE 3: Shares with USD/EUR values implemented")

    def test_fase4_auto_calculation_shares_percentage(self):
        """FASE 4: Test auto-calculation between shares and percentage"""
        # Test percentage to shares calculation
        ownership1 = EntityOwnership.objects.create(
            structure=self.structure,
            owner_ubo=self.party,
            owned_entity=self.entity1,
            corporate_name="Test Corp 1",
            ownership_percentage=25.0  # Should calculate 250 shares (25% of 1000)
        )
        self.assertEqual(ownership1.owned_shares, 250)
        
        # Test shares to percentage calculation
        ownership2 = EntityOwnership.objects.create(
            structure=self.structure,
            owner_entity=self.entity2,
            owned_entity=self.entity1,
            corporate_name="Test Corp 2",
            owned_shares=500  # Should calculate 50% (500 of 1000)
        )
        self.assertEqual(ownership2.ownership_percentage, 50.0)
        print("✓ FASE 4: Auto-calculation shares ↔ percentage working")

    def test_fase4_shares_distribution_validation(self):
        """FASE 4: Test validation that shares cannot exceed total"""
        with self.assertRaises(ValidationError):
            ownership = EntityOwnership(
                structure=self.structure,
                owner_ubo=self.party,
                owned_entity=self.entity1,
                corporate_name="Test Corp",
                owned_shares=1500  # Exceeds total_shares (1000)
            )
            ownership.clean()
        print("✓ FASE 4: Shares distribution validation working")

    def test_fase5_tax_impacts_severities_structure(self):
        """FASE 5: Test Tax Impacts and Severities in Structure"""
        # Create validation rule
        rule = ValidationRule.objects.create(
            parent_entity=self.entity1,
            related_entity=self.entity2,
            relationship_type="INCOMPATIBLE",
            severity="WARNING",
            tax_impacts="High tax implications in US jurisdiction",
            description="Test rule"
        )
        
        # Add entities to structure
        EntityOwnership.objects.create(
            structure=self.structure,
            owner_ubo=self.party,
            owned_entity=self.entity1,
            corporate_name="Corp 1",
            owned_shares=100
        )
        EntityOwnership.objects.create(
            structure=self.structure,
            owner_entity=self.entity1,
            owned_entity=self.entity2,
            corporate_name="Corp 2",
            owned_shares=50
        )
        
        # Test calculated fields
        tax_impacts = self.structure.combined_tax_impacts
        severities = self.structure.combined_severities
        
        self.assertIn("High tax implications", tax_impacts)
        self.assertIn("WARNING", severities)
        print("✓ FASE 5: Tax Impacts and Severities calculation working")

    def test_fase6_prohibited_combinations_validation(self):
        """FASE 6: Test validation of prohibited combinations"""
        # Create prohibited rule
        ValidationRule.objects.create(
            parent_entity=self.entity1,
            related_entity=self.entity2,
            relationship_type="PROHIBITED",
            severity="ERROR",
            description="This combination is prohibited"
        )
        
        # Add first entity
        EntityOwnership.objects.create(
            structure=self.structure,
            owner_ubo=self.party,
            owned_entity=self.entity1,
            corporate_name="Corp 1",
            owned_shares=100
        )
        
        # Try to add second entity (should fail)
        EntityOwnership.objects.create(
            structure=self.structure,
            owner_entity=self.entity1,
            owned_entity=self.entity2,
            corporate_name="Corp 2",
            owned_shares=50
        )
        
        with self.assertRaises(ValidationError):
            self.structure.clean()
        print("✓ FASE 6: Prohibited combinations validation working")

    def test_fase7_automatic_beneficiary_role(self):
        """FASE 7: Test automatic beneficiary role creation"""
        beneficiary = Party.objects.create(
            name="Beneficiary Party",
            person_type="NATURAL_PERSON"
        )
        
        # Create beneficiary relation
        BeneficiaryRelation.objects.create(
            giver_party=self.party,
            beneficiary=beneficiary,
            percentage=50.0
        )
        
        # Check that beneficiary role was created automatically
        beneficiary_role_exists = PartyRole.objects.filter(
            party=beneficiary,
            role_type='BENEFICIARY'
        ).exists()
        
        self.assertTrue(beneficiary_role_exists)
        print("✓ FASE 7: Automatic beneficiary role creation working")

    def test_fase8_status_colors_files_exist(self):
        """FASE 8: Test that status color files exist"""
        import os
        
        css_file = 'static/admin/css/structure_status_colors.css'
        js_file = 'static/admin/js/structure_status_colors.js'
        
        self.assertTrue(os.path.exists(css_file))
        self.assertTrue(os.path.exists(js_file))
        print("✓ FASE 8: Status color CSS and JS files exist")

    def test_overall_conformidade_100_percent(self):
        """Test overall 100% conformidade"""
        print("\n" + "="*60)
        print("🎯 SIRIUS MELHORIAS P2 - CONFORMIDADE 100% VALIDATION")
        print("="*60)
        
        # Run all individual tests
        test_methods = [
            self.test_fase1_templates_field_not_json,
            self.test_fase1_total_shares_field,
            self.test_fase2_corporate_name_hash_number,
            self.test_fase2_corporate_name_validation,
            self.test_fase3_shares_with_usd_eur_values,
            self.test_fase4_auto_calculation_shares_percentage,
            self.test_fase4_shares_distribution_validation,
            self.test_fase5_tax_impacts_severities_structure,
            self.test_fase6_prohibited_combinations_validation,
            self.test_fase7_automatic_beneficiary_role,
            self.test_fase8_status_colors_files_exist,
        ]
        
        passed_tests = 0
        total_tests = len(test_methods)
        
        for test_method in test_methods:
            try:
                test_method()
                passed_tests += 1
            except Exception as e:
                print(f"❌ {test_method.__name__}: {e}")
        
        conformidade_percentage = (passed_tests / total_tests) * 100
        
        print(f"\n📊 CONFORMIDADE RESULT: {conformidade_percentage:.1f}%")
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        
        if conformidade_percentage == 100:
            print("🏆 SIRIUS SYSTEM IS 100% COMPLIANT WITH MELHORIAS P2!")
        else:
            print(f"⚠️  {100 - conformidade_percentage:.1f}% remaining for full compliance")
        
        print("="*60)


def run_tests():
    """Run the conformidade test suite"""
    import unittest
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(ConformidadeTestCase)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("🚀 Starting SIRIUS MELHORIAS P2 Conformidade Tests...")
    success = run_tests()
    
    if success:
        print("\n✅ All conformidade tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some conformidade tests failed!")
        sys.exit(1)

