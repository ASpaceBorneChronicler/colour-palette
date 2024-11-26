document.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('image-preview');
    const fileInput = document.getElementById('imageUpload');
    const colorPalette = document.getElementById('color-palette');
    const copiedAlert = document.getElementById('copied-alert');

    // Image preview
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                imageUpload.src = event.target.result;
                imageUpload.classList.remove('hide')
                
                // Upload image and get colors
                uploadImage(file);
            }
            reader.readAsDataURL(file);
        }
    });

    // Upload image and extract colors
    function uploadImage(file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(colors => {
            // Clear existing palette
            colorPalette.innerHTML = '';
            
            // Create new color items
            colors.forEach(color => {
                const colorItem = document.createElement('div');
                colorItem.className = 'color-list__item';
                
                colorItem.innerHTML = `
                    <div class="color-list__color" style="background: ${color.hex};"></div>
                    <div class="color-list__desc">
                        <div class="color-list__color-value hex-value" title="Copy color">
                            <span>HEX:</span>
                            <span>${color.hex}</span>
                        </div>
                        <div class="color-list__color-value rgb-value" title="Copy color">
                            <span>RGB:</span>
                            <span>${convertHexToRGB(color.hex)}</span>
                        </div>
                    </div>
                `;
                
                colorPalette.appendChild(colorItem);
            });

            // Scroll to a Image
            imageUpload.scrollIntoView({ behavior: 'smooth', block: 'start' });


            // Add copy functionality
            addCopyListeners();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to process image');
        });
    }

    // Convert hex to RGB
    function convertHexToRGB(hex) {
        // Remove # if present
        hex = hex.replace('#', '');
        
        // Convert hex to RGB
        const r = parseInt(hex.substring(0, 2), 16);
        const g = parseInt(hex.substring(2, 4), 16);
        const b = parseInt(hex.substring(4, 6), 16);
        
        return `${r}, ${g}, ${b}`;
    }

    // Add copy to clipboard listeners
    function addCopyListeners() {
        const colorValues = document.querySelectorAll('.color-list__color-value');
        
        colorValues.forEach(valueEl => {
            valueEl.addEventListener('click', function() {
                const colorText = this.querySelector('span:last-child').textContent;
                
                // Copy to clipboard
                navigator.clipboard.writeText(colorText).then(function() {
                    // Show copied alert
                    copiedAlert.innerText = `Copied ${colorText} to clipboard`;
                    copiedAlert.style.display = 'block';
                    setTimeout(() => {
                        copiedAlert.style.display = 'none';
                    }, 2000);
                });
            });
        });
    }
});
