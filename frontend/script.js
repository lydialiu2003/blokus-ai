const board = document.getElementById('board');
const pieceContainer = document.getElementById('piece-container');
const currentTurnDisplay = document.getElementById('current-turn');
let currentPlayer = 1; // Start with Player 1
let hoveredPiece = null; // Track the currently hovered piece
let hoveredCellInPiece = { row: 0, col: 0 }; // Track the hovered cell within the piece

/**
 * Initialize the board as a 20x20 grid.
 */
const initializeBoard = () => {
    board.innerHTML = ''; // Clear the board
    for (let i = 0; i < 20; i++) {
        for (let j = 0; j < 20; j++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = i;
            cell.dataset.col = j;

            // Enable drag-and-drop functionality
            cell.addEventListener('dragover', (e) => e.preventDefault());
            cell.addEventListener('drop', (e) => handleDrop(e, cell));

            board.appendChild(cell);
        }
    }
};

/**
 * Fetch and render the pieces for the current player.
 */
const renderPieces = async () => {
    pieceContainer.innerHTML = ''; // Clear previous pieces
    try {
        const response = await fetch('http://127.0.0.1:5000/get_pieces');
        const { pieces } = await response.json();
        console.log("🧩 Pieces fetched:", pieces);

        pieces.forEach((piece) => {
            const pieceDiv = createPieceDiv(piece);
            pieceContainer.appendChild(pieceDiv);
        });

        if (pieces.length === 0) {
            console.warn("⚠️ No pieces available for the current player.");
        }
    } catch (error) {
        console.error("❌ Error fetching pieces:", error);
        alert("Failed to fetch pieces. Please check the backend.");
    }
};

/**
 * Create a DOM element for a game piece.
 */
const createPieceDiv = (piece) => {
    const pieceDiv = document.createElement('div');
    pieceDiv.classList.add('piece');
    pieceDiv.dataset.piece = piece.name;
    pieceDiv.dataset.shape = JSON.stringify(piece.shape);

    piece.shape.forEach((row, rowIndex) => {
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('row');

        row.forEach((cell, colIndex) => {
            const cellDiv = document.createElement('div');
            cellDiv.classList.add('cell');
            if (cell === 1) {
                cellDiv.classList.add('filled');
                cellDiv.style.backgroundImage = `url(http://127.0.0.1:5000/static/player_${currentPlayer}.png)`;
                cellDiv.style.backgroundSize = 'cover';

                cellDiv.addEventListener('mouseover', () => {
                    hoveredCellInPiece = { row: rowIndex, col: colIndex };
                });
            }
            rowDiv.appendChild(cellDiv);
        });

        pieceDiv.appendChild(rowDiv);
    });

    pieceDiv.draggable = true;
    pieceDiv.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('piece', JSON.stringify({
            name: piece.name,
            shape: piece.shape,
        }));
        hoveredPiece = piece;
        console.log(`🧩 Dragging piece: ${piece.name}`);
    });

    return pieceDiv;
};

/**
 * Handle the drop event and calculate the position.
 */
const handleDrop = (e, cell) => {
    const piece = JSON.parse(e.dataTransfer.getData('piece'));
    const hoveredGridRow = parseInt(cell.dataset.row);
    const hoveredGridCol = parseInt(cell.dataset.col);

    const startX = hoveredGridRow - hoveredCellInPiece.row;
    const startY = hoveredGridCol - hoveredCellInPiece.col;

    console.log("📌 [handleDrop] --- DEBUG INFO ---");
    console.log(`🎯 Dropped Piece: ${piece.name}`);
    console.log(`🟢 Hovered Grid Cell -> Row: ${hoveredGridRow}, Col: ${hoveredGridCol}`);
    console.log(`📍 Calculated Start Position -> X: ${startX}, Y: ${startY}`);

    const isFirstMove = currentPlayer === 1; // Replace with actual game logic
    updateBoard(piece.name, piece.shape, startX, startY, isFirstMove);
};

/**
 * Send the placement request to the backend and update the board.
 */
const updateBoard = async (pieceName, pieceShape, startX, startY, isFirstMove) => {
    try {
        const response = await fetch('http://127.0.0.1:5000/place_piece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                piece: pieceName,
                shape: pieceShape,
                x: startX,
                y: startY,
                isFirstMove,
            }),
        });

        const result = await response.json();
        console.log("📌 [updateBoard] Backend Response:", result);

        if (result.success) {
            renderBoard(result.board);

            if (result.next_player) {
                currentPlayer = result.next_player;
                currentTurnDisplay.textContent = `Current Turn: Player ${currentPlayer}`;
                renderPieces();
            } else {
                currentTurnDisplay.textContent = "Game Over!";
                alert("Game Over! No valid moves left.");
            }
        } else {
            console.error(`❌ Placement Error: ${result.error}`);
            alert(`Invalid move: ${result.error}`);
        }
    } catch (error) {
        console.error("❌ Error placing piece:", error);
        alert("Error communicating with the server.");
    }
};

/**
 * Render the game board with updated grid.
 */
const renderBoard = (grid) => {
    for (let i = 0; i < grid.length; i++) {
        for (let j = 0; j < grid[i].length; j++) {
            const cell = document.querySelector(`.cell[data-row="${i}"][data-col="${j}"]`);
            if (grid[i][j] !== 0) {
                cell.style.backgroundImage = `url(http://127.0.0.1:5000/static/player_${grid[i][j]}.png)`;
                cell.style.backgroundSize = 'cover';
            } else {
                cell.style.backgroundImage = ''; // Clear cell if empty
            }
        }
    }
};

/**
 * Initialize the game.
 */
document.addEventListener('DOMContentLoaded', () => {
    initializeBoard();
    renderPieces();
    currentTurnDisplay.textContent = `Current Turn: Player ${currentPlayer}`;
});
