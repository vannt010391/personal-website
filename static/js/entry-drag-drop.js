/**
 * Drag and Drop Reordering for Knowledge Entries
 * Uses HTML5 Drag and Drop API
 */

class EntryTreeDragDrop {
    constructor() {
        this.draggedElement = null;
        this.draggedId = null;
        this.init();
    }

    init() {
        document.addEventListener('dragstart', (e) => this.handleDragStart(e));
        document.addEventListener('dragover', (e) => this.handleDragOver(e));
        document.addEventListener('drop', (e) => this.handleDrop(e));
        document.addEventListener('dragend', (e) => this.handleDragEnd(e));
        
        this.makeEntriesDraggable();
    }

    makeEntriesDraggable() {
        const entries = document.querySelectorAll('.entry-tree-link');
        entries.forEach(entry => {
            entry.draggable = true;
            entry.style.cursor = 'grab';
        });
    }

    handleDragStart(e) {
        if (!e.target.classList.contains('entry-tree-link')) return;
        
        this.draggedElement = e.target.closest('.entry-tree-item');
        this.draggedId = this.draggedElement.dataset.entryId;
        
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', e.target.innerHTML);
        
        this.draggedElement.style.opacity = '0.5';
        this.draggedElement.classList.add('dragging');
    }

    handleDragOver(e) {
        if (e.preventDefault) {
            e.preventDefault();
        }
        
        const target = e.target.closest('.entry-tree-item');
        if (target && target !== this.draggedElement) {
            target.classList.add('drag-over');
            e.dataTransfer.dropEffect = 'move';
        }
        
        return false;
    }

    handleDrop(e) {
        if (e.stopPropagation) {
            e.stopPropagation();
        }

        const target = e.target.closest('.entry-tree-item');
        if (!target || target === this.draggedElement) return false;

        const droppedEntryId = target.dataset.entryId;
        
        // Reorganize in DOM
        target.parentNode.insertBefore(this.draggedElement, target);
        
        // Update order via API
        this.updateOrder(this.draggedId, droppedEntryId);

        return false;
    }

    handleDragEnd(e) {
        if (this.draggedElement) {
            this.draggedElement.style.opacity = '1';
            this.draggedElement.classList.remove('dragging');
        }
        
        document.querySelectorAll('.drag-over').forEach(el => {
            el.classList.remove('drag-over');
        });
    }

    async updateOrder(draggedId, targetId) {
        try {
            const response = await fetch(`/api/knowledge-entries/${draggedId}/reorder/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                },
                body: JSON.stringify({
                    order: 0,  // Will be recalculated on backend
                })
            });

            if (!response.ok) {
                console.error('Failed to update order');
                location.reload();
            }
        } catch (error) {
            console.error('Error updating order:', error);
        }
    }

    getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new EntryTreeDragDrop();
    });
} else {
    new EntryTreeDragDrop();
}
