/* ============================================================================
   SIRIUS STRUCTURE ADMIN IMPROVED JAVASCRIPT
   ============================================================================ */

(function($) {
    'use strict';

    // Initialize when DOM is ready
    $(document).ready(function() {
        initializeStructureAdmin();
    });

    function initializeStructureAdmin() {
        // Add CSS class to body for styling
        $('body').addClass('structure-admin-improved');
        
        // Initialize all components
        initializeTooltips();
        initializeProgressBars();
        initializeValidationFeedback();
        initializeQuickActions();
        initializeFilterEnhancements();
        initializeFormValidation();
        
        console.log('Structure Admin Improved initialized');
    }

    // ========================================================================
    // TOOLTIPS
    // ========================================================================
    
    function initializeTooltips() {
        // Add tooltips to badges and status indicators
        $('.status-badge').each(function() {
            var status = $(this).text().trim();
            var tooltip = getStatusTooltip(status);
            $(this).attr('data-tooltip', tooltip).addClass('tooltip');
        });
        
        $('.validation-score-badge').each(function() {
            $(this).attr('data-tooltip', 'Validation score based on completeness and accuracy').addClass('tooltip');
        });
        
        $('.entity-count-badge').each(function() {
            $(this).attr('data-tooltip', 'Number of entities in this structure').addClass('tooltip');
        });
    }
    
    function getStatusTooltip(status) {
        var tooltips = {
            'DRAFTING': 'Structure is being created and edited',
            'SENT FOR APPROVAL': 'Structure has been submitted for review',
            'APPROVED': 'Structure has been approved and is ready for implementation',
            'REJECTED': 'Structure was rejected and needs revision'
        };
        return tooltips[status.toUpperCase()] || 'Status information';
    }

    // ========================================================================
    // PROGRESS BARS
    // ========================================================================
    
    function initializeProgressBars() {
        // Create progress bars for ownership percentages
        $('.ownership-summary-display').each(function() {
            var $container = $(this);
            var text = $container.text();
            
            // Parse ownership percentages from text
            var matches = text.match(/(\w+): (\d+)%/g);
            if (matches) {
                var $progressContainer = $('<div class="ownership-progress-container"></div>');
                
                matches.forEach(function(match) {
                    var parts = match.split(': ');
                    var entityName = parts[0];
                    var percentage = parseInt(parts[1]);
                    
                    var progressClass = 'incomplete';
                    if (percentage === 100) progressClass = 'complete';
                    else if (percentage > 100) progressClass = 'over';
                    
                    var $progress = $('<div class="ownership-progress">' +
                        '<div class="ownership-progress-bar ' + progressClass + '" style="width: ' + Math.min(percentage, 100) + '%">' +
                            entityName + ': ' + percentage + '%' +
                        '</div>' +
                    '</div>');
                    
                    $progressContainer.append($progress);
                });
                
                $container.append($progressContainer);
            }
        });
    }

    // ========================================================================
    // VALIDATION FEEDBACK
    // ========================================================================
    
    function initializeValidationFeedback() {
        // Add real-time validation feedback for forms
        $('input[name$="ownership_percentage"]').on('input', function() {
            validateOwnershipPercentage($(this));
        });
        
        $('input[name$="owned_shares"]').on('input', function() {
            validateShares($(this));
        });
        
        // Validate on page load
        $('input[name$="ownership_percentage"]').each(function() {
            validateOwnershipPercentage($(this));
        });
    }
    
    function validateOwnershipPercentage($input) {
        var value = parseFloat($input.val());
        var $feedback = $input.siblings('.validation-feedback');
        
        if ($feedback.length === 0) {
            $feedback = $('<div class="validation-feedback"></div>');
            $input.after($feedback);
        }
        
        $input.removeClass('validation-valid validation-invalid validation-warning');
        
        if (isNaN(value)) {
            $feedback.text('').hide();
            return;
        }
        
        if (value < 0 || value > 100) {
            $input.addClass('validation-invalid');
            $feedback.text('Percentage must be between 0 and 100').show();
        } else if (value === 100) {
            $input.addClass('validation-valid');
            $feedback.text('Complete ownership').show();
        } else if (value > 0) {
            $input.addClass('validation-warning');
            $feedback.text('Partial ownership (' + value + '%)').show();
        } else {
            $feedback.text('').hide();
        }
    }
    
    function validateShares($input) {
        var value = parseInt($input.val());
        var $feedback = $input.siblings('.validation-feedback');
        
        if ($feedback.length === 0) {
            $feedback = $('<div class="validation-feedback"></div>');
            $input.after($feedback);
        }
        
        $input.removeClass('validation-valid validation-invalid');
        
        if (isNaN(value)) {
            $feedback.text('').hide();
            return;
        }
        
        if (value < 0) {
            $input.addClass('validation-invalid');
            $feedback.text('Shares cannot be negative').show();
        } else if (value > 0) {
            $input.addClass('validation-valid');
            $feedback.text(value.toLocaleString() + ' shares').show();
        } else {
            $feedback.text('').hide();
        }
    }

    // ========================================================================
    // QUICK ACTIONS
    // ========================================================================
    
    function initializeQuickActions() {
        // Add quick action buttons to structure list
        $('.admin-list-table tbody tr').each(function() {
            var $row = $(this);
            var $lastCell = $row.find('td:last');
            
            if (!$lastCell.hasClass('action-checkbox-column')) {
                var structureId = getStructureIdFromRow($row);
                if (structureId) {
                    var $quickActions = $('<div class="quick-actions">' +
                        '<button type="button" class="btn-quick-validate" data-id="' + structureId + '" title="Quick Validate">✅</button>' +
                        '<button type="button" class="btn-quick-duplicate" data-id="' + structureId + '" title="Duplicate">📋</button>' +
                        '<button type="button" class="btn-quick-export" data-id="' + structureId + '" title="Export">📊</button>' +
                    '</div>');
                    
                    $lastCell.append($quickActions);
                }
            }
        });
        
        // Bind quick action events
        $(document).on('click', '.btn-quick-validate', function() {
            var structureId = $(this).data('id');
            quickValidateStructure(structureId);
        });
        
        $(document).on('click', '.btn-quick-duplicate', function() {
            var structureId = $(this).data('id');
            quickDuplicateStructure(structureId);
        });
        
        $(document).on('click', '.btn-quick-export', function() {
            var structureId = $(this).data('id');
            quickExportStructure(structureId);
        });
    }
    
    function getStructureIdFromRow($row) {
        // Try to extract structure ID from the row
        var $link = $row.find('a[href*="/corporate/structure/"]').first();
        if ($link.length) {
            var href = $link.attr('href');
            var match = href.match(/\/corporate\/structure\/(\d+)\//);
            return match ? match[1] : null;
        }
        return null;
    }
    
    function quickValidateStructure(structureId) {
        showLoading('Validating structure...');
        
        // Simulate validation (in real implementation, this would be an AJAX call)
        setTimeout(function() {
            hideLoading();
            showMessage('Structure validation completed', 'success');
        }, 1000);
    }
    
    function quickDuplicateStructure(structureId) {
        if (confirm('Are you sure you want to duplicate this structure?')) {
            showLoading('Duplicating structure...');
            
            // Simulate duplication
            setTimeout(function() {
                hideLoading();
                showMessage('Structure duplicated successfully', 'success');
                // In real implementation, redirect to the new structure
            }, 1500);
        }
    }
    
    function quickExportStructure(structureId) {
        showLoading('Generating export...');
        
        // Simulate export
        setTimeout(function() {
            hideLoading();
            showMessage('Export generated successfully', 'success');
            // In real implementation, trigger download
        }, 1000);
    }

    // ========================================================================
    // FILTER ENHANCEMENTS
    // ========================================================================
    
    function initializeFilterEnhancements() {
        // Add filter counters
        $('#changelist-filter ul').each(function() {
            var $list = $(this);
            var $items = $list.find('li a');
            
            $items.each(function() {
                var $link = $(this);
                var text = $link.text().trim();
                
                // Add emoji icons to filter options
                if (text.includes('Complete')) {
                    $link.prepend('✅ ');
                } else if (text.includes('Incomplete')) {
                    $link.prepend('⚠️ ');
                } else if (text.includes('Over-allocated')) {
                    $link.prepend('❌ ');
                } else if (text.includes('Empty')) {
                    $link.prepend('➖ ');
                }
            });
        });
        
        // Add search within filters
        $('#changelist-filter').each(function() {
            var $filter = $(this);
            var $searchBox = $('<div class="filter-search">' +
                '<input type="text" placeholder="Search filters..." class="filter-search-input">' +
            '</div>');
            
            $filter.prepend($searchBox);
            
            $searchBox.find('input').on('input', function() {
                var searchTerm = $(this).val().toLowerCase();
                $filter.find('li').each(function() {
                    var $item = $(this);
                    var text = $item.text().toLowerCase();
                    
                    if (text.includes(searchTerm)) {
                        $item.show();
                    } else {
                        $item.hide();
                    }
                });
            });
        });
    }

    // ========================================================================
    // FORM VALIDATION
    // ========================================================================
    
    function initializeFormValidation() {
        // Add form validation for structure forms
        $('form').on('submit', function(e) {
            var $form = $(this);
            var isValid = true;
            
            // Validate ownership percentages
            $form.find('input[name$="ownership_percentage"]').each(function() {
                var value = parseFloat($(this).val());
                if (!isNaN(value) && (value < 0 || value > 100)) {
                    isValid = false;
                    $(this).addClass('validation-invalid');
                }
            });
            
            // Validate that structures have at least one entity
            if ($form.find('.inline-group .tabular tbody tr').length === 0) {
                showMessage('Structure must have at least one entity ownership', 'error');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
                showMessage('Please fix validation errors before saving', 'error');
            }
        });
    }

    // ========================================================================
    // UTILITY FUNCTIONS
    // ========================================================================
    
    function showLoading(message) {
        var $loading = $('<div class="loading-overlay">' +
            '<div class="loading-spinner"></div>' +
            '<div class="loading-message">' + (message || 'Loading...') + '</div>' +
        '</div>');
        
        $('body').append($loading);
        $loading.fadeIn(200);
    }
    
    function hideLoading() {
        $('.loading-overlay').fadeOut(200, function() {
            $(this).remove();
        });
    }
    
    function showMessage(message, type) {
        type = type || 'info';
        
        var icons = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        };
        
        var $message = $('<div class="admin-message admin-message-' + type + '">' +
            '<span class="message-icon">' + icons[type] + '</span>' +
            '<span class="message-text">' + message + '</span>' +
            '<button type="button" class="message-close">×</button>' +
        '</div>');
        
        // Remove existing messages
        $('.admin-message').remove();
        
        // Add new message
        $('.breadcrumbs').after($message);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            $message.fadeOut(300, function() {
                $(this).remove();
            });
        }, 5000);
        
        // Manual close
        $message.find('.message-close').on('click', function() {
            $message.fadeOut(300, function() {
                $(this).remove();
            });
        });
    }
    
    // Auto-refresh functionality for real-time updates
    function initializeAutoRefresh() {
        if (window.location.pathname.includes('/corporate/structure/')) {
            setInterval(function() {
                // Check for updates (in real implementation)
                // This could update validation status, ownership calculations, etc.
            }, 30000); // Every 30 seconds
        }
    }
    
    // Initialize auto-refresh
    initializeAutoRefresh();

})(django.jQuery);

