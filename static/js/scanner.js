/**
 * Scanner Frontend Logic
 * Crop Disease Detection - Premium UI
 */

// Configuration
const API_BASE = '/api';
const SCAN_ENDPOINT = `${API_BASE}/scan`;
const HISTORY_ENDPOINT = `${API_BASE}/scan/history`;
const DISEASE_ENDPOINT = `${API_BASE}/scan/disease`;

// DOM Elements
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const scanningContainer = document.getElementById('scanningContainer');
const resultsContainer = document.getElementById('resultsContainer');
const imagePreview = document.getElementById('imagePreview');
const previewImage = document.getElementById('previewImage');
const resetBtn = document.getElementById('resetBtn');
const refreshBtn = document.getElementById('refreshBtn');
const downloadBtn = document.getElementById('downloadBtn');
const closePreview = document.getElementById('closePreview');

// Protocol tabs
const protocolTabs = document.querySelectorAll('.protocol-tab');
const protocolPanels = document.querySelectorAll('.protocol-panel');

// ============================================
// EVENT LISTENERS
// ============================================

// Upload zone drag and drop
uploadZone.addEventListener('dragover', handleDragOver);
uploadZone.addEventListener('dragleave', handleDragLeave);
uploadZone.addEventListener('drop', handleDrop);
uploadZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', handleFileSelect);

// Reset button
if (resetBtn) {
    resetBtn.addEventListener('click', resetScanner);
}

// Download button
if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadReport);
}

// Close preview
if (closePreview) {
    closePreview.addEventListener('click', () => {
        imagePreview.classList.add('hidden');
    });
}

// Protocol tabs
protocolTabs.forEach(tab => {
    tab.addEventListener('click', handleTabSwitch);
});

// ============================================
// DRAG AND DROP HANDLERS
// ============================================

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadZone.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadZone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

// ============================================
// FILE PROCESSING
// ============================================

async function processFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        imagePreview.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
    
    // Show scanning animation
    uploadZone.classList.add('hidden');
    resultsContainer.classList.add('hidden');
    scanningContainer.classList.remove('hidden');
    
    // Upload and scan
    await uploadAndScan(file);
}

async function uploadAndScan(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(SCAN_ENDPOINT, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Scan failed: ' + response.statusText);
        }
        
        const data = await response.json();
        
        // Hide scanning, show results
        scanningContainer.classList.add('hidden');
        resultsContainer.classList.remove('hidden');
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError('Scanning error: ' + error.message);
        scanningContainer.classList.add('hidden');
        uploadZone.classList.remove('hidden');
    }
}

// ============================================
// RESULTS DISPLAY
// ============================================

async function displayResults(scanData) {
    // Update disease name
    const diseaseName = document.getElementById('diseaseName');
    const severityBadge = document.getElementById('severityBadge');
    const severityText = document.getElementById('severityText');
    
    diseaseName.textContent = scanData.disease_name;
    
    // Get disease details for severity
    try {
        const diseaseKey = scanData.disease_name.toLowerCase().replace(/\s+/g, '_');
        const diseaseResponse = await fetch(`${DISEASE_ENDPOINT}/${diseaseKey}`);
        const diseaseData = await diseaseResponse.json();
        const disease = diseaseData.disease;
        
        // Update severity badge
        const severity = disease.severity;
        severityBadge.className = `severity-badge ${severity}`;
        severityText.textContent = severity.toUpperCase();
        
        // Update treatment protocols
        updateTreatmentProtocols(disease);
        
    } catch (error) {
        console.error('Error fetching disease details:', error);
    }
    
    // Update confidence gauge
    const confidence = scanData.confidence_score;
    const confidenceGauge = document.getElementById('confidenceGauge');
    const confidenceText = document.getElementById('confidenceText');
    
    // Animate gauge fill
    setTimeout(() => {
        confidenceGauge.style.width = confidence + '%';
        confidenceText.textContent = confidence.toFixed(1) + '%';
    }, 100);
    
    // Update latency
    const latencyValue = document.getElementById('latencyValue');
    latencyValue.textContent = scanData.processing_latency_ms + 'ms';
}

function updateTreatmentProtocols(disease) {
    const protocols = disease.treatment_protocols;
    
    // Immediate actions
    const immediateList = document.getElementById('immediateList');
    immediateList.innerHTML = '';
    if (protocols.immediate) {
        protocols.immediate.forEach(action => {
            const li = document.createElement('li');
            li.textContent = action;
            immediateList.appendChild(li);
        });
    }
    
    // Biological solutions
    const biologicalList = document.getElementById('biologicalList');
    biologicalList.innerHTML = '';
    if (protocols.biological) {
        protocols.biological.forEach(action => {
            const li = document.createElement('li');
            li.textContent = action;
            biologicalList.appendChild(li);
        });
    }
    
    // Prevention
    const preventativeList = document.getElementById('preventativeList');
    preventativeList.innerHTML = '';
    if (protocols.preventative) {
        protocols.preventative.forEach(action => {
            const li = document.createElement('li');
            li.textContent = action;
            preventativeList.appendChild(li);
        });
    }
}

// ============================================
// PROTOCOL TAB SWITCHING
// ============================================

function handleTabSwitch(e) {
    const tabName = e.target.dataset.tab;
    
    // Update active tab
    protocolTabs.forEach(tab => tab.classList.remove('active'));
    e.target.classList.add('active');
    
    // Update active panel
    protocolPanels.forEach(panel => panel.classList.remove('active'));
    document.querySelector(`[data-panel="${tabName}"]`).classList.add('active');
}

// ============================================
// ACTIONS
// ============================================

function resetScanner() {
    uploadZone.classList.remove('hidden');
    resultsContainer.classList.add('hidden');
    scanningContainer.classList.add('hidden');
    imagePreview.classList.add('hidden');
    fileInput.value = '';
    
    // Reset tabs
    protocolTabs.forEach((tab, index) => {
        if (index === 0) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
    
    protocolPanels.forEach((panel, index) => {
        if (index === 0) {
            panel.classList.add('active');
        } else {
            panel.classList.remove('active');
        }
    });
}

function downloadReport() {
    const disease = document.getElementById('diseaseName').textContent;
    const confidence = document.getElementById('confidenceText').textContent;
    const latency = document.getElementById('latencyValue').textContent;
    
    const report = `
CROP DISEASE DETECTION REPORT
============================
Generated: ${new Date().toLocaleString()}

DISEASE DETECTED: ${disease}
Confidence Score: ${confidence}
Processing Latency: ${latency}

IMMEDIATE ACTIONS:
${getProtocolText('immediateList')}

BIOLOGICAL SOLUTIONS:
${getProtocolText('biologicalList')}

PREVENTION:
${getProtocolText('preventativeList')}

---
Generated by CropAI Premium Disease Detection System
    `.trim();
    
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(report));
    element.setAttribute('download', `crop-disease-report-${new Date().getTime()}.txt`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function getProtocolText(listId) {
    const list = document.getElementById(listId);
    const items = Array.from(list.querySelectorAll('li'));
    return items.map(item => `- ${item.textContent}`).join('\n');
}

// ============================================
// ERROR HANDLING
// ============================================

function showError(message) {
    alert(message);
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🌾 Crop Disease Detection Scanner initialized');
});
