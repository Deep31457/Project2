// Global variables
let currentQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = [];
let currentScore = 0;
let quizStartTime = null;

// DOM elements
const navTabs = document.querySelectorAll('.nav-tab');
const tabContents = document.querySelectorAll('.tab-content');
const loadingOverlay = document.getElementById('loading-overlay');
const notification = document.getElementById('notification');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadCategories();
    loadLeaderboard();
    loadAdminData();
});

// Initialize the application
function initializeApp() {
    // Show home tab by default
    switchTab('home');
    
    // Update range input display
    const rangeInput = document.getElementById('num-questions');
    if (rangeInput) {
        updateRangeValue(rangeInput);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Navigation tabs
    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            switchTab(tabName);
        });
    });

    // Start quiz button
    document.getElementById('start-quiz-btn')?.addEventListener('click', () => {
        switchTab('quiz');
    });

    // Quiz form
    document.getElementById('quiz-form')?.addEventListener('submit', handleQuizSetup);

    // Range input
    document.getElementById('num-questions')?.addEventListener('input', function() {
        updateRangeValue(this);
    });

    // Quiz navigation buttons
    document.getElementById('next-question-btn')?.addEventListener('click', nextQuestion);
    document.getElementById('finish-quiz-btn')?.addEventListener('click', finishQuiz);

    // Results buttons
    document.getElementById('new-quiz-btn')?.addEventListener('click', () => {
        resetQuiz();
        switchTab('quiz');
    });
    document.getElementById('view-details-btn')?.addEventListener('click', toggleDetailedResults);

    // Leaderboard refresh
    document.getElementById('refresh-leaderboard-btn')?.addEventListener('click', loadLeaderboard);

    // Admin form
    document.getElementById('add-question-form')?.addEventListener('submit', handleAddQuestion);

    // Admin filters
    document.getElementById('filter-category')?.addEventListener('change', filterQuestions);
    document.getElementById('filter-difficulty')?.addEventListener('change', filterQuestions);

    // Notification close
    document.querySelector('.notification-close')?.addEventListener('click', hideNotification);
}

// Tab switching functionality
function switchTab(tabName) {
    // Update navigation
    navTabs.forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === tabName);
    });

    // Update content
    tabContents.forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });

    // Load data for specific tabs
    if (tabName === 'leaderboard') {
        loadLeaderboard();
    } else if (tabName === 'admin') {
        loadAdminData();
    }
}

// Utility functions
function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

function showNotification(message, type = 'info') {
    const notificationText = notification.querySelector('.notification-text');
    notificationText.textContent = message;
    
    notification.className = `notification ${type}`;
    notification.classList.remove('hidden');
    
    setTimeout(() => {
        hideNotification();
    }, 5000);
}

function hideNotification() {
    notification.classList.add('hidden');
}

function updateRangeValue(input) {
    const value = input.value;
    const rangeValue = document.querySelector('.range-value');
    if (rangeValue) {
        rangeValue.textContent = `${value} questions`;
    }
}

// API functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.error || 'API call failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        showNotification(error.message, 'error');
        throw error;
    }
}

// Load categories for dropdowns
async function loadCategories() {
    try {
        const data = await apiCall('/api/categories');
        
        // Update quiz category dropdown
        const categorySelect = document.getElementById('category');
        if (categorySelect) {
            categorySelect.innerHTML = '<option value="">Select a category</option>';
            
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.name;
                option.textContent = `${category.name} (${category.count} questions)`;
                categorySelect.appendChild(option);
            });
            
            // Add Random Mix option
            const randomOption = document.createElement('option');
            randomOption.value = 'Random Mix';
            randomOption.textContent = 'Random Mix (All categories)';
            categorySelect.appendChild(randomOption);
        }

        // Update admin category dropdown
        const adminCategorySelect = document.getElementById('admin-category');
        if (adminCategorySelect) {
            adminCategorySelect.innerHTML = '<option value="">Select category</option>';
            
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.name;
                option.textContent = category.name;
                adminCategorySelect.appendChild(option);
            });
        }

        // Update filter dropdowns
        const filterCategorySelect = document.getElementById('filter-category');
        if (filterCategorySelect) {
            filterCategorySelect.innerHTML = '<option value="">All Categories</option>';
            
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.name;
                option.textContent = category.name;
                filterCategorySelect.appendChild(option);
            });
        }
        
    } catch (error) {
        console.error('Failed to load categories:', error);
    }
}

