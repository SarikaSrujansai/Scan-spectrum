// Complete Scan Spectrum App with 3D Model Integration
class ScanSpectrumApp {
    constructor() {
        this.currentSection = 'scan';
        this.currentOrgan = null;
        this.currentSubpart = null;
        this.audioPlayer = new AudioPlayer();
        this.init();
    }

    init() {
        console.log('Scan Spectrum App Initialized');
        this.setupEventListeners();
        this.loadOrganLibrary();
        this.showSection('scan');
    }

    setupEventListeners() {
        // Navigation tabs
        document.getElementById('scan-tab').addEventListener('click', () => this.showSection('scan'));
        document.getElementById('explore-tab').addEventListener('click', () => this.showSection('explore'));
        document.getElementById('quiz-tab').addEventListener('click', () => this.showSection('quiz'));

        // Upload button
        document.getElementById('upload-btn').addEventListener('click', () => {
            document.getElementById('image-upload').click();
        });

        // File upload
        document.getElementById('image-upload').addEventListener('change', (e) => {
            this.handleImageUpload(e);
        });

        // Camera button
        document.getElementById('camera-btn').addEventListener('click', () => {
            alert('Camera feature coming soon! Please upload an image file.');
        });

        // Accessibility button
        document.getElementById('accessibility-btn').addEventListener('click', () => {
            this.toggleAccessibility();
        });

        // Settings button
        document.getElementById('settings-btn').addEventListener('click', () => {
            this.showSettings();
        });
    }

    showSection(section) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(el => {
            el.classList.add('hidden');
        });
       
        // Remove active from all tabs
        document.querySelectorAll('.nav-tab').forEach(el => {
            el.classList.remove('active');
        });

        // Show selected section
        document.getElementById(section + '-section').classList.remove('hidden');
        document.getElementById(section + '-tab').classList.add('active');
       
