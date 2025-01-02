
document.addEventListener('DOMContentLoaded', function() {
    // Favicon eklemek
    var link = document.createElement('link');
    link.rel = 'icon';
    link.href = 'https://upload.wikimedia.org/wikipedia/commons/9/95/Instagram_logo_2022.svg'; // Instagram favicon linki
    link.type = 'image/svg+xml';
    document.head.appendChild(link);

    // Formu dinleme ve medya işleme
    document.getElementById('url-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const mediaUrl = document.getElementById('media-url').value.trim();
        if (mediaUrl) {
            // Burada API veya uygun bir işleme yapılabilir.
            // Simülasyon olarak sabit bir indirme linki kullanıyoruz.
            const downloadUrl = "https://example.com/download?media=" + encodeURIComponent(mediaUrl);

            // Medya cevabını göster
            document.getElementById('response-section').style.display = 'block';
            document.getElementById('download-link').href = downloadUrl;
            document.getElementById('media-content').innerHTML = `
                <p>Video veya fotoğraf başarıyla tespit edildi!</p>
                <p><strong>Medya Linki:</strong> ${mediaUrl}</p>
            `;
        } else {
            alert('Lütfen geçerli bir Instagram linki girin.');
        }
    });
});
