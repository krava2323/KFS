const canvas = document.getElementById('simulationCanvas'); //  доступ до canvas 
const ctx = canvas.getContext('2d'); // 2D малюванн
const GRID_SIZE = 200; //  розмір сітки 
const CELL_SIZE = 4;   // розмір  в пікселях клітинки 

// встановлення розмірів canvas
canvas.width = GRID_SIZE * CELL_SIZE;
canvas.height = GRID_SIZE * CELL_SIZE;

const EMPTY = 0;   // порожня клітина
const TREE = 1;    // клітина з деревом
const BURNING = 2; // клітина горить

const COLORS = {
    [EMPTY]: '#2B2B2B',   
    [TREE]: '#228B22',    
    [BURNING]: '#FF4500'  
};

const pBurnSlider = document.getElementById('pBurn');
const tBurnSlider = document.getElementById('tBurn');
const pBurnValueSpan = document.getElementById('pBurnValue'); //  відображення ймовірності заг
const tBurnValueSpan = document.getElementById('tBurnValue'); //  відображення часу горіння 
const resetButton = document.getElementById('resetButton');

let pBurn = parseFloat(pBurnSlider.value); // ймовірність загоряння дерева від сусіднього вогню
let tBurn = parseInt(tBurnSlider.value);   // час горіння клітини до того як вона згорить 

let grid;      //  масив, що зберігає стан кожної клітини
let burnTimer; //  масив, що зберігає, скільки кроків клітина вже горить

// ініціалізація  таймерів горіння
function initializeGrid() {
    // створюємо сітку яка заповнену деревами
    grid = Array.from({ length: GRID_SIZE }, () => new Array(GRID_SIZE).fill(TREE));
    burnTimer = Array.from({ length: GRID_SIZE }, () => new Array(GRID_SIZE).fill(0));
    
    //  початкова пожежу в центрі сітки
    const center = Math.floor(GRID_SIZE / 2);
    grid[center][center] = BURNING;
    burnTimer[center][center] = 1; 
}

// oновлення  симуляції на один крок
function update() {
    const newGrid = grid.map(arr => arr.slice());

    for (let r = 0; r < GRID_SIZE; r++) { // проходимо по рядках
        for (let c = 0; c < GRID_SIZE; c++) { // проходимо по стовпцях
            
            // встановлюєсо так щоб клітина яка горить з часом згорала та змінювала стан
            if (grid[r][c] === BURNING) {
                burnTimer[r][c]++; // більшуємо час горіння для цієї клітини
                if (burnTimer[r][c] > tBurn) { 
                    newGrid[r][c] = EMPTY; 
                }
            }
            
            // встановлюємо загорання від сусідніх палаюих клітинок
            if (grid[r][c] === TREE) {
                let burningNeighbors = 0; // лічильник палаючих сусідів
                for (let dr = -1; dr <= 1; dr++) {
                    for (let dc = -1; dc <= 1; dc++) {
                        if (dr === 0 && dc === 0) continue; 
                        const nr = r + dr; 
                        const nc = c + dc;
                        // перевіряємо чи сусід в межах сітки і чи він горить
                        if (nr >= 0 && nr < GRID_SIZE && nc >= 0 && nc < GRID_SIZE && grid[nr][nc] === BURNING) {
                            burningNeighbors++;
                        }
                    }
                }

                if (burningNeighbors > 0) { //  є один палаючий сусід
                    const ignitionProb = 1 - Math.pow(1 - pBurn, burningNeighbors);
                    if (Math.random() < ignitionProb) { 
                        newGrid[r][c] = BURNING; //  загоряється
                        burnTimer[r][c] = 1;     //  відлік часу горіння
                    }
                }
            }
        } 
    } 
    grid = newGrid; 
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let r = 0; r < GRID_SIZE; r++) {
        for (let c = 0; c < GRID_SIZE; c++) {
            ctx.fillStyle = COLORS[grid[r][c]];
            ctx.fillRect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        }
    }
}

//  цикл симуляції
function simulationLoop() {
    update(); // оновлюємо логіку
    draw();   // зображення результату
    requestAnimationFrame(simulationLoop); 
}

pBurnSlider.addEventListener('input', (e) => {
    pBurn = parseFloat(e.target.value); // оновлюємо значення pBurn
    pBurnValueSpan.textContent = pBurn;   // даємо нове значення користувачу
});

tBurnSlider.addEventListener('input', (e) => {
    tBurn = parseInt(e.target.value);   // оновлюємо значення tBurn
    tBurnValueSpan.textContent = tBurn; // даємо нове значення користувачу
});

resetButton.addEventListener('click', initializeGrid); 
// запуск симуляції 
initializeGrid();   //  початковий стан
simulationLoop();   //  головний цикл
