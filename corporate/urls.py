from django.urls import path
from . import views

app_name = 'corporate'

urlpatterns = [
    # Structure Wizard (implemented)
    path('structure-wizard/', views.StructureWizardView.as_view(), name='structure_wizard'),
    
    # Structure Visualization - Enhanced view for the new node-based system
    path('structures/', views.StructureVisualizationView.as_view(), name='structure_list'),
    path('structures/<int:structure_id>/', views.StructureVisualizationView.as_view(), name='structure_detail'),
    path('api/structures/<int:structure_id>/json/', views.structure_json_api, name='structure_json_api'),
    
    # TODO: Implement these views
    # path('structure-builder/', views.StructureBuilderView.as_view(), name='structure_builder'),
    # path('ownership-matrix/<int:structure_id>/', views.OwnershipMatrixView.as_view(), name='ownership_matrix'),
    # path('ownership-matrix/', views.OwnershipMatrixView.as_view(), name='ownership_matrix_list'),
    # path('api/validate-structure/', views.StructureValidationAPI.as_view(), name='validate_structure'),
    # path('api/structure-preview/', views.StructurePreviewAPI.as_view(), name='structure_preview'),
    # path('api/ownership-data/<int:structure_id>/', views.OwnershipDataAPI.as_view(), name='ownership_data'),
]

