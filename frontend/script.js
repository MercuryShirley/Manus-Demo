document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chatContainer');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');

    // Backend API URL
    const API_URL = 'http://localhost:8000/chat/stream';

    // Function to create a message element
    function createMessageElement(isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'system-message'}`;
        
        if (!isUser) {
            const avatarDiv = document.createElement('div');
            avatarDiv.className = 'avatar';
            avatarDiv.textContent = 'M';
            messageDiv.appendChild(avatarDiv);
        }
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        messageDiv.appendChild(contentDiv);
        
        return { messageDiv, contentDiv };
    }

    // Function to add a user message
    function addUserMessage(text) {
        if (!text.trim()) return;
        
        const { messageDiv, contentDiv } = createMessageElement(true);
        contentDiv.textContent = text;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Function to create thinking animation
    function createThinkingMessage() {
        const { messageDiv, contentDiv } = createMessageElement(false);
        contentDiv.innerHTML = '<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>';
        contentDiv.classList.add('thinking');
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return { messageDiv, contentDiv };
    }

    // Function to create TODO list element
    function createTodoList(queryAnalysis, todos) {
        const todoContainer = document.createElement('div');
        todoContainer.className = 'todo-container';
        
        const analysisDiv = document.createElement('div');
        analysisDiv.className = 'query-analysis';
        analysisDiv.innerHTML = `<span class="analysis-icon">📋</span> <strong>分析：</strong>${queryAnalysis}`;
        todoContainer.appendChild(analysisDiv);
        
        const headerDiv = document.createElement('div');
        headerDiv.className = 'todo-header';
        headerDiv.innerHTML = '<strong>📝 任务列表</strong>';
        todoContainer.appendChild(headerDiv);
        
        const todoList = document.createElement('ul');
        todoList.className = 'todo-list';
        
        todos.forEach(todo => {
            const todoItem = document.createElement('li');
            todoItem.className = 'todo-item';
            todoItem.id = `todo-${todo.id}`;
            
            const checkbox = document.createElement('span');
            checkbox.className = 'todo-checkbox pending';
            checkbox.innerHTML = '○';
            
            const typeIcon = {
                'search': '🔍',
                'analyze': '🧠',
                'synthesize': '📊'
            }[todo.type] || '📌';
            
            const label = document.createElement('span');
            label.className = 'todo-label';
            label.innerHTML = `<span class="type-icon">${typeIcon}</span> ${todo.name}`;
            
            if (todo.depends_on && todo.depends_on.length > 0) {
                const depsSpan = document.createElement('span');
                depsSpan.className = 'todo-deps';
                depsSpan.textContent = ` (依赖: ${todo.depends_on.join(', ')})`;
                label.appendChild(depsSpan);
            }
            
            todoItem.appendChild(checkbox);
            todoItem.appendChild(label);
            todoList.appendChild(todoItem);
        });
        
        todoContainer.appendChild(todoList);
        return todoContainer;
    }

    // Function to update TODO item status
    function updateTodoStatus(taskId, status) {
        const todoItem = document.getElementById(`todo-${taskId}`);
        if (!todoItem) return;
        
        const checkbox = todoItem.querySelector('.todo-checkbox');
        if (!checkbox) return;
        
        todoItem.classList.remove('pending', 'running', 'completed');
        checkbox.classList.remove('pending', 'running', 'completed');
        
        if (status === 'running') {
            checkbox.className = 'todo-checkbox running';
            checkbox.innerHTML = '◐';
            todoItem.classList.add('running');
        } else if (status === 'completed') {
            checkbox.className = 'todo-checkbox completed';
            checkbox.innerHTML = '✓';
            todoItem.classList.add('completed');
        }
        
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Base64 decode function with proper UTF-8 handling
    function decodeBase64(str) {
        try {
            const binaryStr = atob(str);
            const bytes = new Uint8Array(binaryStr.length);
            for (let i = 0; i < binaryStr.length; i++) {
                bytes[i] = binaryStr.charCodeAt(i);
            }
            return new TextDecoder('utf-8').decode(bytes);
        } catch (e) {
            console.error('Base64 decode error:', e);
            return str;
        }
    }

    // Function to handle SSE stream
    async function handleStreamResponse(message) {
        let { messageDiv, contentDiv } = createThinkingMessage();
        let todoContainer = null;
        let finalReply = '';

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                
                // Process complete SSE events
                let eventEnd;
                while ((eventEnd = buffer.indexOf('\n\n')) !== -1) {
                    const eventData = buffer.substring(0, eventEnd);
                    buffer = buffer.substring(eventEnd + 2);
                    
                    if (eventData.startsWith('data: ')) {
                        try {
                            const jsonStr = eventData.slice(6);
                            const data = JSON.parse(jsonStr);
                            
                            console.log('SSE Event:', data.type);
                            
                            switch (data.type) {
                                case 'status':
                                    contentDiv.innerHTML = `<span class="status-text">${data.message}</span><span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>`;
                                    break;
                                    
                                case 'plan':
                                    contentDiv.classList.remove('thinking');
                                    contentDiv.innerHTML = '';
                                    todoContainer = createTodoList(data.query_analysis, data.todos);
                                    contentDiv.appendChild(todoContainer);
                                    chatContainer.scrollTop = chatContainer.scrollHeight;
                                    break;
                                    
                                case 'task_start':
                                    updateTodoStatus(data.task_id, 'running');
                                    break;
                                    
                                case 'task_complete':
                                    updateTodoStatus(data.task_id, 'completed');
                                    break;
                                    
                                case 'final':
                                    if (data.reply_base64) {
                                        finalReply = decodeBase64(data.reply_base64);
                                        console.log('Final reply length:', finalReply.length);
                                    } else if (data.reply) {
                                        finalReply = data.reply;
                                    }
                                    break;
                                    
                                case 'done':
                                    if (finalReply) {
                                        const { messageDiv: finalMsgDiv, contentDiv: finalContentDiv } = createMessageElement(false);
                                        finalContentDiv.innerHTML = formatMarkdown(finalReply);
                                        chatContainer.appendChild(finalMsgDiv);
                                        chatContainer.scrollTop = chatContainer.scrollHeight;
                                    }
                                    break;
                            }
                        } catch (e) {
                            console.error('Error parsing SSE data:', e, eventData);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
            contentDiv.classList.remove('thinking');
            contentDiv.textContent = '抱歉，连接服务器时出现错误。';
        }
    }

    // Markdown formatter with Table support
    function formatMarkdown(text) {
        if (!text) return '';
        
        let html = text;

        // 1. Process Code Blocks first
        const codeBlocks = [];
        html = html.replace(/```([\s\S]*?)```/g, (match, code) => {
            codeBlocks.push(code);
            return `__CODE_BLOCK_${codeBlocks.length - 1}__`;
        });

        // 2. Process Tables - more robust regex
        const lines = html.split('\n');
        let inTable = false;
        let tableLines = [];
        let result = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const isTableRow = line.trim().startsWith('|') && line.trim().endsWith('|');
            const isSeparator = /^\|[\s\-:|]+\|$/.test(line.trim());
            
            if (isTableRow || isSeparator) {
                if (!inTable) {
                    inTable = true;
                    tableLines = [];
                }
                tableLines.push(line);
            } else {
                if (inTable) {
                    // End of table, convert it
                    result.push(convertTableToHtml(tableLines));
                    inTable = false;
                    tableLines = [];
                }
                result.push(line);
            }
        }
        
        // Handle table at end of content
        if (inTable && tableLines.length > 0) {
            result.push(convertTableToHtml(tableLines));
        }
        
        html = result.join('\n');

        // 3. Process other Markdown elements
        html = html
            .replace(/^### (.*$)/gm, '<h4>$1</h4>')
            .replace(/^## (.*$)/gm, '<h3>$1</h3>')
            .replace(/^# (.*$)/gm, '<h2>$1</h2>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/^---$/gm, '<hr>')
            .replace(/^- (.*)$/gm, '<li>$1</li>')
            .replace(/\n/g, '<br>');

        // Wrap consecutive <li> items in <ul>
        html = html.replace(/(<li>.*?<\/li>)(<br>)?(<li>)/g, '$1$3');
        html = html.replace(/(<li>.*?<\/li>)+/g, '<ul>$&</ul>');

        // 4. Restore Code Blocks
        html = html.replace(/__CODE_BLOCK_(\d+)__/g, (match, index) => {
            return `<pre><code>${codeBlocks[index]}</code></pre>`;
        });
        
        return html;
    }

    // Convert markdown table lines to HTML table
    function convertTableToHtml(tableLines) {
        if (tableLines.length < 2) return tableLines.join('\n');
        
        const headerLine = tableLines[0];
        const separatorLine = tableLines[1];
        const bodyLines = tableLines.slice(2);
        
        // Check if second line is separator
        if (!/^[\s\|:-]+$/.test(separatorLine)) {
            return tableLines.join('\n');
        }
        
        const parseRow = (line) => {
            return line.split('|')
                .slice(1, -1) // Remove first and last empty elements
                .map(cell => cell.trim());
        };
        
        const headers = parseRow(headerLine);
        
        let tableHtml = '<div class="table-container"><table><thead><tr>';
        headers.forEach(header => {
            tableHtml += `<th>${header}</th>`;
        });
        tableHtml += '</tr></thead><tbody>';
        
        bodyLines.forEach(line => {
            const cells = parseRow(line);
            if (cells.length > 0) {
                tableHtml += '<tr>';
                headers.forEach((_, index) => {
                    const cellContent = cells[index] || '';
                    tableHtml += `<td>${cellContent}</td>`;
                });
                tableHtml += '</tr>';
            }
        });
        
        tableHtml += '</tbody></table></div>';
        return tableHtml;
    }

    // Function to handle sending message
    async function handleSend() {
        const text = messageInput.value;
        if (text.trim()) {
            addUserMessage(text);
            messageInput.value = '';
            messageInput.disabled = true;
            sendBtn.disabled = true;

            await handleStreamResponse(text);

            messageInput.disabled = false;
            sendBtn.disabled = false;
            messageInput.focus();
        }
    }

    // Event listeners
    sendBtn.addEventListener('click', handleSend);

    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    });

    messageInput.focus();
});
