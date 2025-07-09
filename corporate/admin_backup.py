# Corporate Admin Configuration
# This file imports the improved admin interface for the SIRIUS system

try:
    # Import the improved admin - this provides enhanced UX features
    from .admin_improved import *
    print("✅ Admin melhorado carregado com sucesso!")
except ImportError as e:
    print(f"⚠️ Admin melhorado não encontrado: {e}")
    
    # Fallback to basic admin if improved admin is not available
    from django.contrib import admin
    from .models import Entity, Structure, EntityOwnership, ValidationRule
    
    # Basic admin registration
    admin.site.register(Entity)
    admin.site.register(Structure) 
    admin.site.register(EntityOwnership)
    admin.site.register(ValidationRule)
    
    print("📋 Admin básico carregado como fallback")
