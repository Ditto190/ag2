/**
 * Generative UI Application
 * Main JavaScript for handling UI generation and rendering
 */

// UI Component Renderer
window.UIComponentRenderer = {
    /**
     * Render a UI component based on its specification
     */
    render(componentData) {
        const type = componentData.type;
        
        switch(type) {
            case 'form':
                return this.renderForm(componentData);
            case 'table':
                return this.renderTable(componentData);
            case 'dashboard':
                return this.renderDashboard(componentData);
            case 'chart':
                return this.renderChart(componentData);
            case 'chat':
                return this.renderChat(componentData);
            case 'card':
                return this.renderCard(componentData);
            default:
                return this.renderDefault(componentData);
        }
    },

    /**
     * Render a form component
     */
    renderForm(data) {
        const form = document.createElement('form');
        form.className = 'component-form';
        
        data.fields.forEach(field => {
            const formGroup = document.createElement('div');
            formGroup.className = 'form-group';
            
            const label = document.createElement('label');
            label.className = 'form-label';
            label.textContent = field.label;
            if (field.required) {
                label.textContent += ' *';
            }
            
            let input;
            if (field.type === 'textarea') {
                input = document.createElement('textarea');
                input.className = 'form-textarea';
                input.rows = 4;
            } else {
                input = document.createElement('input');
                input.className = 'form-input';
                input.type = field.type;
            }
            
            input.name = field.name;
            input.placeholder = field.placeholder || '';
            input.required = field.required || false;
            
            formGroup.appendChild(label);
            formGroup.appendChild(input);
            form.appendChild(formGroup);
        });
        
        // Add submit button
        const submitBtn = document.createElement('button');
        submitBtn.type = 'submit';
        submitBtn.className = 'btn btn-primary';
        submitBtn.textContent = data.submitButton?.text || 'Submit';
        
        form.appendChild(submitBtn);
        
        // Handle form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            console.log('Form submitted:', data);
            alert('Form submitted! Check console for data.');
        });
        
        return form;
    },

    /**
     * Render a table component
     */
    renderTable(data) {
        const wrapper = document.createElement('div');
        wrapper.className = 'component-table-wrapper';
        
        const table = document.createElement('table');
        table.className = 'component-table';
        
        // Create header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        data.headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Create body
        const tbody = document.createElement('tbody');
        data.rows.forEach(row => {
            const tr = document.createElement('tr');
            row.forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        
        wrapper.appendChild(table);
        
        // Add pagination if present
        if (data.pagination) {
            const pagination = document.createElement('div');
            pagination.className = 'pagination';
            pagination.textContent = `Page ${data.pagination.currentPage} of ${data.pagination.totalPages}`;
            wrapper.appendChild(pagination);
        }
        
        return wrapper;
    },

    /**
     * Render a dashboard component
     */
    renderDashboard(data) {
        const dashboard = document.createElement('div');
        dashboard.className = 'component-dashboard';
        
        const title = document.createElement('h3');
        title.textContent = data.title;
        dashboard.appendChild(title);
        
        const widgetsContainer = document.createElement('div');
        widgetsContainer.className = 'dashboard-widgets';
        widgetsContainer.style.display = 'grid';
        widgetsContainer.style.gridTemplateColumns = 'repeat(auto-fit, minmax(250px, 1fr))';
        widgetsContainer.style.gap = '1rem';
        widgetsContainer.style.marginTop = '1rem';
        
        data.widgets.forEach(widget => {
            const widgetEl = this.renderWidget(widget);
            widgetsContainer.appendChild(widgetEl);
        });
        
        dashboard.appendChild(widgetsContainer);
        return dashboard;
    },

    /**
     * Render a dashboard widget
     */
    renderWidget(widget) {
        const widgetEl = document.createElement('div');
        widgetEl.className = 'dashboard-widget';
        widgetEl.style.backgroundColor = 'white';
        widgetEl.style.padding = '1.5rem';
        widgetEl.style.borderRadius = '0.5rem';
        widgetEl.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
        
        if (widget.type === 'metric') {
            const title = document.createElement('div');
            title.textContent = widget.title;
            title.style.fontSize = '0.875rem';
            title.style.color = '#6B7280';
            
            const value = document.createElement('div');
            value.textContent = widget.value;
            value.style.fontSize = '2rem';
            value.style.fontWeight = 'bold';
            value.style.marginTop = '0.5rem';
            
            const change = document.createElement('div');
            change.textContent = widget.change;
            change.style.fontSize = '0.875rem';
            change.style.color = widget.trend === 'up' ? '#10B981' : '#EF4444';
            change.style.marginTop = '0.5rem';
            
            widgetEl.appendChild(title);
            widgetEl.appendChild(value);
            widgetEl.appendChild(change);
        } else if (widget.type === 'chart') {
            const title = document.createElement('div');
            title.textContent = widget.title;
            title.style.fontWeight = '600';
            title.style.marginBottom = '1rem';
            
            const chartPlaceholder = document.createElement('div');
            chartPlaceholder.textContent = '📊 Chart: ' + widget.chartType;
            chartPlaceholder.style.textAlign = 'center';
            chartPlaceholder.style.padding = '2rem';
            chartPlaceholder.style.backgroundColor = '#F9FAFB';
            chartPlaceholder.style.borderRadius = '0.375rem';
            
            widgetEl.appendChild(title);
            widgetEl.appendChild(chartPlaceholder);
        }
        
        return widgetEl;
    },

    /**
     * Render a chart component
     */
    renderChart(data) {
        const chartContainer = document.createElement('div');
        chartContainer.className = 'component-chart';
        chartContainer.style.backgroundColor = 'white';
        chartContainer.style.padding = '1.5rem';
        chartContainer.style.borderRadius = '0.5rem';
        
        const title = document.createElement('h3');
        title.textContent = data.title;
        chartContainer.appendChild(title);
        
        const chartPlaceholder = document.createElement('div');
        chartPlaceholder.style.height = '300px';
        chartPlaceholder.style.display = 'flex';
        chartPlaceholder.style.alignItems = 'center';
        chartPlaceholder.style.justifyContent = 'center';
        chartPlaceholder.style.backgroundColor = '#F9FAFB';
        chartPlaceholder.style.borderRadius = '0.375rem';
        chartPlaceholder.style.marginTop = '1rem';
        chartPlaceholder.textContent = `📊 ${data.chartType.toUpperCase()} Chart Visualization`;
        
        chartContainer.appendChild(chartPlaceholder);
        
        // Note: In a real app, you'd integrate Chart.js or similar library here
        return chartContainer;
    },

    /**
     * Render a chat component
     */
    renderChat(data) {
        const chatContainer = document.createElement('div');
        chatContainer.className = 'component-chat';
        chatContainer.style.maxWidth = '600px';
        
        const messagesContainer = document.createElement('div');
        messagesContainer.className = 'chat-messages';
        messagesContainer.style.height = '400px';
        messagesContainer.style.overflowY = 'auto';
        messagesContainer.style.border = '1px solid #E5E7EB';
        messagesContainer.style.borderRadius = '0.5rem';
        messagesContainer.style.padding = '1rem';
        messagesContainer.style.marginBottom = '1rem';
        
        data.messages.forEach(msg => {
            const msgEl = document.createElement('div');
            msgEl.className = `chat-message chat-message-${msg.sender}`;
            msgEl.style.marginBottom = '0.75rem';
            msgEl.style.padding = '0.75rem';
            msgEl.style.borderRadius = '0.375rem';
            msgEl.style.backgroundColor = msg.sender === 'assistant' ? '#F3F4F6' : '#DBEAFE';
            msgEl.textContent = msg.text;
            messagesContainer.appendChild(msgEl);
        });
        
        const inputContainer = document.createElement('div');
        inputContainer.style.display = 'flex';
        inputContainer.style.gap = '0.5rem';
        
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = data.inputPlaceholder || 'Type a message...';
        input.className = 'form-input';
        input.style.flex = '1';
        
        const sendBtn = document.createElement('button');
        sendBtn.textContent = 'Send';
        sendBtn.className = 'btn btn-primary';
        sendBtn.onclick = () => {
            if (input.value.trim()) {
                const msgEl = document.createElement('div');
                msgEl.className = 'chat-message chat-message-user';
                msgEl.style.marginBottom = '0.75rem';
                msgEl.style.padding = '0.75rem';
                msgEl.style.borderRadius = '0.375rem';
                msgEl.style.backgroundColor = '#DBEAFE';
                msgEl.textContent = input.value;
                messagesContainer.appendChild(msgEl);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                input.value = '';
            }
        };
        
        inputContainer.appendChild(input);
        inputContainer.appendChild(sendBtn);
        
        chatContainer.appendChild(messagesContainer);
        chatContainer.appendChild(inputContainer);
        
        return chatContainer;
    },

    /**
     * Render a card component
     */
    renderCard(data) {
        const card = document.createElement('div');
        card.className = 'component-card';
        card.style.backgroundColor = 'white';
        card.style.padding = '1.5rem';
        card.style.borderRadius = '0.5rem';
        card.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
        
        if (data.title) {
            const title = document.createElement('h3');
            title.textContent = data.title;
            card.appendChild(title);
        }
        
        if (data.content) {
            const content = document.createElement('p');
            content.textContent = data.content;
            content.style.marginTop = '0.5rem';
            content.style.color = '#6B7280';
            card.appendChild(content);
        }
        
        if (data.actions) {
            const actionsContainer = document.createElement('div');
            actionsContainer.style.marginTop = '1rem';
            actionsContainer.style.display = 'flex';
            actionsContainer.style.gap = '0.5rem';
            
            data.actions.forEach(action => {
                const btn = document.createElement('button');
                btn.className = 'btn btn-primary';
                btn.textContent = action.label;
                btn.onclick = () => {
                    if (action.intent) {
                        document.getElementById('intentInput').value = action.intent;
                        document.getElementById('generateBtn').click();
                    }
                };
                actionsContainer.appendChild(btn);
            });
            
            card.appendChild(actionsContainer);
        }
        
        return card;
    },

    /**
     * Render default/unknown component
     */
    renderDefault(data) {
        const container = document.createElement('div');
        container.className = 'component-default';
        container.style.padding = '1rem';
        container.style.backgroundColor = '#FEF3C7';
        container.style.borderRadius = '0.375rem';
        container.textContent = 'Component type not fully supported yet: ' + data.type;
        
        const pre = document.createElement('pre');
        pre.style.marginTop = '1rem';
        pre.style.fontSize = '0.875rem';
        pre.style.overflow = 'auto';
        pre.textContent = JSON.stringify(data, null, 2);
        container.appendChild(pre);
        
        return container;
    }
};

// WebSocket connection manager (for real-time updates)
class WebSocketManager {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.reconnectDelay = 1000;
        this.maxReconnectDelay = 30000;
    }

    connect() {
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectDelay = 1000;
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket disconnected. Reconnecting...');
            setTimeout(() => this.connect(), this.reconnectDelay);
            this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }

    handleMessage(data) {
        console.log('Received message:', data);
        
        if (data.type === 'ui_update') {
            const container = document.getElementById('generatedUI');
            if (container) {
                container.innerHTML = '';
                const component = UIComponentRenderer.render(data.components);
                container.appendChild(component);
            }
        }
    }
}

// Initialize WebSocket connection (optional, enable if needed)
// const wsManager = new WebSocketManager(`ws://${window.location.host}/ws`);
// wsManager.connect();

console.log('Generative UI application loaded');
