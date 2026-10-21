// Fungsi untuk memindah halaman (SPA)
function showPage(pageId) {
    // Sembunyikan semua halaman
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        page.classList.remove('active');
    });

    // Tampilkan halaman yang dipilih
    document.getElementById(pageId).classList.add('active');
}

// ==========================================
// Logika Tampilan 2D (Menggambar Lapangan & Pemain)
// ==========================================
const canvas = document.getElementById('fieldCanvas');
const ctx = canvas.getContext('2d');

// Fungsi Menggambar Papan / Lapangan
function drawField() {
    // Bersihkan canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Warna dasar lapangan 
    ctx.fillStyle = '#1e1e1e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Garis batas lapangan
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.strokeRect(40, 40, canvas.width - 80, canvas.height - 80);

    // Garis tengah
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 40);
    ctx.lineTo(canvas.width / 2, canvas.height - 40);
    ctx.stroke();

    // Lingkaran tengah
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 60, 0, Math.PI * 2);
    ctx.stroke();
}

// Simulasi data pemain
// Nanti koordinat x dan y ini yang akan disuplai oleh backend (misal dari OpenCV)
let players = [
    { id: 1, x: 200, y: 150 },
    { id: 2, x: 600, y: 300 },
    { id: 3, x: 400, y: 250 },
    { id: 4, x: 250, y: 400 }
];

// Fungsi animasi pergerakan pemain
function renderMap() {
    drawField();

    // Loop untuk menggambar setiap pemain
    players.forEach(player => {
        ctx.beginPath();
        ctx.arc(player.x, player.y, 12, 0, Math.PI * 2);
        ctx.fillStyle = '#ff8c00'; // Warna titik pemain (Oranye)
        ctx.fill();
        
        ctx.strokeStyle = '#ffffff'; // Garis putih di luar titik
        ctx.lineWidth = 2;
        ctx.stroke();

        // -- Kode di bawah ini hanya simulasi agar titik bergerak --
        // Pada implementasi aslinya, titik bergerak karena koordinat x dan y diupdate dari backend
        player.x += (Math.random() - 0.5) * 4;
        player.y += (Math.random() - 0.5) * 4;

        // Mencegah titik keluar dari area garis lapangan
        if(player.x < 50) player.x = 50;
        if(player.x > canvas.width - 50) player.x = canvas.width - 50;
        if(player.y < 50) player.y = 50;
        if(player.y > canvas.height - 50) player.y = canvas.height - 50;
    });

    // Panggil fungsi ini terus-menerus untuk live streaming
    requestAnimationFrame(renderMap);
}

// Jalankan animasi tampilan 2D
renderMap();