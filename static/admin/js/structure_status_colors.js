// Structure Status Colors JavaScript - FASE 8

document.addEventListener('DOMContentLoaded', function() {
    // Apply colors to Structure list view
    applyStructureStatusColors();
    
    // Apply colors to Structure change form
    applyStructureFormColors();
});

function applyStructureStatusColors() {
    // Find all rows in the admin list view
    const rows = document.querySelectorAll('.results tbody tr');
    
    rows.forEach(row => {
        // Look for status field in the row
        const statusCell = row.querySelector('.field-status');
        
        if (statusCell) {
            const status = statusCell.textContent.trim();
            
            // Remove any existing status classes
            row.classList.remove('structure-drafting', 'structure-sent-approval', 'structure-approved');
            
            // Apply appropriate class based on status
            switch(status) {
                case 'Drafting':
                    row.classList.add('structure-drafting');
                    break;
                case 'Sent for Approval':
                    row.classList.add('structure-sent-approval');
                    break;
                case 'Approved':
                    row.classList.add('structure-approved');
                    break;
            }
        }
    });
}

function applyStructureFormColors() {
    // Apply colors to the change form based on current status
    const statusField = document.querySelector('#id_status');
    
    if (statusField) {
        const currentStatus = statusField.value;
        const formContainer = document.querySelector('.form-row');
        
        if (formContainer) {
            // Remove existing classes
            formContainer.classList.remove('structure-drafting', 'structure-sent-approval', 'structure-approved');
            
            // Apply class based on current status
            switch(currentStatus) {
                case 'DRAFTING':
                    formContainer.classList.add('structure-drafting');
                    break;
                case 'SENT_FOR_APPROVAL':
                    formContainer.classList.add('structure-sent-approval');
                    break;
                case 'APPROVED':
                    formContainer.classList.add('structure-approved');
                    break;
            }
        }
        
        // Add event listener for status changes
        statusField.addEventListener('change', function() {
            applyStructureFormColors();
        });
    }
}

// Function to show warning when changing from approved status
function showStatusChangeWarning() {
    const statusField = document.querySelector('#id_status');
    
    if (statusField) {
        const originalStatus = statusField.getAttribute('data-original-value') || statusField.value;
        
        statusField.addEventListener('change', function() {
            if (originalStatus === 'APPROVED' && this.value !== 'APPROVED') {
                const confirmed = confirm(
                    'Warning: You are changing the status of an approved structure. ' +
                    'This action may require additional approvals. Continue?'
                );
                
                if (!confirmed) {
                    this.value = originalStatus;
                    applyStructureFormColors();
                }
            }
        });
        
        // Store original value
        statusField.setAttribute('data-original-value', statusField.value);
    }
}

// Initialize warning system
document.addEventListener('DOMContentLoaded', function() {
    showStatusChangeWarning();
});