        this.currentSection = section;
    }

    async handleImageUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        console.log('Uploading:', file.name);

        // Show processing
        document.getElementById('processing-area').classList.remove('hidden');

        try {
            const formData = new FormData();
            formData.append('image', file);

            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            console.log('Upload result:', result);

            if (result.success) {
                this.showResults(result);
            } else {
                throw new Error(result.error);
            }

        } catch (error) {
            console.error('Upload failed:', error);
            this.showError('Upload failed: ' + error.message);
        } finally {
            document.getElementById('processing-area').classList.add('hidden');
        }
    }

    showResults(result) {
        document.getElementById('results-area').classList.remove('hidden');
       
        // Draw simple silhouette
        this.drawSilhouette(result.part);
       
        // Load organ data with 3D models
        this.loadOrganData(result.part);
       
        console.log(`Success! Detected: ${result.part} (${Math.round(result.confidence * 100)}% confidence)`);
       
        // Update detection display
        document.getElementById('detection-result').textContent = `Detected: ${result.part}`;
        document.getElementById('confidence-level').textContent = `AI Confidence: ${Math.round(result.confidence * 100)}%`;
    }

    drawSilhouette(organ) {
        const canvas = document.getElementById('silhouette-canvas');
        const ctx = canvas.getContext('2d');
       
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
       
        // Draw simple body silhouette
        ctx.fillStyle = '#3b82f6';
        ctx.globalAlpha = 0.3;
       
        // Head
        ctx.beginPath();
        ctx.arc(200, 80, 30, 0, Math.PI * 2);
        ctx.fill();
       
        // Body
        ctx.fillRect(170, 110, 60, 120);
       
        // Arms
        ctx.fillRect(140, 110, 30, 80);
        ctx.fillRect(230, 110, 30, 80);
       
        // Legs
        ctx.fillRect(180, 230, 25, 100);
        ctx.fillRect(195, 230, 25, 100);
       
        // Highlight organ with full opacity
        ctx.globalAlpha = 0.8;
        ctx.fillStyle = '#ef4444';
       
        if (organ === 'heart') {
            // Heart position
            ctx.beginPath();
            ctx.moveTo(190, 150);
            ctx.bezierCurveTo(190, 130, 210, 130, 210, 150);
            ctx.bezierCurveTo(210, 170, 200, 180, 190, 170);
            ctx.bezierCurveTo(180, 180, 190, 170, 190, 150);
            ctx.fill();
        } else if (organ === 'brain') {
            // Brain position
            ctx.beginPath();
            ctx.arc(200, 80, 25, 0, Math.PI * 2);
            ctx.fill();
        } else if (organ === 'lungs') {
            // Lungs position
            ctx.fillRect(160, 130, 30, 60);
            ctx.fillRect(210, 130, 30, 60);
        } else {
            // Default organ position
            ctx.fillRect(180, 160, 40, 40);
        }
       
        ctx.globalAlpha = 1.0;
    }

    async loadOrganData(organ) {
        try {
            const response = await fetch('/api/organ/' + organ);
            const data = await response.json();
            this.showOrganInfo(data);
            this.display3DModel(data);
            this.currentOrgan = data;
        } catch (error) {
            console.error('Failed to load organ data:', error);
            this.showDemoOrganInfo(organ);
        }
    }

    display3DModel(organData) {
        const modelDisplay = document.getElementById('model-display');
       
        if (organData.model_image) {
            modelDisplay.innerHTML = organData.model_image;
           
            // Update organ info
            document.getElementById('organ-name').textContent = organData.name;
            document.getElementById('organ-description').textContent = organData.full_description || organData.description;
            document.getElementById('detected-emoji').textContent = organData.emoji;
        } else {
            modelDisplay.innerHTML = `
                <div class="text-center text-white p-12">
                    <div class="text-6xl mb-4">🔬</div>
                    <p class="text-xl">3D Model Loading...</p>
                    <p class="text-gray-300 mt-2">Interactive ${organData.name} Anatomy</p>
                </div>
            `;
        }
    }

    showOrganInfo(organData) {
        const container = document.getElementById('subparts-nav');
        const content = document.getElementById('subpart-content');
       
        // Clear previous content
        container.innerHTML = '';
        content.innerHTML = '';
       
        // Create subpart buttons with numbering
        organData.subparts.forEach((subpart, index) => {
            const button = document.createElement('button');
            button.className = 'subpart-btn';
            button.innerHTML = `
                <div class="flex items-center text-left">
                    <div class="number-badge">${index + 1}</div>
                    <div>
                        <div class="font-semibold">${subpart.name}</div>
                        <div class="text-xs text-gray-600 mt-1">${subpart.function}</div>
                    </div>
                </div>
            `;
           
            button.addEventListener('click', () => {
                // Remove active class from all buttons
                document.querySelectorAll('.subpart-btn').forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                button.classList.add('active');
               
                this.showSubpartInfo(subpart, organData);
            });
           
            container.appendChild(button);
        });

        // Show first subpart by default
        if (organData.subparts.length > 0) {
            container.firstChild.click();
        }
    }

    showSubpartInfo(subpart, organData) {
        const detailsContainer = document.getElementById('subpart-details');
       
        detailsContainer.innerHTML = `
            <div class="professional-header">
                <div class="flex items-center">
                    <div class="number-badge" style="background: white; color: #3B82F6;">${subpart.number || 1}</div>
                    <div>
                        <h4 class="text-xl font-bold">${subpart.name}</h4>
                        <p class="text-blue-100">${subpart.function}</p>
                    </div>
                </div>
            </div>
           
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-6">
                <!-- Medical Content -->
                <div>
                    <h4 class="text-lg font-bold text-gray-800 mb-3">📚 Detailed Anatomy</h4>
                    <div class="space-y-4">
                        <p class="text-gray-700 leading-relaxed">${subpart.detailed_description || subpart.description}</p>
                       
                        <div class="teaching-point">
                            <strong>🎯 Medical Focus:</strong> Key anatomical features and functional significance
                        </div>
                       
                        <div class="clinical-note">
                            <strong>🏥 Clinical Importance:</strong> ${subpart.clinical_importance || 'Important for medical diagnosis and treatment'}
                        </div>
                       
                        <div class="anatomy-fact">
                            <strong>💡 Anatomical Fact:</strong> ${subpart.fun_fact}
                        </div>

                        ${subpart.dimensions ? `
                        <div class="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                            <strong>📏 Dimensions:</strong> ${subpart.dimensions}
                        </div>
                        ` : ''}
                    </div>
                </div>
               
                <!-- 3D Model Highlight -->
                <div>
                    <h4 class="text-lg font-bold text-gray-800 mb-3">🔬 3D Model Highlight</h4>
                    <p class="text-gray-600 mb-4">Structure ${subpart.number || 1} highlighted in the interactive model</p>
                    <div class="model-container" style="height: 300px;">
                        <div class="model-svg">
                            ${organData.model_image}
                            ${subpart.model_section || ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
       
        // Play audio narration for this subpart
        this.audioPlayer.playDemoNarration(subpart.name);
       
        this.currentSubpart = subpart;
    }

    showDemoOrganInfo(organ) {
        const demoData = {
            heart: {
                name: 'Heart',
                emoji: '❤️',
                description: 'The powerful muscular organ that pumps blood throughout your circulatory system.',
                full_description: 'The human heart is a sophisticated four-chambered muscular pump located in the mediastinum of the thoracic cavity.',
                model_image: `
                    <svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="heartGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#dc2626;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#991b1b;stop-opacity:1" />
                            </linearGradient>
                            <filter id="heartShadow">
                                <feDropShadow dx="4" dy="8" stdDeviation="8" flood-color="#000000" flood-opacity="0.3"/>
                            </filter>
                        </defs>
                       
                        <path d="M200,120 Q250,80 280,120 Q320,160 280,200 Q250,240 200,240 Q150,240 120,200 Q80,160 120,120 Q150,80 200,120Z"
                              fill="url(#heartGrad)" filter="url(#heartShadow)" class="beat"/>
                       
                        <ellipse cx="170" cy="140" rx="25" ry="35" fill="#f87171" opacity="0.8" id="right-atrium"/>
                        <ellipse cx="230" cy="140" rx="25" ry="35" fill="#f87171" opacity="0.8" id="left-atrium"/>
                        <ellipse cx="170" cy="190" rx="30" ry="25" fill="#ef4444" opacity="0.9" id="right-ventricle"/>
                        <ellipse cx="230" cy="190" rx="30" ry="25" fill="#ef4444" opacity="0.9" id="left-ventricle"/>
                       
                        <text x="170" y="135" text-anchor="middle" fill="white" font-size="10" font-weight="bold">RA</text>
                        <text x="230" y="135" text-anchor="middle" fill="white" font-size="10" font-weight="bold">LA</text>
                        <text x="170" y="195" text-anchor="middle" fill="white" font-size="10" font-weight="bold">RV</text>
                        <text x="230" y="195" text-anchor="middle" fill="white" font-size="10" font-weight="bold">LV</text>
                    </svg>
                `,
                subparts: [
                    {
                        id: 'right_atrium',
                        name: 'Right Atrium',
                        number: 1,
                        description: 'Receives deoxygenated blood from systemic circulation',
                        detailed_description: 'The right atrium is the thin-walled, quadrilateral-shaped chamber forming the right border of the heart. It receives deoxygenated blood from the entire body through major venous systems.',
                        fun_fact: 'Processes the entire blood volume every minute!',
                        function: 'Systemic venous blood reception',
                        clinical_importance: 'Site for pacemaker implantation and central venous access',
                        color: '#FF6B6B',
                        dimensions: '4-5 cm diameter, 2-3 mm wall thickness',
                        model_section: `
                            <style>
                                @keyframes highlightRA {
                                    0%, 100% { fill: #f87171; opacity: 0.8; }
                                    50% { fill: #fef3c7; opacity: 1; stroke: #d97706; stroke-width: 3; }
                                }
                                #right-atrium {
                                    animation: highlightRA 2s infinite;
                                }
                            </style>
                        `
                    },
                    {
                        id: 'left_ventricle',
                        name: 'Left Ventricle',
                        number: 2,
                        description: 'Generates high-pressure systemic blood flow',
                        detailed_description: 'The left ventricle is the dominant cardiac chamber with thick, muscular walls designed to generate high pressures against systemic vascular resistance.',
                        fun_fact: 'Works 7 times harder than the right ventricle!',
                        function: 'Systemic circulation pump',
                        clinical_importance: 'Primary determinant of cardiac output',
                        color: '#FF8E8E',
                        dimensions: '10-15 mm wall thickness',
                        model_section: `
                            <style>
                                @keyframes highlightLV {
                                    0%, 100% { fill: #ef4444; opacity: 0.9; }
                                    50% { fill: #fef3c7; opacity: 1; stroke: #d97706; stroke-width: 3; }
                                }
                                #left-ventricle {
                                    animation: highlightLV 2s infinite;
                                }
                            </style>
                        `
                    }
                ]
            },
            brain: {
                name: 'Brain',
                emoji: '🧠',
                description: 'The control center of your nervous system and consciousness.',
                full_description: 'The human brain is the most complex biological structure known, containing an estimated 86 billion neurons.',
                model_image: `
                    <svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="brainGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#7c3aed;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#5b21b6;stop-opacity:1" />
                            </linearGradient>
                            <filter id="brainShadow">
                                <feDropShadow dx="4" dy="8" stdDeviation="8" flood-color="#000000" flood-opacity="0.3"/>
                            </filter>
                        </defs>
                       
                        <path d="M150,150 Q120,120 150,90 Q200,60 250,90 Q280,120 250,150 Q280,180 250,210 Q200,240 150,210 Q120,180 150,150Z"
                              fill="url(#brainGrad)" filter="url(#brainShadow)" class="pulse" id="cerebrum"/>
                       
                        <path d="M180,100 Q200,80 220,100 Q230,130 210,150 Q190,150 180,130Z" fill="#8b5cf6" opacity="0.8" id="frontal-lobe"/>
                       
                        <ellipse cx="200" cy="220" rx="60" ry="25" fill="#6d28d9" opacity="0.8" id="cerebellum"/>
                       
                        <text x="200" y="110" text-anchor="middle" fill="white" font-size="8" font-weight="bold">Frontal</text>
                        <text x="200" y="220" text-anchor="middle" fill="white" font-size="8" font-weight="bold">Cerebellum</text>
                    </svg>
                `,
                subparts: [
                    {
                        id: 'frontal_lobe',
                        name: 'Frontal Lobe',
                        number: 1,
                        description: 'Executive functions, planning, and voluntary movement',
                        detailed_description: 'The frontal lobe constitutes the anterior third of each cerebral hemisphere, responsible for executive functions and voluntary movement.',
                        fun_fact: 'Accounts for 41% of total cerebral cortex volume!',
                        function: 'Executive control and movement',
                        clinical_importance: 'Site of personality and judgment centers',
                        color: '#A78BFA',
                        dimensions: 'Largest cerebral lobe',
                        model_section: `
                            <style>
                                @keyframes highlightFrontal {
                                    0%, 100% { fill: #8b5cf6; opacity: 0.8; }
                                    50% { fill: #fef3c7; opacity: 1; stroke: #d97706; stroke-width: 2; }
                                }
                                #frontal-lobe {
                                    animation: highlightFrontal 2s infinite;
                                }
                            </style>
                        `
                    }
                ]
            }
        };
       
        const organData = demoData[organ] || demoData.heart;
        this.showOrganInfo(organData);
        this.display3DModel(organData);
        this.currentOrgan = organData;
    }

    async loadOrganLibrary() {
        try {
            const response = await fetch('/api/organs');
            const organs = await response.json();
            this.showOrganLibrary(organs);
        } catch (error) {
            console.error('Failed to load organs:', error);
            this.showDemoOrganLibrary();
        }
    }

    showOrganLibrary(organs) {
        const grid = document.getElementById('organ-grid');
        grid.innerHTML = '';

        organs.forEach(organ => {
            const item = document.createElement('div');
            item.className = 'organ-item';
            item.innerHTML = `
                <div style="width: 80px; height: 80px; background: #dbeafe; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 32px;">
                    ${organ.emoji}
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-2">${organ.name}</h3>
                <p class="text-sm text-gray-600 mb-3">${organ.system}</p>
                <p class="text-xs text-gray-500 mb-4">${organ.description}</p>
                <button class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                    Explore in 3D
                </button>
            `;
            item.addEventListener('click', () => {
                this.selectOrgan(organ);
            });
            grid.appendChild(item);
        });
    }

    showDemoOrganLibrary() {
        const demoOrgans = [
            {
                id: 'heart',
                name: 'Heart',
                emoji: '❤️',
                system: 'Cardiovascular System',
                description: 'Blood pumping organ',
                animation: 'beat'
            },
            {
                id: 'brain',
                name: 'Brain',
                emoji: '🧠',
                system: 'Nervous System',
                description: 'Control center',
                animation: 'pulse'
            },
            {
                id: 'lungs',
                name: 'Lungs',
                emoji: '🫁',
                system: 'Respiratory System',
                description: 'Breathing organs',
                animation: 'breathe'
            },
            {
                id: 'liver',
                name: 'Liver',
                emoji: '🟫',
                system: 'Digestive System',
                description: 'Detox organ',
                animation: 'pulse'
            }
        ];
        this.showOrganLibrary(demoOrgans);
    }

    selectOrgan(organ) {
        this.showSection('scan');
        this.showResults({
            success: true,
            part: organ.id,
            confidence: 0.95,
            model_id: organ.id
        });
    }

    toggleAccessibility() {
        // Toggle high contrast mode
        document.body.classList.toggle('high-contrast');
        alert('Accessibility features toggled');
    }

    showSettings() {
        alert('Settings panel coming soon!');
    }

    showError(message) {
        // Create a nice error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'fixed top-4 right-4 bg-red-500 text-white p-4 rounded-lg shadow-lg z-50';
        errorDiv.innerHTML = `
            <div class="flex items-center">
                <span class="text-xl mr-2">❌</span>
                <span>${message}</span>
            </div>
        `;
        document.body.appendChild(errorDiv);
       
        // Remove after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
}

// Start the app when page loads
document.addEventListener('DOMContentLoaded', function() {
    window.app = new ScanSpectrumApp();
    console.log('🌟 Scan Spectrum App Loaded Successfully!');
})