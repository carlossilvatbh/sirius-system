# SIRIUS System Migration Guide

## Overview

This document outlines the migration process for the SIRIUS system refactoring that implements a comprehensive architectural enhancement across 5 phases.

## Migration Summary

### Phase 1: Corporate App Refactoring
- **Structure** model renamed to **Entity**
- New **Structure** model for corporate hierarchies
- New **EntityOwnership** model for ownership relationships
- New **MasterEntity** model for structure roots
- Enhanced **ValidationRule** model

### Phase 2: Financial Department App
- New app: `financial_department`
- **EntityPrice** model for entity pricing
- **IncorporationCost** model for cost components
- **ServicePrice** and **ServiceCost** models for service pricing

### Phase 3: Parties App
- New app: `parties`
- **Party** model (replaces UBO functionality)
- **PartyRole** model for multiple roles
- **Passport** model for document management
- **BeneficiaryRelation** model (replaces Successor)
- **DocumentAttachment** model for document URLs

### Phase 4: Sales App Refactoring
- **Partner** model (replaces Client)
- **Contact** model moved from corporate_relationship
- **StructureRequest** model for structure requests
- **StructureApproval** model for approval workflow

### Phase 5: Corporate Relationships Updates
- **File** model for approved structures
- Updated **Service** and **ServiceActivity** models
- Enhanced **RelationshipStructure** model

## Data Migration Strategy

### 1. Backup Current Data
```bash
# Create database backup
python manage.py dumpdata > backup_before_migration.json

# Create model backups (already done)
cp -r corporate corporate_backup
cp -r sales sales_backup
cp -r corporate_relationship corporate_relationship_backup
```

### 2. Migration Steps

#### Step 1: Install Dependencies
```bash
pip install python-dateutil
```

#### Step 2: Create Initial Migrations
```bash
python manage.py makemigrations financial_department
python manage.py makemigrations parties
python manage.py makemigrations corporate
python manage.py makemigrations sales
python manage.py makemigrations corporate_relationship
```

#### Step 3: Apply Migrations
```bash
python manage.py migrate financial_department
python manage.py migrate parties
python manage.py migrate corporate
python manage.py migrate sales
python manage.py migrate corporate_relationship
```

#### Step 4: Data Migration Scripts

Create custom migration scripts for data transformation:

1. **Migrate Structure → Entity**
   - Copy all Structure records to Entity table
   - Update field mappings (nome → name, etc.)
   - Preserve all relationships

2. **Migrate UBO → Party**
   - Copy all UBO records to Party table
   - Set person_type based on tipo_pessoa
   - Create PartyRole records for UBO roles

3. **Migrate Client → Partner**
   - Copy Client records to Partner table
   - Create corresponding Party records
   - Link Partner to Party via OneToOne

4. **Migrate Successor → BeneficiaryRelation**
   - Copy Successor records to BeneficiaryRelation
   - Update field mappings
   - Link to new Party records

### 3. Validation Steps

After migration, validate:

1. **Data Integrity**
   - All records migrated successfully
   - No data loss
   - Relationships preserved

2. **Functional Testing**
   - Admin interface works
   - All models accessible
   - Validation rules function

3. **Performance Testing**
   - Query performance maintained
   - Index effectiveness

## Model Mapping Reference

### Structure → Entity
```python
# Old Structure fields → New Entity fields
nome → name
tipo → entity_type
descricao → removed (no longer needed)
templates → implementation_templates
jurisdicao → jurisdiction
estado_us → us_state
estado_br → br_state
# ... other field mappings
```

### UBO → Party
```python
# Old UBO fields → New Party fields
nome → name
tipo_pessoa → person_type
email → email
telefone → phone
endereco → address
# ... other field mappings
```

### Client → Partner
```python
# Old Client fields → New Partner fields
company_name → company_name
address → address
created_at → created_at
# + new Party relationship
```

## Post-Migration Tasks

1. **Update Admin Configurations**
   - Register new models in admin
   - Configure inlines and fieldsets
   - Test admin functionality

2. **Update Views and URLs**
   - Update any hardcoded model references
   - Test all endpoints
   - Update API serializers if applicable

3. **Update Templates**
   - Update any template references
   - Test frontend functionality

4. **Documentation Updates**
   - Update API documentation
   - Update user manuals
   - Update technical documentation

## Rollback Strategy

If migration fails:

1. **Restore from Backup**
   ```bash
   # Restore database
   python manage.py loaddata backup_before_migration.json
   
   # Restore model files
   cp -r corporate_backup/* corporate/
   cp -r sales_backup/* sales/
   cp -r corporate_relationship_backup/* corporate_relationship/
   ```

2. **Remove New Apps**
   - Remove from INSTALLED_APPS
   - Delete migration files
   - Delete app directories

## Testing Checklist

- [ ] All models can be created via admin
- [ ] All relationships work correctly
- [ ] Validation rules function properly
- [ ] No circular import errors
- [ ] Performance is acceptable
- [ ] All existing functionality preserved
- [ ] New functionality works as expected

## Support and Troubleshooting

### Common Issues

1. **Circular Import Errors**
   - Check model references
   - Use string references for foreign keys
   - Verify app order in INSTALLED_APPS

2. **Migration Conflicts**
   - Delete migration files and recreate
   - Use --fake-initial if needed
   - Check for dependency conflicts

3. **Data Loss**
   - Restore from backup
   - Check migration scripts
   - Verify field mappings

### Contact Information

For migration support, contact the development team or refer to the Django documentation for advanced migration techniques.

## Conclusion

This migration represents a significant architectural improvement to the SIRIUS system, providing better separation of concerns, enhanced corporate hierarchy management, and improved financial management capabilities while maintaining data integrity and system stability.

