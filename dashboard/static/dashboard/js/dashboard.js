// SIRIUS Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard functionality
    initializeDashboard();
});

function initializeDashboard() {
    // Add loading states to action buttons
    setupActionButtons();
    
    // Setup auto-refresh functionality
    setupAutoRefresh();
    
    // Setup tooltips
    setupTooltips();
    
    // Setup confirmation dialogs
    setupConfirmations();
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
}

function setupActionButtons() {
    const actionButtons = document.querySelectorAll('form button[type="submit"]');
    
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            this.disabled = true;
            
            // Re-enable button after 5 seconds as fallback
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 5000);
        });
    });
}

function setupAutoRefresh() {
    // Auto-refresh stats every 2 minutes
    setInterval(refreshStats, 120000);
    
    // Auto-refresh recent activity every 5 minutes
    setInterval(refreshRecentActivity, 300000);
    
    // Add manual refresh button
    addRefreshButton();
}

function refreshStats() {
    fetch('/admin/dashboard/api/?type=stats')
        .then(response => response.json())
        .then(data => {
            updateStatsDisplay(data);
        })
        .catch(error => {
            console.error('Error refreshing stats:', error);
        });
}

function updateStatsDisplay(stats) {
    // Update stat cards
    const statCards = document.querySelectorAll('.stat-card');
    
    if (statCards.length >= 4) {
        statCards[0].querySelector('h3').textContent = stats.pending_requests;
        statCards[1].querySelector('h3').textContent = stats.in_progress;
        statCards[2].querySelector('h3').textContent = stats.pending_approval;
        statCards[3].querySelector('h3').textContent = stats.completed_this_month;
    }
    
    // Add visual feedback for updates
    statCards.forEach(card => {
        card.style.transform = 'scale(1.02)';
        setTimeout(() => {
            card.style.transform = 'scale(1)';
        }, 200);
    });
}

function refreshRecentActivity() {
    fetch('/admin/dashboard/api/?type=recent_activity')
        .then(response => response.json())
        .then(data => {
            updateActivityDisplay(data.activities);
        })
        .catch(error => {
            console.error('Error refreshing activity:', error);
        });
}

function updateActivityDisplay(activities) {
    const activityTimeline = document.querySelector('.activity-timeline');
    if (!activityTimeline) return;
    
    // Clear existing activities
    activityTimeline.innerHTML = '';
    
    if (activities.length === 0) {
        activityTimeline.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-history"></i>
                <p>No recent activity</p>
            </div>
        `;
        return;
    }
    
    // Add new activities
    activities.forEach(activity => {
        const activityItem = createActivityItem(activity);
        activityTimeline.appendChild(activityItem);
    });
}

function createActivityItem(activity) {
    const item = document.createElement('div');
    item.className = 'activity-item';
    
    item.innerHTML = `
        <div class="activity-icon ${activity.color}">
            <i class="${activity.icon}"></i>
        </div>
        <div class="activity-content">
            <h5>${activity.title}</h5>
            <p>${activity.description}</p>
            <small class="text-muted">
                <i class="fas fa-clock"></i> ${formatTimestamp(activity.timestamp)}
            </small>
        </div>
        <div class="activity-action">
            <a href="${activity.url}" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-external-link-alt"></i>
            </a>
        </div>
    `;
    
    return item;
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minutes ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    if (diffDays < 7) return `${diffDays} days ago`;
    
    return date.toLocaleDateString();
}

function addRefreshButton() {
    const dashboardContainer = document.querySelector('.dashboard-container');
    if (!dashboardContainer) return;
    
    const refreshButton = document.createElement('button');
    refreshButton.className = 'btn btn-outline-secondary btn-sm';
    refreshButton.style.position = 'fixed';
    refreshButton.style.top = '20px';
    refreshButton.style.right = '20px';
    refreshButton.style.zIndex = '1000';
    refreshButton.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
    
    refreshButton.addEventListener('click', function() {
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
        this.disabled = true;
        
        // Refresh all data
        Promise.all([
            refreshStats(),
            refreshRecentActivity()
        ]).finally(() => {
            this.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
            this.disabled = false;
        });
    });
    
    document.body.appendChild(refreshButton);
}

function setupTooltips() {
    // Add tooltips to action buttons
    const buttons = document.querySelectorAll('[data-toggle="tooltip"]');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', showTooltip);
        button.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = event.target.getAttribute('title') || event.target.getAttribute('data-title');
    
    if (!tooltip.textContent) return;
    
    tooltip.style.position = 'absolute';
    tooltip.style.background = '#333';
    tooltip.style.color = 'white';
    tooltip.style.padding = '5px 10px';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '12px';
    tooltip.style.zIndex = '1001';
    tooltip.style.pointerEvents = 'none';
    
    document.body.appendChild(tooltip);
    
    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    event.target._tooltip = tooltip;
}

function hideTooltip(event) {
    if (event.target._tooltip) {
        document.body.removeChild(event.target._tooltip);
        delete event.target._tooltip;
    }
}

function setupConfirmations() {
    // Add confirmation dialogs for destructive actions
    const destructiveActions = document.querySelectorAll('button[data-confirm]');
    
    destructiveActions.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + R: Refresh dashboard
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            location.reload();
        }
        
        // Ctrl/Cmd + D: Focus on dashboard (if multiple tabs)
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            window.focus();
        }
        
        // Escape: Close any open modals or dialogs
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                modal.style.display = 'none';
            });
        }
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '1002';
    notification.style.minWidth = '300px';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

function animateCounter(element, start, end, duration = 1000) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

// Initialize counters animation on page load
document.addEventListener('DOMContentLoaded', function() {
    const statNumbers = document.querySelectorAll('.stat-content h3');
    statNumbers.forEach(element => {
        const finalValue = parseInt(element.textContent);
        element.textContent = '0';
        animateCounter(element, 0, finalValue, 1500);
    });
});

// Handle form submissions with better UX
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.tagName === 'FORM') {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            submitButton.disabled = true;
            
            // Show loading overlay for the parent container
            const container = form.closest('.request-item, .structure-item, .approval-item');
            if (container) {
                container.style.opacity = '0.7';
                container.style.pointerEvents = 'none';
            }
        }
    }
});

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Performance monitoring
let performanceMetrics = {
    pageLoadTime: 0,
    apiCalls: 0,
    errors: 0
};

window.addEventListener('load', function() {
    performanceMetrics.pageLoadTime = performance.now();
});

// Error tracking
window.addEventListener('error', function(e) {
    performanceMetrics.errors++;
    console.error('Dashboard error:', e.error);
});

// Export for debugging
window.dashboardMetrics = performanceMetrics;

