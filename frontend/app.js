const API_URL = window.location.origin.includes("127.0.0.1") || window.location.origin.includes("localhost") && !window.location.origin.includes("8000") ? "http://127.0.0.1:8000" : window.location.origin;
let activeTasks = [];

async function submitTask() {
    const promptInput = document.getElementById('prompt');
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    // Change button state
    const btn = document.getElementById('submitBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<span class="relative flex items-center justify-center gap-2"><svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Deploying...</span>`;

    try {
        await ensureUserAndWorkflowExist();

        const response = await fetch(`${API_URL}/tasks/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt, workflow_id: 1 })
        });
        
        const data = await response.json();
        
        activeTasks.unshift({ id: data.task_id, prompt: prompt, status: 'PENDING', result: null });
        promptInput.value = '';
        renderTasks();
        
        pollTaskStatus(data.task_id);
    } catch (error) {
        console.error("Error submitting task:", error);
        alert("Make sure the backend and celery worker are running!");
    } finally {
        // Restore button
        setTimeout(() => { btn.innerHTML = originalText; }, 500);
    }
}

async function ensureUserAndWorkflowExist() {
    try {
        await fetch(`${API_URL}/users/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: "demo@agentflow.ai" })
        });
        await fetch(`${API_URL}/workflows/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: "Demo Workflow", description: "Frontend demo", owner_id: 1 })
        });
    } catch(e) { }
}

async function pollTaskStatus(taskId) {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`${API_URL}/tasks/${taskId}`);
            const data = await response.json();
            
            const taskIndex = activeTasks.findIndex(t => t.id === taskId);
            if (taskIndex !== -1) {
                activeTasks[taskIndex].status = data.status;
                activeTasks[taskIndex].result = data.result;
                renderTasks();
                
                if (data.status === 'COMPLETED' || data.status === 'FAILED') {
                    clearInterval(interval);
                }
            }
        } catch (error) {
            console.error("Error polling:", error);
            clearInterval(interval);
        }
    }, 1000);
}

function getStatusConfig(status) {
    switch(status) {
        case 'PENDING': 
            return { color: 'text-amber-400', border: 'border-amber-500/50', bg: 'bg-amber-400/10', icon: '<svg class="w-4 h-4 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>' };
        case 'PROCESSING': 
            return { color: 'text-brand-500', border: 'border-brand-500/50', bg: 'bg-brand-500/10', icon: '<svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>' };
        case 'COMPLETED': 
            return { color: 'text-emerald-400', border: 'border-emerald-500/50', bg: 'bg-emerald-400/10', icon: '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>' };
        case 'FAILED': 
            return { color: 'text-rose-400', border: 'border-rose-500/50', bg: 'bg-rose-400/10', icon: '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>' };
        default: 
            return { color: 'text-slate-400', border: 'border-slate-500/50', bg: 'bg-slate-400/10', icon: '' };
    }
}

function renderTasks() {
    const taskList = document.getElementById('taskList');
    
    if (activeTasks.length === 0) {
        taskList.innerHTML = `
            <div class="flex flex-col items-center justify-center h-40 text-slate-500 space-y-3">
                <svg class="w-12 h-12 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
                <p>No active workflows. Deploy an agent to begin.</p>
            </div>
        `;
        return;
    }

    taskList.innerHTML = '';

    activeTasks.forEach(task => {
        const item = document.createElement('div');
        const config = getStatusConfig(task.status);
        
        item.className = `p-5 rounded-xl bg-slate-800/40 border-l-4 ${config.border} border-t border-r border-b border-slate-700/50 backdrop-blur-sm transition-all shadow-sm`;
        
        let resultHtml = '';
        if (task.result) {
            const parsedMarkdown = marked.parse(task.result);
            resultHtml = `
                <div class="mt-4 p-4 rounded-lg bg-slate-900/80 border border-emerald-500/20 shadow-inner max-h-[400px] overflow-y-auto">
                    <div class="prose prose-invert prose-emerald max-w-none text-sm">
                        ${parsedMarkdown}
                    </div>
                </div>
            `;
        }
        
        item.innerHTML = `
            <div class="flex justify-between items-center mb-3">
                <span class="text-xs font-bold text-slate-400 tracking-wider uppercase">Task ID #${task.id}</span>
                <span class="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold ${config.color} ${config.bg}">
                    ${config.icon}
                    ${task.status}
                </span>
            </div>
            <p class="text-slate-200 text-lg leading-snug">"${task.prompt}"</p>
            ${resultHtml}
        `;
        taskList.appendChild(item);
    });
}
