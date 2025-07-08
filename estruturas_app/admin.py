from django.contrib import admin
from .models import Estrutura

# NOTE: Admin registration moved to corporate.admin for unified management
# The Estrutura model is now a proxy for corporate.Structure
# All admin functionality is available through corporate.StructureAdmin

# The legacy admin has been disabled to avoid conflicts.
# To manage Legal Structures, use the Corporate app admin interface.

# If you need to restore the legacy admin interface, uncomment the following:

# from django.utils.html import format_html

# @admin.register(Estrutura)
# class EstruturaAdmin(admin.ModelAdmin):
#     """
#     Legacy admin interface for managing legal structures.
#     Use corporate.StructureAdmin for new functionality.
#     """
#     list_display = [
#         'nome', 
#         'tipo', 
#         'get_full_jurisdiction_display',
#         'custo_base', 
#         'custo_manutencao',
#         'ativo'
#     ]
#     list_filter = [
#         'tipo',
#         'jurisdicao',
#         'ativo'
#     ]
#     search_fields = ['nome', 'descricao']
#     readonly_fields = ['created_at', 'updated_at']