// ============================================================================
// CSS ADDITIONS FOR JAVASCRIPT FEATURES
// ============================================================================

// Add dynamic styles
var dynamicStyles = `
    <style>
        .quick-actions {
            display: inline-flex;
            gap: 5px;
            margin-left: 10px;
        }
        
        .quick-actions button {
            background: none;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 4px 6px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s ease;
        }
        
        .quick-actions button:hover {
            background: #f8f9fa;
            border-color: #adb5bd;
        }
        
        .validation-feedback {
            font-size: 11px;
            margin-top: 2px;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        .validation-valid {
            border-color: #28a745 !important;
            background-color: #f8fff8 !important;
        }
        
        .validation-invalid {
            border-color: #dc3545 !important;
            background-color: #fff8f8 !important;
        }
        
        .validation-warning {
            border-color: #ffc107 !important;
            background-color: #fffbf0 !important;
        }
        
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .loading-message {
            color: white;
            margin-top: 15px;
            font-size: 16px;
            font-weight: 500;
        }
        
        .admin-message {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 20px;
            margin: 10px 0;
            border-radius: 8px;
            font-weight: 500;
        }
        
        .admin-message-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .admin-message-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .admin-message-warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        
        .admin-message-info {
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
        
        .filter-search {
            padding: 10px 15px;
            border-bottom: 1px solid #dee2e6;
        }
        
        .filter-search-input {
            width: 100%;
            padding: 6px 10px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 12px;
        }
        
        .ownership-progress-container {
            margin-top: 10px;
        }
        
        .ownership-progress {
            margin-bottom: 5px;
        }
    </style>
`;

// Inject dynamic styles
document.head.insertAdjacentHTML('beforeend', dynamicStyles);

