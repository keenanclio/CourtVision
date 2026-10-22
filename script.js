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
    // Background gelap
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#1e1e1e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#ffffff'; // Warna garis lapangan
    ctx.lineWidth = 3;

    const margin = 20;
    const w = canvas.width - (margin * 2);
    const h = canvas.height - (margin * 2);

    // Garis luar lapangan basket
    ctx.strokeRect(margin, margin, w, h);

    // Garis tengah (Half-court)
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, margin);
    ctx.lineTo(canvas.width / 2, canvas.height - margin);
    ctx.stroke();

    // Lingkaran tengah
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 40, 0, Math.PI * 2);
    ctx.stroke();

    // -- Area Kiri (Left Court) --
    // Paint Area (Key) Kiri
    ctx.strokeRect(margin, (canvas.height/2) - 60, 130, 120);
    // Ring dan Backboard Kiri
    ctx.beginPath();
    ctx.moveTo(margin + 10, (canvas.height/2) - 20);
    ctx.lineTo(margin + 10, (canvas.height/2) + 20);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(margin + 25, canvas.height/2, 10, 0, Math.PI * 2);
    ctx.strokeStyle = '#ff8c00'; // Ring warna oranye
    ctx.stroke();
    
    // Garis Three-Point Kiri
    ctx.strokeStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(margin, canvas.height/2, 180, -Math.PI/2.5, Math.PI/2.5);
    ctx.stroke();

    // -- Area Kanan (Right Court) --
    // Paint Area (Key) Kanan
    ctx.strokeRect(canvas.width - margin - 130, (canvas.height/2) - 60, 130, 120);
    // Ring dan Backboard Kanan
    ctx.beginPath();
    ctx.moveTo(canvas.width - margin - 10, (canvas.height/2) - 20);
    ctx.lineTo(canvas.width - margin - 10, (canvas.height/2) + 20);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(canvas.width - margin - 25, canvas.height/2, 10, 0, Math.PI * 2);
    ctx.strokeStyle = '#ff8c00'; // Ring warna oranye
    ctx.stroke();

    // Garis Three-Point Kanan
    ctx.strokeStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(canvas.width - margin, canvas.height/2, 180, Math.PI - Math.PI/2.5, Math.PI + Math.PI/2.5);
    ctx.stroke();
}

// Simulasi data pemain bergerak di lapangan
let players = [
    { id: 1, x: 200, y: 150 },
    { id: 2, x: 600, y: 300 },
    { id: 3, x: 400, y: 250 },
    { id: 4, x: 250, y: 350 },
    { id: 5, x: 500, y: 100 }
];

function renderMap() {
    drawBasketballCourt();

    players.forEach(player => {
        ctx.beginPath();
        ctx.arc(player.x, player.y, 10, 0, Math.PI * 2);
        ctx.fillStyle = '#ff8c00'; // Titik pemain
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Simulasi pergerakan (nantinya ini diganti dengan data OpenCV kamu)
        player.x += (Math.random() - 0.5) * 5;
        player.y += (Math.random() - 0.5) * 5;

        // Batas agar tidak keluar kanvas
        if(player.x < 30) player.x = 30;
        if(player.x > canvas.width - 30) player.x = canvas.width - 30;
        if(player.y < 30) player.y = 30;
        if(player.y > canvas.height - 30) player.y = canvas.height - 30;
    });

    requestAnimationFrame(renderMap);
}

renderMap();
