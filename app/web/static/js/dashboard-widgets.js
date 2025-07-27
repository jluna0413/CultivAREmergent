/**
 * Dashboard Widget System
 * Handles customizable widgets, drag-and-drop, and mobile responsiveness
 */

class DashboardWidgetSystem {
    constructor() {
        this.widgets = [];
        this.isDragging = false;
        this.draggedElement = null;
        this.touchStartPos = { x: 0, y: 0 };
        this.widgetConfig = this.loadWidgetConfig();
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadWidgets();
        this.setupDragAndDrop();
        this.setupMobileHandlers();
    }

    // Load widget configuration from localStorage
    loadWidgetConfig() {
        const saved = localStorage.getItem('dashboard-widgets');
        return saved ? JSON.parse(saved) : this.getDefaultConfig();
    }

    // Save widget configuration to localStorage
    saveWidgetConfig() {
        localStorage.setItem('dashboard-widgets', JSON.stringify(this.widgetConfig));
    }

    // Default widget configuration
    getDefaultConfig() {
        return {
            widgets: [
                { id: 'plants', enabled: true, order: 1, size: 'large' },
                { id: 'strains', enabled: true, order: 2, size: 'medium' },
                { id: 'sensors', enabled: true, order: 3, size: 'medium' },
                { id: 'harvests', enabled: true, order: 4, size: 'medium' },
                { id: 'timeline', enabled: true, order: 5, size: 'large' },
                { id: 'quick-actions', enabled: true, order: 6, size: 'small' },
                { id: 'environmental', enabled: true, order: 7, size: 'large' }
            ]
        };
    }

