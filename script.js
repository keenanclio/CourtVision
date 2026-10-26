// ==========================================
// Logika Pindah Halaman (Single Page App)
// ==========================================
function showPage(event, pageId) {
    if (event) {
        event.preventDefault(); // Mencegah reload / scroll otomatis browser
    }
    
    // Sembunyikan semua halaman
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        page.classList.remove('active');
    });

    // Tampilkan halaman yang dipilih
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
    }
}

// ==========================================
// Menggambar Lapangan Basket 2D
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

    // Garis Luar Lapangan
    ctx.strokeRect(margin, margin, w, h);

    // Garis & Lingkaran Tengah
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, margin);
    ctx.lineTo(canvas.width / 2, canvas.height - margin);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 40, 0, Math.PI * 2);
    ctx.stroke();

    // Area Ring Kiri
    ctx.strokeRect(margin, (canvas.height/2) - 60, 130, 120);
    ctx.beginPath();
    ctx.arc(margin + 25, canvas.height/2, 10, 0, Math.PI * 2);
    ctx.strokeStyle = '#ff8c00'; 
    ctx.stroke();
    
    ctx.strokeStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(margin, canvas.height/2, 180, -Math.PI/2.5, Math.PI/2.5);
    ctx.stroke();

    // Area Ring Kanan
    ctx.strokeRect(canvas.width - margin - 130, (canvas.height/2) - 60, 130, 120);
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
// Logika WebSocket (Pemain Real-Time)
// ==========================================
let players = [];

function connectWebSocket() {
    const ws = new WebSocket("ws://localhost:8765");

    ws.onopen = function() {
        console.log("✅ WebSocket terhubung ke Python AI!");
    };

    ws.onmessage = function(event) {
        try {
            players = JSON.parse(event.data);
        } catch (e) {
            console.error("Gagal membaca data WebSocket:", e);
        }
    };

    ws.onclose = function() {
        console.log("⚠️ Server AI terputus. Mencoba terhubung kembali...");
        setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = function(err) {
        ws.close();
    };
}

// Jalankan WebSocket
connectWebSocket();

// Loop Render Animasi Map
function renderMap() {
    drawBasketballCourt();

    players.forEach(player => {
        ctx.beginPath();
        ctx.arc(player.x, player.y, 10, 0, Math.PI * 2);
        
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

// Jalankan Rendering
renderMap();
