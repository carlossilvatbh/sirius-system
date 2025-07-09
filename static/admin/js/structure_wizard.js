/* ============================================================================
   SIRIUS STRUCTURE WIZARD JAVASCRIPT
   ============================================================================ */

(function() {
    'use strict';

    // Global wizard state
    window.StructureWizard = {
        currentStep: 1,
        totalSteps: 5,
        structureId: null,
        isEditing: false,
        selectedEntities: [],
        selectedUBOs: [],
        ownerships: [],
        validationResults: null,
        previewData: null
    };

    // Initialize wizard when DOM is ready
    $(document).ready(function() {
        initializeWizard();
    });

    function initializeWizard() {
        console.log('Initializing Structure Wizard...');
        
        // Load wizard data from template
        if (window.wizardData) {
            StructureWizard.structureId = wizardData.structureId;
            StructureWizard.isEditing = wizardData.isEditing;
            
            if (wizardData.ownerships && wizardData.ownerships.length > 0) {
                StructureWizard.ownerships = wizardData.ownerships;
                loadExistingData();
            }
        }
        
        // Initialize components
        initializeStepNavigation();
        initializeFormValidation();
        initializeSearch();
        initializeOwnershipBuilder();
        
        // Show first step
        showStep(1);
        
        console.log('Structure Wizard initialized successfully');
    }

    // ========================================================================
    // STEP NAVIGATION
    // ========================================================================

    function initializeStepNavigation() {
        // Update step indicators
        updateStepIndicators();
        
        // Bind navigation events
        $('.step').on('click', function() {
            var stepNumber = parseInt($(this).data('step'));
            if (stepNumber <= StructureWizard.currentStep || canNavigateToStep(stepNumber)) {
                showStep(stepNumber);
            }
        });
    }

    window.nextStep = function() {
        if (validateCurrentStep()) {
            saveCurrentStep().then(function() {
                if (StructureWizard.currentStep < StructureWizard.totalSteps) {
                    showStep(StructureWizard.currentStep + 1);
                }
            });
        }
    };

    window.previousStep = function() {
        if (StructureWizard.currentStep > 1) {
            showStep(StructureWizard.currentStep - 1);
        }
    };

    function showStep(stepNumber) {
        // Hide all step contents
        $('.step-content').hide();
        
        // Show target step
        $('#step-content-' + stepNumber).show().addClass('fade-in');
        
        // Update current step
        StructureWizard.currentStep = stepNumber;
        
        // Update UI
        updateStepIndicators();
        updateNavigationButtons();
        updateStepCounter();
        
        // Load step-specific data
        loadStepData(stepNumber);
        
        console.log('Showing step:', stepNumber);
    }

    function updateStepIndicators() {
        $('.step').each(function() {
            var stepNumber = parseInt($(this).data('step'));
            var $step = $(this);
            
            $step.removeClass('active completed');
            
            if (stepNumber === StructureWizard.currentStep) {
                $step.addClass('active');
            } else if (stepNumber < StructureWizard.currentStep) {
                $step.addClass('completed');
            }
        });
        
        // Update connectors
        $('.step-connector').each(function(index) {
            var $connector = $(this);
            if (index + 1 < StructureWizard.currentStep) {
                $connector.addClass('completed');
            } else {
                $connector.removeClass('completed');
            }
        });
    }

    function updateNavigationButtons() {
        var $prevBtn = $('.btn-previous');
        var $nextBtn = $('.btn-next');
        var $saveBtn = $('.btn-save');
        
        // Previous button
        if (StructureWizard.currentStep === 1) {
            $prevBtn.hide();
        } else {
            $prevBtn.show();
        }
        
        // Next/Save button
        if (StructureWizard.currentStep === StructureWizard.totalSteps) {
            $nextBtn.hide();
            $saveBtn.show();
        } else {
            $nextBtn.show();
            $saveBtn.hide();
        }
    }

    function updateStepCounter() {
        $('#current-step').text(StructureWizard.currentStep);
    }

    function canNavigateToStep(stepNumber) {
        // Allow navigation to completed steps or next step
        return stepNumber <= StructureWizard.currentStep + 1;
    }

    // ========================================================================
    // STEP VALIDATION
    // ========================================================================

    function validateCurrentStep() {
        switch (StructureWizard.currentStep) {
            case 1:
                return validateBasicInfo();
            case 2:
                return validateEntitiesUBOs();
            case 3:
                return validateOwnership();
            case 4:
                return validateStructure();
            case 5:
                return true; // Final step always valid
            default:
                return true;
        }
    }

    function validateBasicInfo() {
        var isValid = true;
        var name = $('#structure-name').val().trim();
        
        // Clear previous errors
        $('.form-group').removeClass('error success');
        $('.field-error').remove();
        
        if (!name) {
            showFieldError('#structure-name', 'Structure name is required');
            isValid = false;
        } else {
            showFieldSuccess('#structure-name', 'Valid name');
        }
        
        return isValid;
    }

    function validateEntitiesUBOs() {
        var hasEntities = StructureWizard.selectedEntities.length > 0;
        var hasUBOs = StructureWizard.selectedUBOs.length > 0;
        
        if (!hasEntities && !hasUBOs) {
            showMessage('Please select at least one entity or UBO', 'error');
            return false;
        }
        
        return true;
    }

    function validateOwnership() {
        if (StructureWizard.ownerships.length === 0) {
            showMessage('Please define at least one ownership relationship', 'error');
            return false;
        }
        
        // Validate each ownership
        var isValid = true;
        StructureWizard.ownerships.forEach(function(ownership, index) {
            if (!ownership.owned_entity_id) {
                showMessage('Ownership ' + (index + 1) + ': Missing owned entity', 'error');
                isValid = false;
            }
            
            if (!ownership.owner_ubo_id && !ownership.owner_entity_id) {
                showMessage('Ownership ' + (index + 1) + ': Missing owner', 'error');
                isValid = false;
            }
            
            if (!ownership.percentage || ownership.percentage <= 0) {
                showMessage('Ownership ' + (index + 1) + ': Invalid percentage', 'error');
                isValid = false;
            }
        });
        
        return isValid;
    }

    function validateStructure() {
        // This will be validated on the server
        return true;
    }

    function showFieldError(selector, message) {
        var $field = $(selector);
        var $group = $field.closest('.form-group');
        
        $group.addClass('error');
        $group.append('<div class="field-error">' + message + '</div>');
    }

    function showFieldSuccess(selector, message) {
        var $field = $(selector);
        var $group = $field.closest('.form-group');
        
        $group.addClass('success');
        if (message) {
            $group.append('<div class="field-success">' + message + '</div>');
        }
    }

    // ========================================================================
    // STEP DATA LOADING
    // ========================================================================

    function loadStepData(stepNumber) {
        switch (stepNumber) {
            case 2:
                loadEntitiesUBOsStep();
                break;
            case 3:
                loadOwnershipBuilderStep();
                break;
            case 4:
                loadValidationStep();
                break;
            case 5:
                loadSaveStep();
                break;
        }
    }

    function loadEntitiesUBOsStep() {
        // Update selected items display
        updateSelectedEntitiesDisplay();
        updateSelectedUBOsDisplay();
    }

    function loadOwnershipBuilderStep() {
        // Populate owner and entity dropdowns
        populateOwnershipDropdowns();
        
        // Render existing ownerships
        renderOwnershipTable();
        
        // Update summary
        updateOwnershipSummary();
    }

    function loadValidationStep() {
        // Show loading
        $('#validation-results').html(
            '<div class="validation-loading">' +
                '<div class="spinner"></div>' +
                '<span>Running validation...</span>' +
            '</div>'
        );
        
        // Run validation
        runValidation();
    }

    function loadSaveStep() {
        // Generate final summary
        generateFinalSummary();
    }

    function loadExistingData() {
        // Load existing ownerships into wizard state
        if (wizardData.ownerships) {
            StructureWizard.ownerships = wizardData.ownerships.map(function(ownership) {
                return {
                    id: ownership.id,
                    owned_entity_id: ownership.owned_entity_id,
                    owned_entity_name: ownership.owned_entity_name,
                    owner_ubo_id: ownership.owner_ubo_id,
                    owner_ubo_name: ownership.owner_ubo_name,
                    owner_entity_id: ownership.owner_entity_id,
                    owner_entity_name: ownership.owner_entity_name,
                    percentage: ownership.percentage,
                    shares: ownership.shares,
                    corporate_name: ownership.corporate_name,
                    hash_number: ownership.hash_number,
                    share_value_usd: ownership.share_value_usd,
                    share_value_eur: ownership.share_value_eur
                };
            });
            
            // Extract selected entities and UBOs
            var entityIds = new Set();
            var uboIds = new Set();
            
            StructureWizard.ownerships.forEach(function(ownership) {
                if (ownership.owned_entity_id) {
                    entityIds.add(ownership.owned_entity_id);
                }
                if (ownership.owner_entity_id) {
                    entityIds.add(ownership.owner_entity_id);
                }
                if (ownership.owner_ubo_id) {
                    uboIds.add(ownership.owner_ubo_id);
                }
            });
            
            StructureWizard.selectedEntities = Array.from(entityIds);
            StructureWizard.selectedUBOs = Array.from(uboIds);
        }
    }

    // ========================================================================
    // FORM VALIDATION
    // ========================================================================

    function initializeFormValidation() {
        // Real-time validation for basic info
        $('#structure-name').on('input', function() {
            var value = $(this).val().trim();
            var $group = $(this).closest('.form-group');
            
            $group.removeClass('error success');
            $('.field-error, .field-success').remove();
            
            if (value.length > 0) {
                showFieldSuccess('#structure-name');
            }
        });
        
        // Percentage validation
        $(document).on('input', 'input[name="percentage"]', function() {
            var value = parseFloat($(this).val());
            var $input = $(this);
            
            $input.removeClass('error success warning');
            
            if (isNaN(value)) {
                return;
            }
            
            if (value < 0 || value > 100) {
                $input.addClass('error');
            } else if (value === 100) {
                $input.addClass('success');
            } else if (value > 0) {
                $input.addClass('warning');
            }
        });
    }

    // ========================================================================
    // SEARCH FUNCTIONALITY
    // ========================================================================

    function initializeSearch() {
        // Entity search
        $('#entity-search').on('input', function() {
            var searchTerm = $(this).val().toLowerCase();
            filterItems('#entities-list .entity-card', searchTerm);
        });
        
        // UBO search
        $('#ubo-search').on('input', function() {
            var searchTerm = $(this).val().toLowerCase();
            filterItems('#ubos-list .ubo-card', searchTerm);
        });
    }

    function filterItems(selector, searchTerm) {
        $(selector).each(function() {
            var $item = $(this);
            var text = $item.text().toLowerCase();
            
            if (text.includes(searchTerm)) {
                $item.show();
            } else {
                $item.hide();
            }
        });
    }

    // ========================================================================
    // ENTITY/UBO SELECTION
    // ========================================================================

    window.selectEntity = function(entityId) {
        var index = StructureWizard.selectedEntities.indexOf(entityId);
        
        if (index === -1) {
            // Add entity
            StructureWizard.selectedEntities.push(entityId);
            $('.entity-card[data-id="' + entityId + '"]').addClass('selected');
            $('.entity-card[data-id="' + entityId + '"] .btn-select').text('Selected').addClass('selected');
        } else {
            // Remove entity
            StructureWizard.selectedEntities.splice(index, 1);
            $('.entity-card[data-id="' + entityId + '"]').removeClass('selected');
            $('.entity-card[data-id="' + entityId + '"] .btn-select').text('Select').removeClass('selected');
        }
        
        updateSelectedEntitiesDisplay();
    };

    window.selectUBO = function(uboId) {
        var index = StructureWizard.selectedUBOs.indexOf(uboId);
        
        if (index === -1) {
            // Add UBO
            StructureWizard.selectedUBOs.push(uboId);
            $('.ubo-card[data-id="' + uboId + '"]').addClass('selected');
            $('.ubo-card[data-id="' + uboId + '"] .btn-select').text('Selected').addClass('selected');
        } else {
            // Remove UBO
            StructureWizard.selectedUBOs.splice(index, 1);
            $('.ubo-card[data-id="' + uboId + '"]').removeClass('selected');
            $('.ubo-card[data-id="' + uboId + '"] .btn-select').text('Select').removeClass('selected');
        }
        
        updateSelectedUBOsDisplay();
    };

    function updateSelectedEntitiesDisplay() {
        var $container = $('#selected-entities');
        $container.empty();
        
        if (StructureWizard.selectedEntities.length === 0) {
            $container.html('<div class="empty-state">No entities selected</div>');
            return;
        }
        
        StructureWizard.selectedEntities.forEach(function(entityId) {
            var entity = findEntityById(entityId);
            if (entity) {
                var $item = $('<div class="selected-item">' +
                    '<span class="selected-item-name">🏢 ' + entity.name + '</span>' +
                    '<button type="button" class="btn-remove" onclick="removeEntity(' + entityId + ')">×</button>' +
                '</div>');
                $container.append($item);
            }
        });
    }

    function updateSelectedUBOsDisplay() {
        var $container = $('#selected-ubos');
        $container.empty();
        
        if (StructureWizard.selectedUBOs.length === 0) {
            $container.html('<div class="empty-state">No UBOs selected</div>');
            return;
        }
        
        StructureWizard.selectedUBOs.forEach(function(uboId) {
            var ubo = findUBOById(uboId);
            if (ubo) {
                var $item = $('<div class="selected-item">' +
                    '<span class="selected-item-name">👤 ' + ubo.name + '</span>' +
                    '<button type="button" class="btn-remove" onclick="removeUBO(' + uboId + ')">×</button>' +
                '</div>');
                $container.append($item);
            }
        });
    }

    window.removeEntity = function(entityId) {
        selectEntity(entityId); // Toggle selection
    };

    window.removeUBO = function(uboId) {
        selectUBO(uboId); // Toggle selection
    };

    function findEntityById(entityId) {
        if (window.wizardData && window.wizardData.entities) {
            return window.wizardData.entities.find(function(entity) {
                return entity.id === entityId;
            });
        }
        return null;
    }

    function findUBOById(uboId) {
        if (window.wizardData && window.wizardData.parties) {
            return window.wizardData.parties.find(function(party) {
                return party.id === uboId;
            });
        }
        return null;
    }

    // ========================================================================
    // OWNERSHIP BUILDER
    // ========================================================================

    function initializeOwnershipBuilder() {
        // Initialize ownership table
        renderOwnershipTable();
    }

    window.addOwnership = function() {
        showOwnershipModal();
    };

    window.autoBalance = function() {
        // Auto-balance ownership percentages
        var entityGroups = {};
        
        // Group ownerships by entity
        StructureWizard.ownerships.forEach(function(ownership) {
            var entityId = ownership.owned_entity_id;
            if (!entityGroups[entityId]) {
                entityGroups[entityId] = [];
            }
            entityGroups[entityId].push(ownership);
        });
        
        // Balance each entity group
        Object.keys(entityGroups).forEach(function(entityId) {
            var ownerships = entityGroups[entityId];
            var equalPercentage = 100 / ownerships.length;
            
            ownerships.forEach(function(ownership) {
                ownership.percentage = parseFloat(equalPercentage.toFixed(2));
            });
        });
        
        // Re-render table
        renderOwnershipTable();
        updateOwnershipSummary();
        
        showMessage('Ownership percentages auto-balanced', 'success');
    };

    function showOwnershipModal() {
        populateOwnershipModalDropdowns();
        $('#ownership-modal').show();
    }

    window.closeOwnershipModal = function() {
        $('#ownership-modal').hide();
        $('#ownership-form')[0].reset();
    };

    window.saveOwnership = function() {
        var formData = getOwnershipFormData();
        
        if (validateOwnershipForm(formData)) {
            // Add to ownerships array
            var ownership = {
                id: Date.now(), // Temporary ID
                owned_entity_id: parseInt(formData.owned_entity),
                owned_entity_name: getEntityName(formData.owned_entity),
                percentage: parseFloat(formData.percentage),
                shares: formData.shares ? parseInt(formData.shares) : null,
                corporate_name: formData.corporate_name,
                hash_number: formData.hash_number,
                share_value_usd: formData.share_value_usd ? parseFloat(formData.share_value_usd) : null,
                share_value_eur: formData.share_value_eur ? parseFloat(formData.share_value_eur) : null
            };
            
            // Set owner
            var ownerParts = formData.owner.split('_');
            if (ownerParts[0] === 'ubo') {
                ownership.owner_ubo_id = parseInt(ownerParts[1]);
                ownership.owner_ubo_name = getUBOName(ownerParts[1]);
            } else if (ownerParts[0] === 'entity') {
                ownership.owner_entity_id = parseInt(ownerParts[1]);
                ownership.owner_entity_name = getEntityName(ownerParts[1]);
            }
            
            StructureWizard.ownerships.push(ownership);
            
            // Re-render table and summary
            renderOwnershipTable();
            updateOwnershipSummary();
            
            // Close modal
            closeOwnershipModal();
            
            showMessage('Ownership relationship added', 'success');
        }
    };

    function getOwnershipFormData() {
        return {
            owner: $('#modal-owner').val(),
            owned_entity: $('#modal-owned-entity').val(),
            percentage: $('#modal-percentage').val(),
            shares: $('#modal-shares').val(),
            corporate_name: $('#modal-corporate-name').val(),
            hash_number: $('#modal-hash-number').val(),
            share_value_usd: $('#modal-share-value-usd').val(),
            share_value_eur: $('#modal-share-value-eur').val()
        };
    }

    function validateOwnershipForm(formData) {
        var isValid = true;
        
        if (!formData.owner) {
            showMessage('Please select an owner', 'error');
            isValid = false;
        }
        
        if (!formData.owned_entity) {
            showMessage('Please select an owned entity', 'error');
            isValid = false;
        }
        
        if (!formData.percentage || formData.percentage <= 0 || formData.percentage > 100) {
            showMessage('Please enter a valid percentage (0-100)', 'error');
            isValid = false;
        }
        
        return isValid;
    }

    function populateOwnershipDropdowns() {
        populateOwnershipModalDropdowns();
    }

    function populateOwnershipModalDropdowns() {
        var $ownerSelect = $('#modal-owner');
        var $entitySelect = $('#modal-owned-entity');
        
        // Clear existing options
        $ownerSelect.empty().append('<option value="">Select owner...</option>');
        $entitySelect.empty().append('<option value="">Select entity...</option>');
        
        // Add UBOs as owners
        StructureWizard.selectedUBOs.forEach(function(uboId) {
            var ubo = findUBOById(uboId);
            if (ubo) {
                $ownerSelect.append('<option value="ubo_' + ubo.id + '">👤 ' + ubo.name + '</option>');
            }
        });
        
        // Add entities as owners
        StructureWizard.selectedEntities.forEach(function(entityId) {
            var entity = findEntityById(entityId);
            if (entity) {
                $ownerSelect.append('<option value="entity_' + entity.id + '">🏢 ' + entity.name + '</option>');
            }
        });
        
        // Add entities as owned entities
        StructureWizard.selectedEntities.forEach(function(entityId) {
            var entity = findEntityById(entityId);
            if (entity) {
                $entitySelect.append('<option value="' + entity.id + '">🏢 ' + entity.name + '</option>');
            }
        });
    }

    function renderOwnershipTable() {
        var $tbody = $('#ownership-tbody');
        $tbody.empty();
        
        if (StructureWizard.ownerships.length === 0) {
            $tbody.append(
                '<tr><td colspan="7" class="text-center">No ownership relationships defined</td></tr>'
            );
            return;
        }
        
        StructureWizard.ownerships.forEach(function(ownership, index) {
            var ownerName = ownership.owner_ubo_name || ownership.owner_entity_name || 'Unknown';
            var ownerIcon = ownership.owner_ubo_name ? '👤' : '🏢';
            
            var $row = $('<tr>' +
                '<td>' + ownerIcon + ' ' + ownerName + '</td>' +
                '<td>🏢 ' + ownership.owned_entity_name + '</td>' +
                '<td>' + (ownership.percentage || 0) + '%</td>' +
                '<td>' + (ownership.shares || '-') + '</td>' +
                '<td>' + (ownership.corporate_name || '-') + '</td>' +
                '<td>' + (ownership.hash_number || '-') + '</td>' +
                '<td>' +
                    '<button type="button" class="btn-remove-ownership" onclick="removeOwnership(' + index + ')">×</button>' +
                '</td>' +
            '</tr>');
            
            $tbody.append($row);
        });
    }

    window.removeOwnership = function(index) {
        if (confirm('Are you sure you want to remove this ownership relationship?')) {
            StructureWizard.ownerships.splice(index, 1);
            renderOwnershipTable();
            updateOwnershipSummary();
            showMessage('Ownership relationship removed', 'info');
        }
    };

    function updateOwnershipSummary() {
        var $container = $('#ownership-summary-content');
        $container.empty();
        
        if (StructureWizard.ownerships.length === 0) {
            $container.html('<div class="empty-state">No ownership relationships to summarize</div>');
            return;
        }
        
        // Group by entity
        var entitySummary = {};
        
        StructureWizard.ownerships.forEach(function(ownership) {
            var entityId = ownership.owned_entity_id;
            var entityName = ownership.owned_entity_name;
            
            if (!entitySummary[entityId]) {
                entitySummary[entityId] = {
                    name: entityName,
                    totalPercentage: 0,
                    ownerships: []
                };
            }
            
            entitySummary[entityId].totalPercentage += ownership.percentage || 0;
            entitySummary[entityId].ownerships.push(ownership);
        });
        
        // Render summary
        Object.keys(entitySummary).forEach(function(entityId) {
            var summary = entitySummary[entityId];
            var statusClass = 'incomplete';
            var statusIcon = '⚠️';
            
            if (summary.totalPercentage === 100) {
                statusClass = 'complete';
                statusIcon = '✅';
            } else if (summary.totalPercentage > 100) {
                statusClass = 'over';
                statusIcon = '❌';
            }
            
            var $item = $('<div class="summary-item">' +
                '<span class="summary-label">🏢 ' + summary.name + '</span>' +
                '<span class="summary-value ' + statusClass + '">' + statusIcon + ' ' + summary.totalPercentage.toFixed(1) + '%</span>' +
            '</div>');
            
            $container.append($item);
        });
    }

    function getEntityName(entityId) {
        var entity = findEntityById(parseInt(entityId));
        return entity ? entity.name : 'Unknown Entity';
    }

    function getUBOName(uboId) {
        var ubo = findUBOById(parseInt(uboId));
        return ubo ? ubo.name : 'Unknown UBO';
    }

    // ========================================================================
    // VALIDATION STEP
    // ========================================================================

    function runValidation() {
        if (!StructureWizard.structureId) {
            showValidationError('Structure must be saved before validation');
            return;
        }
        
        // Make AJAX call to validate
        $.ajax({
            url: '/admin/corporate/structure/' + StructureWizard.structureId + '/validate/',
            method: 'POST',
            headers: {
                'X-CSRFToken': window.wizardData.csrfToken
            },
            data: JSON.stringify({
                step: 4,
                structure_id: StructureWizard.structureId
            }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    StructureWizard.validationResults = response.validation;
                    StructureWizard.previewData = response.preview;
                    
                    displayValidationResults(response.validation);
                    displayStructurePreview(response.preview);
                } else {
                    showValidationError(response.error || 'Validation failed');
                }
            },
            error: function() {
                showValidationError('Failed to run validation');
            }
        });
    }

    function displayValidationResults(validation) {
        var $container = $('#validation-results');
        $container.empty();
        
        // Display errors
        if (validation.errors && validation.errors.length > 0) {
            validation.errors.forEach(function(error) {
                $container.append(
                    '<div class="validation-result error">❌ ' + error + '</div>'
                );
            });
        }
        
        // Display warnings
        if (validation.warnings && validation.warnings.length > 0) {
            validation.warnings.forEach(function(warning) {
                $container.append(
                    '<div class="validation-result warning">⚠️ ' + warning + '</div>'
                );
            });
        }
        
        // Display info
        if (validation.info && validation.info.length > 0) {
            validation.info.forEach(function(info) {
                $container.append(
                    '<div class="validation-result info">ℹ️ ' + info + '</div>'
                );
            });
        }
        
        // Display success if no issues
        if ((!validation.errors || validation.errors.length === 0) &&
            (!validation.warnings || validation.warnings.length === 0)) {
            $container.append(
                '<div class="validation-result success">✅ All validations passed successfully!</div>'
            );
        }
    }

    function displayStructurePreview(preview) {
        var $container = $('#structure-preview');
        $container.empty();
        
        if (!preview) {
            $container.html('<div class="empty-state">No preview data available</div>');
            return;
        }
        
        // Structure info
        $container.append(
            '<div class="preview-section">' +
                '<h4>📋 Structure Information</h4>' +
                '<p><strong>Name:</strong> ' + preview.name + '</p>' +
                '<p><strong>Status:</strong> ' + preview.status + '</p>' +
                '<p><strong>Description:</strong> ' + (preview.description || 'No description') + '</p>' +
            '</div>'
        );
        
        // Summary
        if (preview.summary) {
            $container.append(
                '<div class="preview-section">' +
                    '<h4>📊 Summary</h4>' +
                    '<p><strong>Total Entities:</strong> ' + preview.summary.total_entities + '</p>' +
                    '<p><strong>Total Ownerships:</strong> ' + preview.summary.total_ownerships + '</p>' +
                    '<p><strong>Complete Entities:</strong> ' + preview.summary.complete_entities + '</p>' +
                    '<p><strong>Incomplete Entities:</strong> ' + preview.summary.incomplete_entities + '</p>' +
                '</div>'
            );
        }
        
        // Entities
        if (preview.entities && preview.entities.length > 0) {
            var entitiesHtml = '<div class="preview-section"><h4>🏢 Entities</h4><ul>';
            preview.entities.forEach(function(entity) {
                entitiesHtml += '<li>' + entity.name + ' (' + entity.type + ') - ' + entity.total_ownership + '%</li>';
            });
            entitiesHtml += '</ul></div>';
            $container.append(entitiesHtml);
        }
    }

    function showValidationError(message) {
        $('#validation-results').html(
            '<div class="validation-result error">❌ ' + message + '</div>'
        );
    }

    // ========================================================================
    // SAVE STEP
    // ========================================================================

    function generateFinalSummary() {
        var $container = $('#final-summary-content');
        $container.empty();
        
        // Structure info
        $container.append(
            '<div class="summary-section">' +
                '<h4>📋 Structure Details</h4>' +
                '<p><strong>Name:</strong> ' + $('#structure-name').val() + '</p>' +
                '<p><strong>Status:</strong> ' + $('#structure-status option:selected').text() + '</p>' +
                '<p><strong>Description:</strong> ' + ($('#structure-description').val() || 'No description') + '</p>' +
            '</div>'
        );
        
        // Entities and UBOs
        $container.append(
            '<div class="summary-section">' +
                '<h4>🏢 Components</h4>' +
                '<p><strong>Selected Entities:</strong> ' + StructureWizard.selectedEntities.length + '</p>' +
                '<p><strong>Selected UBOs:</strong> ' + StructureWizard.selectedUBOs.length + '</p>' +
                '<p><strong>Ownership Relationships:</strong> ' + StructureWizard.ownerships.length + '</p>' +
            '</div>'
        );
        
        // Validation status
        if (StructureWizard.validationResults) {
            var hasErrors = StructureWizard.validationResults.errors && StructureWizard.validationResults.errors.length > 0;
            var hasWarnings = StructureWizard.validationResults.warnings && StructureWizard.validationResults.warnings.length > 0;
            
            var statusIcon = hasErrors ? '❌' : (hasWarnings ? '⚠️' : '✅');
            var statusText = hasErrors ? 'Has Errors' : (hasWarnings ? 'Has Warnings' : 'Valid');
            
            $container.append(
                '<div class="summary-section">' +
                    '<h4>✅ Validation Status</h4>' +
                    '<p><strong>Status:</strong> ' + statusIcon + ' ' + statusText + '</p>' +
                '</div>'
            );
        }
    }

    window.saveStructure = function() {
        var approve = $('#approve-structure').is(':checked');
        var generateDocs = $('#generate-docs').is(':checked');
        
        showLoading('Saving structure...');
        
        $.ajax({
            url: '/admin/corporate/structure/save-step/',
            method: 'POST',
            headers: {
                'X-CSRFToken': window.wizardData.csrfToken
            },
            data: JSON.stringify({
                step: 5,
                structure_id: StructureWizard.structureId,
                approve: approve,
                generate_docs: generateDocs
            }),
            contentType: 'application/json',
            success: function(response) {
                hideLoading();
                
                if (response.success) {
                    showMessage('Structure saved successfully!', 'success');
                    
                    // Redirect after a short delay
                    setTimeout(function() {
                        if (response.redirect_url) {
                            window.location.href = response.redirect_url;
                        } else {
                            window.location.href = '/admin/corporate/structure/';
                        }
                    }, 2000);
                } else {
                    showMessage(response.error || 'Failed to save structure', 'error');
                }
            },
            error: function() {
                hideLoading();
                showMessage('Failed to save structure', 'error');
            }
        });
    };

    // ========================================================================
    // STEP SAVING
    // ========================================================================

    function saveCurrentStep() {
        return new Promise(function(resolve, reject) {
            var stepData = getStepData(StructureWizard.currentStep);
            
            if (!stepData) {
                resolve();
                return;
            }
            
            showLoading('Saving step data...');
            
            $.ajax({
                url: '/admin/corporate/structure/save-step/',
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.wizardData.csrfToken
                },
                data: JSON.stringify(stepData),
                contentType: 'application/json',
                success: function(response) {
                    hideLoading();
                    
                    if (response.success) {
                        if (response.structure_id) {
                            StructureWizard.structureId = response.structure_id;
                        }
                        resolve(response);
                    } else {
                        showMessage(response.error || 'Failed to save step', 'error');
                        reject(response);
                    }
                },
                error: function() {
                    hideLoading();
                    showMessage('Failed to save step data', 'error');
                    reject();
                }
            });
        });
    }

    function getStepData(stepNumber) {
        switch (stepNumber) {
            case 1:
                return {
                    step: 1,
                    structure_id: StructureWizard.structureId,
                    name: $('#structure-name').val().trim(),
                    description: $('#structure-description').val().trim(),
                    status: $('#structure-status').val()
                };
            
            case 2:
                return {
                    step: 2,
                    structure_id: StructureWizard.structureId,
                    selected_entities: StructureWizard.selectedEntities,
                    selected_ubos: StructureWizard.selectedUBOs
                };
            
            case 3:
                return {
                    step: 3,
                    structure_id: StructureWizard.structureId,
                    ownerships: StructureWizard.ownerships
                };
            
            default:
                return null;
        }
    }

    // ========================================================================
    // UTILITY FUNCTIONS
    // ========================================================================

    function showLoading(message) {
        $('#loading-overlay .loading-text').text(message || 'Loading...');
        $('#loading-overlay').show();
    }

    function hideLoading() {
        $('#loading-overlay').hide();
    }

    function showMessage(message, type) {
        type = type || 'info';
        
        var icons = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        };
        
        // Remove existing messages
        $('.wizard-message').remove();
        
        var $message = $('<div class="wizard-message wizard-message-' + type + '">' +
            '<span class="message-icon">' + icons[type] + '</span>' +
            '<span class="message-text">' + message + '</span>' +
            '<button type="button" class="message-close" onclick="$(this).parent().remove()">×</button>' +
        '</div>');
        
        $('.wizard-header').after($message);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            $message.fadeOut(300, function() {
                $(this).remove();
            });
        }, 5000);
    }

    // Add message styles
    var messageStyles = `
        <style>
            .wizard-message {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 12px 20px;
                margin: 10px 0;
                border-radius: 8px;
                font-weight: 500;
                animation: slideDown 0.3s ease;
            }
            
            .wizard-message-success {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .wizard-message-error {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .wizard-message-warning {
                background-color: #fff3cd;
                color: #856404;
                border: 1px solid #ffeaa7;
            }
            
            .wizard-message-info {
                background-color: #d1ecf1;
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
            
            .message-close {
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                margin-left: auto;
                opacity: 0.7;
            }
            
            .message-close:hover {
                opacity: 1;
            }
            
            @keyframes slideDown {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    `;
    
    $('head').append(messageStyles);

})();