    // Setup event listeners
    setupEventListeners() {
        // Widget customization toggle
        document.addEventListener('click', (e) => {
            if (e.target.matches('.widget-settings-btn')) {
                this.toggleWidgetSettings();
            }
            
            if (e.target.matches('.widget-toggle')) {
                this.toggleWidget(e.target.dataset.widgetId);
            }
        });

        // Window resize handler
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    // Load and render widgets
    loadWidgets() {
        const container = document.querySelector('.dashboard-widgets');
        if (!container) return;

        // Sort widgets by order
        const sortedWidgets = this.widgetConfig.widgets
            .filter(w => w.enabled)
            .sort((a, b) => a.order - b.order);

        // Clear container
        container.innerHTML = '';

        // Render each widget
        sortedWidgets.forEach(widget => {
            const widgetElement = this.createWidgetElement(widget);
            container.appendChild(widgetElement);
        });
    }

    // Create widget element
    createWidgetElement(widget) {
        const element = document.createElement('div');
        element.className = `dashboard-widget widget-${widget.size} widget-${widget.id}`;
        element.dataset.widgetId = widget.id;
        element.innerHTML = this.getWidgetContent(widget);
        
        // Add drag handle
        const dragHandle = document.createElement('div');
        dragHandle.className = 'widget-drag-handle';
        dragHandle.innerHTML = '<i class="fas fa-grip-vertical"></i>';
        element.appendChild(dragHandle);
        
        return element;
    }

    // Get widget content based on type
    getWidgetContent(widget) {
        switch(widget.id) {
            case 'plants':
                return this.getActivePlantsWidget();
            case 'strains':
                return this.getStrainsWidget();
            case 'sensors':
                return this.getSensorsWidget();
            case 'harvests':
                return this.getHarvestsWidget();
            case 'timeline':
                return this.getTimelineWidget();
            case 'quick-actions':
                return this.getQuickActionsWidget();
            case 'environmental':
                return this.getEnvironmentalWidget();
            default:
                return '<div class="widget-content">Unknown widget</div>';
        }
    }

    // Active Plants Widget
    getActivePlantsWidget() {
        return `
            <div class="widget-header">
                <h4><i class="fas fa-seedling"></i> Active Plants</h4>
                <button class="btn btn-sm btn-primary widget-expand-btn">
                    <i class="fas fa-expand"></i>
                </button>
            </div>
            <div class="widget-content">
                <div class="widget-stat">
                    <div class="stat-number" id="plants-count">0</div>
                    <div class="stat-label">Total Plants</div>
                </div>
                <div class="plant-list" id="recent-plants">
                    <!-- Plants will be loaded here -->
                </div>
            </div>
        `;
    }

    // Plant Timeline Widget
    getTimelineWidget() {
        return `
            <div class="widget-header">
                <h4><i class="fas fa-history"></i> Plant Timeline</h4>
                <div class="timeline-controls">
                    <button class="btn btn-sm btn-outline-secondary" id="timeline-prev">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <span id="timeline-period">This Week</span>
                    <button class="btn btn-sm btn-outline-secondary" id="timeline-next">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
            <div class="widget-content">
                <div class="timeline-container" id="plant-timeline">
                    <!-- Timeline will be loaded here -->
                </div>
            </div>
        `;
    }

    // Quick Actions Widget
    getQuickActionsWidget() {
        return `
            <div class="widget-header">
                <h4><i class="fas fa-bolt"></i> Quick Actions</h4>
            </div>
            <div class="widget-content">
                <div class="quick-actions-grid">
                    <button class="quick-action-btn" data-action="add-plant">
                        <i class="fas fa-plus"></i>
                        <span>Add Plant</span>
                    </button>
                    <button class="quick-action-btn" data-action="water-all">
                        <i class="fas fa-tint"></i>
                        <span>Water All</span>
                    </button>
                    <button class="quick-action-btn" data-action="record-activity">
                        <i class="fas fa-clipboard"></i>
                        <span>Log Activity</span>
                    </button>
                    <button class="quick-action-btn" data-action="check-sensors">
                        <i class="fas fa-thermometer"></i>
                        <span>Check Sensors</span>
                    </button>
                </div>
            </div>
        `;
    }

    // Environmental Widget
    getEnvironmentalWidget() {
        return `
            <div class="widget-header">
                <h4><i class="fas fa-leaf"></i> Environment</h4>
                <button class="btn btn-sm btn-outline-secondary widget-refresh-btn" data-widget="environmental">
                    <i class="fas fa-sync"></i>
                </button>
            </div>
            <div class="widget-content">
                <div class="environmental-grid" id="environmental-data">
                    <!-- Environmental data will be loaded here -->
                </div>
            </div>
        `;
    }

    // Sensors Widget
    getSensorsWidget() {
        return `
            <div class="widget-header">
                <h4><i class="fas fa-thermometer-half"></i> Sensors</h4>
            </div>
            <div class="widget-content">
                <div class="widget-stat">
                    <div class="stat-number" id="sensors-count">0</div>
                    <div class="stat-label">Active Sensors</div>
                </div>
            </div>
        `;
    }

    // Strains Widget
    getStrainsWidget() {
        return `
            <div class="widget-header">
                <h4><i class="fas fa-dna"></i> Strains</h4>
            </div>
            <div class="widget-content">
                <div class="widget-stat">
                    <div class="stat-number" id="strains-count">0</div>
                    <div class="stat-label">In Collection</div>
                </div>
            </div>
        `;
    }

    // Harvests Widget
    getHarvestsWidget() {
        return `
            <div class="widget-header">
                <h4><i class="fas fa-leaf"></i> Harvests</h4>
            </div>
            <div class="widget-content">
                <div class="widget-stat">
                    <div class="stat-number" id="harvests-count">0</div>
                    <div class="stat-label">Completed</div>
                </div>
            </div>
        `;
    }

    // Setup drag and drop functionality
    setupDragAndDrop() {
        const container = document.querySelector('.dashboard-widgets');
        if (!container) return;

        // Mouse events
        container.addEventListener('mousedown', this.handleMouseDown.bind(this));
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
        document.addEventListener('mouseup', this.handleMouseUp.bind(this));

        // Touch events for mobile
        container.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: false });
        document.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: false });
        document.addEventListener('touchend', this.handleTouchEnd.bind(this));
    }

    // Mouse event handlers
    handleMouseDown(e) {
        const dragHandle = e.target.closest('.widget-drag-handle');
        if (!dragHandle) return;

        e.preventDefault();
        this.startDrag(e, dragHandle.parentElement);
    }

    handleMouseMove(e) {
        if (!this.isDragging) return;
        e.preventDefault();
        this.updateDrag(e.clientX, e.clientY);
    }

    handleMouseUp(e) {
        if (!this.isDragging) return;
        this.endDrag();
    }

    // Touch event handlers
    handleTouchStart(e) {
        const dragHandle = e.target.closest('.widget-drag-handle');
        if (!dragHandle) return;

        e.preventDefault();
        const touch = e.touches[0];
        this.touchStartPos = { x: touch.clientX, y: touch.clientY };
        this.startDrag(touch, dragHandle.parentElement);
    }

    handleTouchMove(e) {
        if (!this.isDragging) return;
        e.preventDefault();
        const touch = e.touches[0];
        this.updateDrag(touch.clientX, touch.clientY);
    }

    handleTouchEnd(e) {
        if (!this.isDragging) return;
        this.endDrag();
    }

    // Start drag operation
    startDrag(event, element) {
        this.isDragging = true;
        this.draggedElement = element;
        element.classList.add('dragging');
        document.body.style.cursor = 'grabbing';
    }

    // Update drag position
    updateDrag(x, y) {
        if (!this.draggedElement) return;

        // Find the element at the current position
        const elementBelow = document.elementFromPoint(x, y);
        const targetWidget = elementBelow?.closest('.dashboard-widget');

        if (targetWidget && targetWidget !== this.draggedElement) {
            // Determine if we should insert before or after
            const rect = targetWidget.getBoundingClientRect();
            const midpoint = rect.top + rect.height / 2;
            
            if (y < midpoint) {
                targetWidget.parentNode.insertBefore(this.draggedElement, targetWidget);
            } else {
                targetWidget.parentNode.insertBefore(this.draggedElement, targetWidget.nextSibling);
            }
        }
    }

    // End drag operation
    endDrag() {
        if (!this.isDragging) return;

        this.isDragging = false;
        if (this.draggedElement) {
            this.draggedElement.classList.remove('dragging');
            this.updateWidgetOrder();
        }
        this.draggedElement = null;
        document.body.style.cursor = '';
    }

    // Update widget order after drag
    updateWidgetOrder() {
        const widgets = document.querySelectorAll('.dashboard-widget');
        widgets.forEach((widget, index) => {
            const widgetId = widget.dataset.widgetId;
            const widgetConfig = this.widgetConfig.widgets.find(w => w.id === widgetId);
            if (widgetConfig) {
                widgetConfig.order = index + 1;
            }
        });
        this.saveWidgetConfig();
    }

    // Toggle widget visibility
    toggleWidget(widgetId) {
        const widget = this.widgetConfig.widgets.find(w => w.id === widgetId);
        if (widget) {
            widget.enabled = !widget.enabled;
            this.saveWidgetConfig();
            this.loadWidgets();
        }
    }

    // Toggle widget settings panel
    toggleWidgetSettings() {
        const panel = document.querySelector('.widget-settings-panel');
        if (panel) {
            panel.classList.toggle('active');
        }
    }

    // Handle window resize
    handleResize() {
        // Adjust widget sizes for mobile
        const isMobile = window.innerWidth < 768;
        const widgets = document.querySelectorAll('.dashboard-widget');
        
        widgets.forEach(widget => {
            if (isMobile) {
                widget.classList.add('mobile-optimized');
            } else {
                widget.classList.remove('mobile-optimized');
            }
        });
    }

    // Setup mobile-specific handlers
    setupMobileHandlers() {
        // Swipe gestures for timeline navigation
        let startX = 0;
        let startY = 0;
        
        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        document.addEventListener('touchend', (e) => {
            if (!startX || !startY) return;
            
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            
            const diffX = startX - endX;
            const diffY = startY - endY;
            
            // Only handle horizontal swipes on timeline
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                const timeline = e.target.closest('.timeline-container');
                if (timeline) {
                    if (diffX > 0) {
                        this.navigateTimeline('next');
                    } else {
                        this.navigateTimeline('prev');
                    }
                }
            }
            
            startX = 0;
            startY = 0;
        });
    }

    // Navigate timeline
    navigateTimeline(direction) {
        // Timeline navigation logic would go here
        console.log('Navigate timeline:', direction);
    }

    // Load plant timeline data
    loadPlantTimeline() {
        // This would typically fetch from an API
        const timelineContainer = document.getElementById('plant-timeline');
        if (!timelineContainer) return;

        // Mock timeline data
        const timelineData = [
            { date: '2025-01-20', event: 'Planted Northern Lights seeds', type: 'plant' },
            { date: '2025-01-22', event: 'First watering', type: 'water' },
            { date: '2025-01-25', event: 'Seedlings emerged', type: 'growth' },
            { date: '2025-01-27', event: 'Added nutrients', type: 'feed' }
        ];

        const timelineHTML = timelineData.map(item => `
            <div class="timeline-item timeline-${item.type}">
                <div class="timeline-date">${new Date(item.date).toLocaleDateString()}</div>
                <div class="timeline-content">
                    <div class="timeline-icon">
                        <i class="fas fa-${this.getTimelineIcon(item.type)}"></i>
                    </div>
                    <div class="timeline-text">${item.event}</div>
                </div>
            </div>
        `).join('');

        timelineContainer.innerHTML = timelineHTML;
    }

    // Get timeline icon based on event type
    getTimelineIcon(type) {
        const icons = {
            plant: 'seedling',
            water: 'tint',
            feed: 'flask',
            growth: 'leaf',
            harvest: 'cut'
        };
        return icons[type] || 'circle';
    }

    // Initialize data loading
    loadWidgetData() {
        this.loadPlantTimeline();
        // Load other widget data as needed
    }
}

// Initialize dashboard widgets when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.dashboard-widgets')) {
        window.dashboardWidgets = new DashboardWidgetSystem();
        window.dashboardWidgets.loadWidgetData();
    }
});