// Quiz functionality
async function handleQuizSetup(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const quizConfig = {
        player_name: formData.get('player-name') || document.getElementById('player-name').value,
        category: formData.get('category') || document.getElementById('category').value,
        difficulty: formData.get('difficulty') || document.getElementById('difficulty').value,
        num_questions: parseInt(formData.get('num-questions') || document.getElementById('num-questions').value)
    };

    if (!quizConfig.player_name || !quizConfig.category) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }

    try {
        showLoading();
        const data = await apiCall('/api/start-quiz', {
            method: 'POST',
            body: JSON.stringify(quizConfig)
        });

        currentQuestions = data.questions;
        currentQuestionIndex = 0;
        userAnswers = [];
        currentScore = 0;
        quizStartTime = Date.now();

        // Switch to quiz playing interface
        document.getElementById('quiz-setup').classList.add('hidden');
        document.getElementById('quiz-playing').classList.remove('hidden');
        
        displayQuestion();
        hideLoading();
        
    } catch (error) {
        hideLoading();
        console.error('Failed to start quiz:', error);
    }
}

function displayQuestion() {
    if (currentQuestionIndex >= currentQuestions.length) {
        finishQuiz();
        return;
    }

    const question = currentQuestions[currentQuestionIndex];
    const questionCard = document.querySelector('.question-card');
    
    // Update progress
    const progress = ((currentQuestionIndex) / currentQuestions.length) * 100;
    document.querySelector('.progress-fill').style.width = `${progress}%`;
    document.querySelector('.question-counter').textContent = 
        `Question ${currentQuestionIndex + 1} of ${currentQuestions.length}`;
    
    // Update score
    document.querySelector('.score').textContent = `Score: ${currentScore}`;
    
    // Update question
    document.querySelector('.question-number').textContent = `Question ${currentQuestionIndex + 1}`;
    document.querySelector('.question-text').textContent = question.question;
    
    // Update options
    const optionsContainer = document.querySelector('.options-container');
    optionsContainer.innerHTML = '';
    
    question.options.forEach((option, index) => {
        const optionElement = document.createElement('div');
        optionElement.className = 'option';
        optionElement.dataset.index = index;
        
        optionElement.innerHTML = `
            <div class="option-letter">${String.fromCharCode(65 + index)}</div>
            <div class="option-text">${option}</div>
        `;
        
        optionElement.addEventListener('click', () => selectOption(index));
        optionsContainer.appendChild(optionElement);
    });
    
    // Hide/show navigation buttons
    document.getElementById('next-question-btn').classList.add('hidden');
    document.getElementById('finish-quiz-btn').classList.add('hidden');
}

