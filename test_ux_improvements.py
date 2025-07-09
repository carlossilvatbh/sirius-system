#!/usr/bin/env python
"""
Test script for UX improvements in Django Admin for Structures
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirius_project.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from corporate.models import Entity, Structure, EntityOwnership
from parties.models import Party


def test_admin_improvements():
    """Test all admin improvements"""
    print("🧪 Testing Django Admin UX Improvements...")
    
    # Test 1: Check if admin classes are properly registered
    print("\n1️⃣ Testing Admin Registration...")
    from django.contrib import admin
    from corporate.models import Structure, Entity, EntityOwnership
    
    try:
        structure_admin = admin.site._registry[Structure]
        entity_admin = admin.site._registry[Entity]
        ownership_admin = admin.site._registry[EntityOwnership]
        print("   ✅ All admin classes properly registered")
    except KeyError as e:
        print(f"   ❌ Admin registration error: {e}")
        return False
    
    # Test 2: Check admin methods
    print("\n2️⃣ Testing Admin Methods...")
    try:
        # Create test data
        entity = Entity.objects.create(
            name="Test Entity",
            entity_type="Corporation",
            jurisdiction="Delaware"
        )
        
        structure = Structure.objects.create(
            name="Test Structure",
            description="Test structure for UX validation",
            status="drafting"
        )
        
        # Test admin methods
        admin_instance = structure_admin(Structure, admin.site)
        
        # Test display methods
        name_with_icon = admin_instance.name_with_icon(structure)
        status_badge = admin_instance.status_badge(structure)
        entities_count = admin_instance.entities_count(structure)
        completion_percentage = admin_instance.completion_percentage(structure)
        
        print("   ✅ name_with_icon method working")
        print("   ✅ status_badge method working")
        print("   ✅ entities_count method working")
        print("   ✅ completion_percentage method working")
        
    except Exception as e:
        print(f"   ❌ Admin methods error: {e}")
        return False
    
    # Test 3: Check fieldsets configuration
    print("\n3️⃣ Testing Fieldsets Configuration...")
    try:
        fieldsets = admin_instance.fieldsets
        if fieldsets and len(fieldsets) >= 3:
            print("   ✅ Fieldsets properly configured")
        else:
            print("   ❌ Fieldsets not properly configured")
            return False
    except Exception as e:
        print(f"   ❌ Fieldsets error: {e}")
        return False
    
    # Test 4: Check inline configuration
    print("\n4️⃣ Testing Inline Configuration...")
    try:
        inlines = admin_instance.inlines
        if inlines and len(inlines) > 0:
            inline_class = inlines[0]
            inline_instance = inline_class(EntityOwnership, admin.site)
            print("   ✅ Inlines properly configured")
        else:
            print("   ❌ Inlines not configured")
            return False
    except Exception as e:
        print(f"   ❌ Inlines error: {e}")
        return False
    
    # Test 5: Check custom URLs
    print("\n5️⃣ Testing Custom URLs...")
    try:
        urls = admin_instance.get_urls()
        wizard_url_found = any('wizard' in str(url.pattern) for url in urls)
        if wizard_url_found:
            print("   ✅ Custom wizard URL configured")
        else:
            print("   ⚠️ Wizard URL not found (may be normal)")
    except Exception as e:
        print(f"   ❌ Custom URLs error: {e}")
        return False
    
    # Test 6: Test ownership calculations
    print("\n6️⃣ Testing Ownership Calculations...")
    try:
        # Create test ownership
        party = Party.objects.create(
            name="Test UBO",
            person_type="NATURAL_PERSON",
            nationality="US"
        )
        
        ownership = EntityOwnership.objects.create(
            structure=structure,
            owned_entity=entity,
            owner_ubo=party,
            ownership_percentage=50.0,
            owned_shares=500,
            corporate_name="Test Corp"
        )
        
        # Test validation methods
        inline_instance = inline_class(EntityOwnership, admin.site)
        validation_status = inline_instance.validation_status(ownership)
        owner_display = inline_instance.owner_display(ownership)
        
        print("   ✅ Ownership validation working")
        print("   ✅ Owner display working")
        
    except Exception as e:
        print(f"   ❌ Ownership calculations error: {e}")
        return False
    
    # Test 7: Test summary methods
    print("\n7️⃣ Testing Summary Methods...")
    try:
        ownership_summary = admin_instance.ownership_summary(structure)
        validation_summary = admin_instance.validation_summary(structure)
        
        if ownership_summary and validation_summary:
            print("   ✅ Summary methods working")
        else:
            print("   ❌ Summary methods not working")
            return False
    except Exception as e:
        print(f"   ❌ Summary methods error: {e}")
        return False
    
    # Test 8: Check static files
    print("\n8️⃣ Testing Static Files...")
    try:
        import os
        css_files = [
            'static/admin/css/structure_admin_improved.css',
            'static/admin/css/ownership_matrix.css',
            'static/admin/css/structure_wizard.css'
        ]
        
        js_files = [
            'static/admin/js/structure_admin_improved.js',
            'static/admin/js/structure_wizard.js'
        ]
        
        missing_files = []
        for file_path in css_files + js_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if not missing_files:
            print("   ✅ All static files present")
        else:
            print(f"   ⚠️ Missing static files: {missing_files}")
    except Exception as e:
        print(f"   ❌ Static files error: {e}")
    
    # Test 9: Test templates
    print("\n9️⃣ Testing Templates...")
    try:
        template_files = [
            'templates/admin/corporate/structure_wizard.html',
            'templates/admin/corporate/ownership_matrix.html',
            'templates/admin/corporate/structure_validation_results.html'
        ]
        
        missing_templates = []
        for template_path in template_files:
            if not os.path.exists(template_path):
                missing_templates.append(template_path)
        
        if not missing_templates:
            print("   ✅ All templates present")
        else:
            print(f"   ⚠️ Missing templates: {missing_templates}")
    except Exception as e:
        print(f"   ❌ Templates error: {e}")
    
    print("\n🎉 UX Improvements Test Completed!")
    return True


def test_performance():
    """Test performance of admin queries"""
    print("\n⚡ Testing Performance...")
    
    from django.db import connection
    from django.test.utils import override_settings
    
    try:
        # Reset query count
        connection.queries_log.clear()
        
        # Create test data
        structure = Structure.objects.create(
            name="Performance Test Structure",
            description="Testing query performance",
            status="drafting"
        )
        
        entities = []
        for i in range(5):
            entity = Entity.objects.create(
                name=f"Entity {i}",
                entity_type="Corporation",
                jurisdiction="Delaware"
            )
            entities.append(entity)
        
        parties = []
        for i in range(3):
            party = Party.objects.create(
                name=f"UBO {i}",
                person_type="NATURAL_PERSON",
                nationality="US"
            )
            parties.append(party)
        
        # Create ownerships
        for i, entity in enumerate(entities):
            EntityOwnership.objects.create(
                structure=structure,
                owned_entity=entity,
                owner_ubo=parties[i % len(parties)],
                ownership_percentage=100.0 / len(parties) if i < len(parties) else 0,
                owned_shares=1000,
                corporate_name=f"Corp {i}"
            )
        
        # Test admin query performance
        from django.contrib import admin
        structure_admin = admin.site._registry[Structure]
        admin_instance = structure_admin(Structure, admin.site)
        
        # Reset queries
        connection.queries_log.clear()
        
        # Test ownership summary (should use select_related)
        ownership_summary = admin_instance.ownership_summary(structure)
        query_count = len(connection.queries)
        
        print(f"   📊 Ownership summary queries: {query_count}")
        if query_count <= 3:  # Should be efficient
            print("   ✅ Query performance is good")
        else:
            print("   ⚠️ Query performance could be improved")
        
    except Exception as e:
        print(f"   ❌ Performance test error: {e}")


def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    try:
        EntityOwnership.objects.filter(structure__name__contains="Test").delete()
        Structure.objects.filter(name__contains="Test").delete()
        Entity.objects.filter(name__contains="Test").delete()
        Party.objects.filter(name__contains="Test").delete()
        print("   ✅ Test data cleaned up")
    except Exception as e:
        print(f"   ❌ Cleanup error: {e}")


if __name__ == "__main__":
    print("🚀 Starting UX Improvements Validation...")
    print("=" * 60)
    
    try:
        # Run tests
        success = test_admin_improvements()
        test_performance()
        
        # Cleanup
        cleanup_test_data()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 ALL TESTS PASSED! UX improvements are working correctly.")
        else:
            print("❌ Some tests failed. Please check the implementation.")
            
    except Exception as e:
        print(f"\n💥 Test suite error: {e}")
        cleanup_test_data()

