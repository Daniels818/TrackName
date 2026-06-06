document.addEventListener('DOMContentLoaded', () => {
    // Tabs logic for index.html
    const tabs = document.querySelectorAll('.tab');
    if (tabs.length > 0) {
        const hash = window.location.hash || '#title';
        
        function activateTab(targetId) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
            
            const tab = document.querySelector(`.tab[data-target="${targetId}"]`);
            const content = document.getElementById(targetId);
            
            if (tab && content) {
                tab.classList.add('active');
                content.style.display = 'block';
            }
        }
        
        activateTab(hash.substring(1) === 'lyrics' ? 'lyrics' : 'title');
        
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.dataset.target;
                window.location.hash = target;
                activateTab(target);
            });
        });
    }

    // History clear logic
    const historyForm = document.getElementById('history-clear-form');
    if (historyForm) {
        historyForm.addEventListener('submit', (e) => {
            if (!confirm("¿Borrar todo el historial?")) {
                e.preventDefault();
            }
        });
    }
});

async function toggleFavorite(songData, btn) {
    const isSaved = btn.classList.contains('saved');
    const endpoint = isSaved ? '/favorites/remove' : '/favorites/add';
    const originalText = btn.innerHTML;
    
    btn.disabled = true;
    btn.innerHTML = '...';
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(isSaved ? { url: songData.url } : songData)
        });
        
        if (!response.ok) throw new Error('Network error');
        
        const result = await response.json();
        
        if (result.success) {
            if (isSaved) {
                btn.classList.remove('saved');
            } else {
                btn.classList.add('saved');
            }
        }
    } catch (e) {
        alert('Hubo un error de red.');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

async function removeFavorite(url, btn) {
    if (!confirm("¿Seguro que deseas eliminar este favorito?")) return;
    
    const card = btn.closest('.card');
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '...';
    
    try {
        const response = await fetch('/favorites/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });
        
        if (!response.ok) throw new Error('Network error');
        
        const result = await response.json();
        
        if (result.success) {
            card.style.opacity = '0';
            setTimeout(() => {
                card.remove();
            }, 300);
        }
    } catch (e) {
        alert('Hubo un error de red.');
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

function handleImageError(img) {
    img.onerror = null;
    img.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60"><rect width="60" height="60" fill="%23333"/></svg>';
}

function handleDetailImageError(img) {
    img.onerror = null;
    img.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect width="200" height="200" fill="%23333"/></svg>';
}