function selectOption(selectedIndex) {
    // Remove previous selection
    document.querySelectorAll('.option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // Mark selected option
    const selectedOption = document.querySelector(`[data-index="${selectedIndex}"]`);
    selectedOption.classList.add('selected');
    
    // Store answer
    userAnswers[currentQuestionIndex] = selectedIndex;
    
    // Show next/finish button
    if (currentQuestionIndex < currentQuestions.length - 1) {
        document.getElementById('next-question-btn').classList.remove('hidden');
    } else {
        document.getElementById('finish-quiz-btn').classList.remove('hidden');
    }
}

function nextQuestion() {
    currentQuestionIndex++;
    displayQuestion();
}

async function finishQuiz() {
    try {
        showLoading();
        
        const data = await apiCall('/api/submit-quiz', {
            method: 'POST',
            body: JSON.stringify({ answers: userAnswers })
        });

        displayResults(data.results);
        hideLoading();
        
    } catch (error) {
        hideLoading();
        console.error('Failed to submit quiz:', error);
    }
}

function displayResults(results) {
    // Switch to results view
    document.getElementById('quiz-playing').classList.add('hidden');
    document.getElementById('quiz-results').classList.remove('hidden');
    
    // Update results display
    document.querySelector('.grade').textContent = results.grade.grade;
    document.querySelector('.grade-emoji').textContent = results.grade.emoji;
    document.getElementById('grade-message').textContent = results.grade.message;
    
    document.getElementById('final-score').textContent = results.score;
    document.getElementById('correct-answers').textContent = 
        `${results.correct_count}/${results.total_questions}`;
    document.getElementById('accuracy').textContent = `${results.accuracy.toFixed(1)}%`;
    
    // Store results for detailed view
    window.currentResults = results;
}

function toggleDetailedResults() {
    const detailedResults = document.getElementById('detailed-results');
    const isHidden = detailedResults.classList.contains('hidden');
    
    if (isHidden) {
        displayDetailedResults();
        detailedResults.classList.remove('hidden');
        document.getElementById('view-details-btn').innerHTML = 
            '<i class="fas fa-eye-slash"></i> Hide Details';
    } else {
        detailedResults.classList.add('hidden');
        document.getElementById('view-details-btn').innerHTML = 
            '<i class="fas fa-list"></i> View Detailed Results';
    }
}

function displayDetailedResults() {
    const results = window.currentResults;
    if (!results) return;
    
    const resultsList = document.querySelector('.results-list');
    resultsList.innerHTML = '';
    
    results.results.forEach((result, index) => {
        const question = currentQuestions[index];
        const resultItem = document.createElement('div');
        resultItem.className = `result-item ${result.is_correct ? 'correct' : 'incorrect'}`;
        
        const userAnswerText = question.options[result.user_answer];
        const correctAnswerText = question.options[result.correct_answer];
        
        resultItem.innerHTML = `
            <div class="result-question">${index + 1}. ${question.question}</div>
            <div class="result-answers">
                <div class="result-answer user-answer">
                    Your answer: ${String.fromCharCode(65 + result.user_answer)}. ${userAnswerText}
                </div>
                <div class="result-answer correct-answer">
                    Correct answer: ${String.fromCharCode(65 + result.correct_answer)}. ${correctAnswerText}
                </div>
            </div>
            <div class="result-explanation">${result.explanation || 'No explanation available.'}</div>
        `;
        
        resultsList.appendChild(resultItem);
    });
}

function resetQuiz() {
    // Reset all quiz state
    currentQuestions = [];
    currentQuestionIndex = 0;
    userAnswers = [];
    currentScore = 0;
    quizStartTime = null;
    
    // Reset UI
    document.getElementById('quiz-setup').classList.remove('hidden');
    document.getElementById('quiz-playing').classList.add('hidden');
    document.getElementById('quiz-results').classList.add('hidden');
    document.getElementById('detailed-results').classList.add('hidden');
    
    // Clear form
    document.getElementById('quiz-form').reset();
    updateRangeValue(document.getElementById('num-questions'));
}

// Leaderboard functionality
async function loadLeaderboard() {
    try {
        const data = await apiCall('/api/high-scores');
        displayLeaderboard(data.scores);
    } catch (error) {
        console.error('Failed to load leaderboard:', error);
        document.getElementById('leaderboard-body').innerHTML = 
            '<div class="loading">Failed to load leaderboard</div>';
    }
}

function displayLeaderboard(scores) {
    const leaderboardBody = document.getElementById('leaderboard-body');
    
    if (!scores || scores.length === 0) {
        leaderboardBody.innerHTML = '<div class="loading">No scores yet. Be the first to play!</div>';
        return;
    }
    
    leaderboardBody.innerHTML = '';
    
    scores.forEach((score, index) => {
        const row = document.createElement('div');
        row.className = 'leaderboard-row';
        
        let rankClass = '';
        if (index === 0) rankClass = 'gold';
        else if (index === 1) rankClass = 'silver';
        else if (index === 2) rankClass = 'bronze';
        
        const date = new Date(score.timestamp).toLocaleDateString();
        
        row.innerHTML = `
            <span class="rank ${rankClass}">${index + 1}</span>
            <span>${score.name}</span>
            <span>${score.score}</span>
            <span>${score.accuracy.toFixed(1)}%</span>
            <span>${score.category}</span>
            <span>${score.difficulty}</span>
            <span>${date}</span>
        `;
        
        leaderboardBody.appendChild(row);
    });
}

// Admin functionality
async function loadAdminData() {
    await Promise.all([
        loadStats(),
        loadQuestions(),
        loadCategories()
    ]);
}

async function loadStats() {
    try {
        const data = await apiCall('/api/stats');
        displayStats(data.stats);
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

function displayStats(stats) {
    document.getElementById('total-questions').textContent = stats.total_questions;
    document.getElementById('total-categories').textContent = stats.total_categories;
    
    const avgPerCategory = stats.total_categories > 0 ? 
        Math.round(stats.total_questions / stats.total_categories) : 0;
    document.getElementById('avg-per-category').textContent = avgPerCategory;
}

async function loadQuestions() {
    try {
        const data = await apiCall('/api/questions');
        window.allQuestions = data.questions;
        displayQuestions(data.questions);
    } catch (error) {
        console.error('Failed to load questions:', error);
        document.getElementById('questions-list').innerHTML = 
            '<div class="loading">Failed to load questions</div>';
    }
}

function displayQuestions(questions) {
    const questionsList = document.getElementById('questions-list');
    const categoryFilter = document.getElementById('filter-category').value;
    const difficultyFilter = document.getElementById('filter-difficulty').value;
    
    questionsList.innerHTML = '';
    
    Object.keys(questions).forEach(category => {
        if (categoryFilter && category !== categoryFilter) return;
        
        Object.keys(questions[category]).forEach(difficulty => {
            if (difficultyFilter && difficulty !== difficultyFilter) return;
            
            questions[category][difficulty].forEach((question, index) => {
                const questionItem = document.createElement('div');
                questionItem.className = 'question-item';
                
                questionItem.innerHTML = `
                    <button class="delete-btn" onclick="deleteQuestion('${category}', '${difficulty}', ${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                    <h4>${question.question}</h4>
                    <div class="question-meta">
                        <span class="meta-tag category">${category}</span>
                        <span class="meta-tag difficulty">${difficulty}</span>
                    </div>
                    <div class="question-options">
                        ${question.options.map((option, optIndex) => `
                            <div class="question-option ${optIndex === question.correct ? 'correct' : ''}">
                                <span>${String.fromCharCode(65 + optIndex)}.</span>
                                <span>${option}</span>
                            </div>
                        `).join('')}
                    </div>
                    ${question.explanation ? `<div class="result-explanation">${question.explanation}</div>` : ''}
                `;
                
                questionsList.appendChild(questionItem);
            });
        });
    });
    
    if (questionsList.children.length === 0) {
        questionsList.innerHTML = '<div class="loading">No questions match the current filters</div>';
    }
}

function filterQuestions() {
    if (window.allQuestions) {
        displayQuestions(window.allQuestions);
    }
}

async function handleAddQuestion(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    const questionData = {
        category: document.getElementById('admin-category').value,
        difficulty: document.getElementById('admin-difficulty').value,
        question: document.getElementById('admin-question').value,
        options: [
            document.getElementById('option-0').value,
            document.getElementById('option-1').value,
            document.getElementById('option-2').value,
            document.getElementById('option-3').value
        ],
        correct_answer: parseInt(document.getElementById('correct-answer').value),
        explanation: document.getElementById('admin-explanation').value
    };
    
    // Validate
    if (!questionData.category || !questionData.difficulty || !questionData.question) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    if (questionData.options.some(option => !option.trim())) {
        showNotification('Please fill in all answer options', 'error');
        return;
    }
    
    try {
        showLoading();
        await apiCall('/api/add-question', {
            method: 'POST',
            body: JSON.stringify(questionData)
        });
        
        showNotification('Question added successfully!', 'success');
        event.target.reset();
        
        // Reload admin data
        await loadAdminData();
        hideLoading();
        
    } catch (error) {
        hideLoading();
        console.error('Failed to add question:', error);
    }
}

async function deleteQuestion(category, difficulty, questionIndex) {
    if (!confirm('Are you sure you want to delete this question?')) {
        return;
    }
    
    try {
        showLoading();
        await apiCall('/api/delete-question', {
            method: 'POST',
            body: JSON.stringify({
                category,
                difficulty,
                question_index: questionIndex
            })
        });
        
        showNotification('Question deleted successfully!', 'success');
        
        // Reload admin data
        await loadAdminData();
        hideLoading();
        
    } catch (error) {
        hideLoading();
        console.error('Failed to delete question:', error);
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // During quiz, allow number keys to select options
    if (document.getElementById('quiz-playing').classList.contains('hidden') === false) {
        const key = event.key;
        if (['1', '2', '3', '4'].includes(key)) {
            const index = parseInt(key) - 1;
            selectOption(index);
        } else if (key === 'Enter') {
            const nextBtn = document.getElementById('next-question-btn');
            const finishBtn = document.getElementById('finish-quiz-btn');
            
            if (!nextBtn.classList.contains('hidden')) {
                nextQuestion();
            } else if (!finishBtn.classList.contains('hidden')) {
                finishQuiz();
            }
        }
    }
    
    // Global shortcuts
    if (event.ctrlKey || event.metaKey) {
        switch (event.key) {
            case '1':
                event.preventDefault();
                switchTab('home');
                break;
            case '2':
                event.preventDefault();
                switchTab('quiz');
                break;
            case '3':
                event.preventDefault();
                switchTab('leaderboard');
                break;
            case '4':
                event.preventDefault();
                switchTab('admin');
                break;
        }
    }
});