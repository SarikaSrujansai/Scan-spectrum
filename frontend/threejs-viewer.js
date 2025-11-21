// Audio Player with TTS Support
class AudioPlayer {
    constructor() {
        this.audio = new Audio();
        this.isPlaying = false;
        this.currentTime = 0;
        this.duration = 0;
        this.playbackRate = 1.0;
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.audio.addEventListener('loadedmetadata', () => {
            this.duration = this.audio.duration;
            this.updateDurationDisplay();
        });

        this.audio.addEventListener('timeupdate', () => {
            this.currentTime = this.audio.currentTime;
            this.updateProgressBar();
            this.updateCurrentTimeDisplay();
        });

        this.audio.addEventListener('ended', () => {
            this.isPlaying = false;
            this.updatePlayButton();
        });

        // Play/Pause button
        const playPauseBtn = document.getElementById('play-pause-btn');
        if (playPauseBtn) {
            playPauseBtn.addEventListener('click', () => this.togglePlay());
        }

        // Speed control
        const speedControl = document.getElementById('speed-control');
        if (speedControl) {
            speedControl.addEventListener('change', (e) => {
                this.setPlaybackRate(parseFloat(e.target.value));
            });
        }

        // Progress bar click
        const progressContainer = document.querySelector('#progress-bar')?.parentElement;
        if (progressContainer) {
            progressContainer.addEventListener('click', (e) => {
                const rect = progressContainer.getBoundingClientRect();
                const percent = (e.clientX - rect.left) / rect.width;
                this.seekTo(percent * this.duration);
            });
        }
    }

    async loadAudio(audioUrl, textContent) {
        try {
            // For demo, we'll use browser TTS
            if (textContent) {
                await this.generateTTS(textContent);
                return true;
            }
           
            // If URL provided, load it
            if (audioUrl) {
                this.audio.src = audioUrl;
                return true;
            }
           
            return false;
        } catch (error) {
            console.error('Error loading audio:', error);
            return false;
        }
    }

    async generateTTS(text) {
        return new Promise((resolve) => {
            if ('speechSynthesis' in window) {
                // Stop any current speech
                window.speechSynthesis.cancel();
               
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.8;
                utterance.pitch = 1;
                utterance.volume = 0.8;
               
                utterance.onend = () => {
                    this.isPlaying = false;
                    this.updatePlayButton();
                    resolve();
                };
               
                utterance.onstart = () => {
                    this.isPlaying = true;
                    this.updatePlayButton();
                };
               
                window.speechSynthesis.speak(utterance);
            } else {
                console.warn('TTS not supported in this browser');
                resolve();
            }
        });
    }

    togglePlay() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
            window.speechSynthesis.resume();
        } else {
            this.audio.play().catch(e => console.error('Audio play failed:', e));
        }
        this.isPlaying = true;
        this.updatePlayButton();
    }

    pause() {
        if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
            window.speechSynthesis.pause();
        } else {
            this.audio.pause();
        }
        this.isPlaying = false;
        this.updatePlayButton();
    }

    seekTo(time) {
        this.audio.currentTime = time;
    }

    setPlaybackRate(rate) {
        this.playbackRate = rate;
        this.audio.playbackRate = rate;
       
        if ('speechSynthesis' in window) {
            // Note: speechSynthesis rate might not be supported in all browsers
            const utterances = window.speechSynthesis.getVoices();
            // Rate adjustment for TTS would need to be handled differently
        }
    }

    updatePlayButton() {
        const button = document.getElementById('play-pause-btn');
        if (button) {
            button.innerHTML = this.isPlaying ? '⏸️' : '▶';
        }
    }

    updateProgressBar() {
        const progressBar = document.getElementById('progress-bar');
        if (progressBar && this.duration > 0) {
            const progress = (this.currentTime / this.duration) * 100;
            progressBar.style.width = `${progress}%`;
        }
    }

    updateCurrentTimeDisplay() {
        const element = document.getElementById('current-time');
        if (element) {
            element.textContent = this.formatTime(this.currentTime);
        }
    }

    updateDurationDisplay() {
        const element = document.getElementById('duration');
        if (element) {
            element.textContent = this.formatTime(this.duration);
        }
    }

    formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
       
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    // Demo method to play sample narration
    playDemoNarration(subpartName) {
        const demoText = `Hello! Let's learn about the ${subpartName}. This is a demo narration. In the full version, you would hear a detailed 5-10 minute explanation about this body part, including its structure, function, and interesting facts.`;
       
        this.generateTTS(demoText);
    }