// ==========================================
// Logika Pindah Halaman (SPA)
// ==========================================
function showPage(pageId) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}

// ==========================================
// Logika Tampilan 2D Basket (Coaching Board)
// ==========================================
const canvas = document.getElementById('fieldCanvas');
const ctx = canvas.getContext('2d');

function drawBasketballCourt() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#1e1e1e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#ffffff'; 
    ctx.lineWidth = 3;

    const margin = 20;
    const w = canvas.width - (margin * 2);
    const h = canvas.height - (margin * 2);

    ctx.strokeRect(margin, margin, w, h);

    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, margin);
    ctx.lineTo(canvas.width / 2, canvas.height - margin);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 40, 0, Math.PI * 2);
    ctx.stroke();

    ctx.strokeRect(margin, (canvas.height/2) - 60, 130, 120);
    ctx.beginPath();
    ctx.moveTo(margin + 10, (canvas.height/2) - 20);
    ctx.lineTo(margin + 10, (canvas.height/2) + 20);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.arc(margin + 25, canvas.height/2, 10, 0, Math.PI * 2);
    ctx.strokeStyle = '#ff8c00'; 
    ctx.stroke();
    
    ctx.strokeStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(margin, canvas.height/2, 180, -Math.PI/2.5, Math.PI/2.5);
    ctx.stroke();

    ctx.strokeRect(canvas.width - margin - 130, (canvas.height/2) - 60, 130, 120);
    ctx.beginPath();
    ctx.moveTo(canvas.width - margin - 10, (canvas.height/2) - 20);
    ctx.lineTo(canvas.width - margin - 10, (canvas.height/2) + 20);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.arc(canvas.width - margin - 25, canvas.height/2, 10, 0, Math.PI * 2);
    ctx.strokeStyle = '#ff8c00'; 
    ctx.stroke();

    ctx.strokeStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(canvas.width - margin, canvas.height/2, 180, Math.PI - Math.PI/2.5, Math.PI + Math.PI/2.5);
    ctx.stroke();
}

// ==========================================
// Logika Integrasi WebSocket dengan Python (AI)
// ==========================================

let players = [];
const ws = new WebSocket("ws://localhost:8765");

ws.onmessage = function(event) {
    players = JSON.parse(event.data);
};

function renderMap() {
    drawBasketballCourt();

    players.forEach(player => {
        ctx.beginPath();
        ctx.arc(player.x, player.y, 10, 0, Math.PI * 2);
        
        // Logika pewarnaan tim
        if (player.team === "TimBiru") {
            ctx.fillStyle = '#0066cc'; // Biru Warriors
        } else {
            ctx.fillStyle = '#fdb927'; // Kuning Lakers
        }
        
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();
    });

    requestAnimationFrame(renderMap);
}

renderMap();