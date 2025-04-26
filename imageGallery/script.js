const images = [
    {
        full: 'nature.jpg',
        thumb: 'nature1.jpg',
        caption: 'Nature Scene'
    },
    {
        full: 'cityview.jpg',
        thumb: 'cityview1.jpg',
        caption: 'City View'
    },
    {
        full: 'technology.jpg',
        thumb: 'technology1.jpg',
        caption: 'Technology'
    },
    {
        full: 'wildAnimal.jpg',
        thumb: 'wildAnimal1.jpg',
        caption: 'Wild Animals'
    },
    {
        full: 'modern.jpg',
        thumb: 'modern1.jpg',
        caption: 'Modern Architecture'
    }
];

let currentIndex = 0;
const mainImage = document.querySelector('.main-image');
const caption = document.querySelector('.caption');
const thumbnailsContainer = document.querySelector('.thumbnails');

// Initialize gallery
function initGallery() {
    // Create thumbnails
    images.forEach((image, index) => {
        const thumb = document.createElement('img');
        thumb.className = 'thumbnail';
        thumb.src = image.thumb;
        thumb.alt = `Thumbnail ${index + 1}`;
        thumb.dataset.index = index;
        thumb.addEventListener('click', () => showImage(index));
        thumbnailsContainer.appendChild(thumb);
    });

    // Initial image
    showImage(currentIndex);
}

// Show selected image
function showImage(index) {
    currentIndex = index;
    mainImage.src = images[index].full;
    caption.textContent = images[index].caption;

    // Update active thumbnail
    document.querySelectorAll('.thumbnail').forEach((thumb, i) => {
        thumb.classList.toggle('active', i === index);
    });
}

// Navigation functions
function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage(currentIndex);
}

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    showImage(currentIndex);
}

// Event listeners
document.querySelector('.prev').addEventListener('click', prevImage);
document.querySelector('.next').addEventListener('click', nextImage);

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') prevImage();
    if (e.key === 'ArrowRight') nextImage();
});

// Initialize the gallery
initGallery();
