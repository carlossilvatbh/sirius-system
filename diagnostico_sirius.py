#!/usr/bin/env python
"""
Script de diagnóstico para verificar problemas no sistema Sirius
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sirius_project.settings')
django.setup()

def test_models():
    """Testa se os modelos estão funcionando"""
    print("🔍 Testando Modelos...")
    try:
        from corporate.models import Entity, Structure, StructureNode, NodeOwnership
        from parties.models import Party
        
        print(f"✅ Entidades: {Entity.objects.count()}")
        print(f"✅ Estruturas: {Structure.objects.count()}")
        print(f"✅ Nós: {StructureNode.objects.count()}")
        print(f"✅ Propriedades: {NodeOwnership.objects.count()}")
        print(f"✅ Partes: {Party.objects.count()}")
        
        if Structure.objects.exists():
            s = Structure.objects.first()
            print(f"✅ Primeira estrutura: {s.name} (ID: {s.id})")
        
        return True
    except Exception as e:
        print(f"❌ Erro nos modelos: {e}")
        return False

def test_urls():
    """Testa se as URLs estão configuradas"""
    print("\n🔍 Testando URLs...")
    try:
        from django.urls import reverse
        
        urls_to_test = [
            ('dashboard:main', None),
            ('corporate:structure_list', None),
            ('corporate:structure_detail', [1]),
            ('corporate:structure_json_api', [1]),
        ]
        
        for url_name, args in urls_to_test:
            try:
                if args:
                    url = reverse(url_name, args=args)
                else:
                    url = reverse(url_name)
                print(f"✅ {url_name}: {url}")
            except Exception as e:
                print(f"❌ {url_name}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Erro geral nas URLs: {e}")
        return False

def test_views():
    """Testa se as views estão funcionando"""
    print("\n🔍 Testando Views...")
    try:
        from corporate.views import StructureVisualizationView
        from dashboard.views import DashboardView
        
        print("✅ StructureVisualizationView importada")
        print("✅ DashboardView importada")
        
        return True
    except Exception as e:
        print(f"❌ Erro nas views: {e}")
        return False

def test_templates():
    """Verifica se os templates existem"""
    print("\n🔍 Verificando Templates...")
    try:
        import os
        from django.conf import settings
        
        templates_to_check = [
            'templates/corporate/structure_visualization.html',
            'dashboard/templates/admin/dashboard/dashboard.html',
            'templates/admin/base_site.html',
        ]
        
        for template in templates_to_check:
            if os.path.exists(template):
                print(f"✅ {template}")
            else:
                print(f"❌ {template} - NÃO ENCONTRADO")
        
        return True
    except Exception as e:
        print(f"❌ Erro verificando templates: {e}")
        return False

def test_admin():
    """Testa se o admin está funcionando"""
    print("\n🔍 Testando Admin...")
    try:
        from django.contrib import admin
        from corporate.models import Entity, Structure, StructureNode, NodeOwnership
        
        models_registered = [
            Entity,
            Structure, 
            StructureNode,
            NodeOwnership
        ]
        
        for model in models_registered:
            if admin.site.is_registered(model):
                print(f"✅ {model.__name__} registrado no admin")
            else:
                print(f"❌ {model.__name__} NÃO registrado no admin")
        
        return True
    except Exception as e:
        print(f"❌ Erro no admin: {e}")
        return False

def test_settings():
    """Verifica configurações importantes"""
    print("\n🔍 Verificando Settings...")
    try:
        from django.conf import settings
        
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps")
        
        required_apps = ['corporate', 'dashboard', 'parties']
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print(f"✅ App {app} instalado")
            else:
                print(f"❌ App {app} NÃO instalado")
        
        return True
    except Exception as e:
        print(f"❌ Erro nas configurações: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 DIAGNÓSTICO DO SISTEMA SIRIUS")
    print("=" * 50)
    
    tests = [
        test_settings,
        test_models,
        test_urls,
        test_views,
        test_templates,
        test_admin,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro executando {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS RESULTADOS")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 TODOS OS TESTES PASSARAM! ({passed}/{total})")
        print("✅ Sistema funcionando corretamente!")
    else:
        print(f"⚠️  {passed}/{total} testes passaram")
        print("❌ Existem problemas que precisam ser corrigidos")
    
    print("\n🌐 Para testar manualmente:")
    print("- Dashboard: http://127.0.0.1:8000/dashboard/")
    print("- Estruturas: http://127.0.0.1:8000/corporate/structures/")
    print("- Admin: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    main()
