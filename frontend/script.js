const board = document.getElementById("board");
const pieceContainer = document.getElementById("piece-container");
const currentTurnDisplay = document.getElementById("current-turn");

let currentPlayer = 1;
let hoveredPiece = null;
let hoveredPieceDiv = null;

const API_BASE_URL = "http://127.0.0.1:5000";
const API_GET_PIECES = `${API_BASE_URL}/get_pieces`;
const API_ROTATE_KEYPRESS = `${API_BASE_URL}/rotate_piece_keypress`;
const API_PLACE_PIECE = `${API_BASE_URL}/place_piece`;
const API_GET_BOARD = `${API_BASE_URL}/get_board`;

/**
 * Initialize the board as a 20x20 grid.
 */
 const initializeBoard = async () => {
    board.innerHTML = "";
    for (let i = 0; i < 20; i++) {
        for (let j = 0; j < 20; j++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.dataset.row = i;
            cell.dataset.col = j;

            cell.addEventListener("dragover", (e) => e.preventDefault());
            cell.addEventListener("drop", (e) => handleDrop(e, cell));

            // ✅ Add hover preview events
            cell.addEventListener("dragenter", (e) => handleHover(e, cell));
            cell.addEventListener("dragleave", clearHover);

            board.appendChild(cell);
        }
    }
    await updateBoardState();
};

/**
 * Handle hovering over a board cell to show placement preview.
 */
const handleHover = (e, cell) => {
    if (!hoveredPiece || !hoveredPieceDiv) return;

    // Clear previous highlights
    document.querySelectorAll(".preview").forEach((cell) => {
        cell.classList.remove("preview");
    });

    const startX = parseInt(cell.dataset.row);
    const startY = parseInt(cell.dataset.col);
    const pieceShape = JSON.parse(hoveredPieceDiv.dataset.shape);

    // ✅ Apply the highlight effect on the board based on the piece shape
    pieceShape.forEach((row, i) => {
        row.forEach((cellValue, j) => {
            if (cellValue === 1) {
                const targetCell = document.querySelector(
                    `.cell[data-row="${startX + i}"][data-col="${startY + j}"]`
                );
                if (targetCell) {
                    targetCell.classList.add("preview");
                }
            }
        });
    });
};

/**
 * Handle removing the placement preview when no longer hovering.
 */
const clearHover = () => {
    document.querySelectorAll(".preview").forEach((cell) => {
        cell.classList.remove("preview");
    });
};

/**
 * Fetch and render the board state.
 */
const updateBoardState = async () => {
    try {
        console.log("📡 Fetching board data...");
        const response = await fetch(API_GET_BOARD);
        if (!response.ok) throw new Error(`Failed to fetch board: ${response.statusText}`);
        
        const data = await response.json();
        console.log("✅ Board Data:", data);

        renderBoard(data.board);
        currentPlayer = data.current_player;
        currentTurnDisplay.textContent = `Current Turn: Player ${currentPlayer}`;
        await renderPieces();
    } catch (error) {
        console.error("❌ Error fetching board state:", error);
    }
};

/**
 * Fetch and render the pieces for the current player.
 */
 const renderPieces = async () => {
    pieceContainer.innerHTML = ""; // ✅ Clear existing pieces before rendering
    try {
        console.log("📡 Fetching pieces data...");
        const response = await fetch(API_GET_PIECES);
        if (!response.ok) throw new Error(`Failed to fetch pieces: ${response.statusText}`);

        const { pieces } = await response.json();
        console.log("✅ Pieces Data:", pieces);

        pieces.forEach((piece) => {
            if (!document.querySelector(`[data-piece="${piece.name}"]`)) { // ✅ Prevent duplicates
                const pieceDiv = createPieceDiv(piece);
                pieceContainer.appendChild(pieceDiv);
            }
        });
    } catch (error) {
        console.error("❌ Error fetching pieces:", error);
    }
};

/**
 * Request backend to rotate or flip a piece.
 */
const rotateOrFlipPiece = async (pieceName, action) => {
    try {
        const response = await fetch(API_ROTATE_KEYPRESS, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ piece: pieceName, action }),
        });

        if (!response.ok) throw new Error(`${action} failed`);

        const data = await response.json();
        return data.shape;
    } catch (error) {
        console.error(`❌ Error ${action}ing piece:`, error);
        return null;
    }
};

/**
 * Handle rotation ('r') and flip ('f') on keypress when a piece is selected.
 */
document.addEventListener("keydown", async (e) => {
    if (!hoveredPiece || !hoveredPieceDiv) return; // Ensure a piece is being hovered

    let pieceName = hoveredPieceDiv.dataset.piece;
    let action = e.key.toLowerCase() === "r" ? "rotate" : e.key.toLowerCase() === "f" ? "flip" : null;

    if (!action) return;

    try {
        let transformedPiece = await rotateOrFlipPiece(pieceName, action);
        if (transformedPiece) {
            hoveredPiece = transformedPiece;
            hoveredPieceDiv.dataset.shape = JSON.stringify(hoveredPiece);
            renderPieceVisual(hoveredPiece, hoveredPieceDiv);
        }
    } catch (error) {
        console.error(`❌ Error ${action}ing piece:`, error);
    }
});

/**
 * Create a DOM element for a game piece.
 */
const createPieceDiv = (piece) => {
    const pieceDiv = document.createElement("div");
    pieceDiv.classList.add("piece");
    pieceDiv.dataset.piece = piece.name;
    pieceDiv.dataset.shape = JSON.stringify(piece.shape);

    renderPieceVisual(piece.shape, pieceDiv);

    pieceDiv.draggable = true;
    pieceDiv.addEventListener("dragstart", (e) => {
        e.dataTransfer.setData("piece", JSON.stringify(piece));
        hoveredPiece = piece.shape;
        hoveredPieceDiv = pieceDiv;
    });

    // ✅ Update hovered piece without rotating
    pieceDiv.addEventListener("mouseover", () => {
        hoveredPiece = JSON.parse(pieceDiv.dataset.shape);
        hoveredPieceDiv = pieceDiv;
    });

    pieceDiv.addEventListener("mouseleave", () => {
        hoveredPiece = null;
        hoveredPieceDiv = null;
    });

    return pieceDiv;
};

/**
 * Render a piece's shape visually inside a div.
 */
const renderPieceVisual = (pieceShape, pieceDiv) => {
    pieceDiv.innerHTML = "";
    pieceShape.forEach((row) => {
        const rowDiv = document.createElement("div");
        rowDiv.classList.add("row");
        row.forEach((cell) => {
            const cellDiv = document.createElement("div");
            cellDiv.classList.add("cell");
            if (cell === 1) {
                cellDiv.classList.add("filled");
                cellDiv.style.backgroundImage = `url(${API_BASE_URL}/static/player_${currentPlayer}.png)`;
                cellDiv.style.backgroundSize = "cover";
            }
            rowDiv.appendChild(cellDiv);
        });
        pieceDiv.appendChild(rowDiv);
    });
};

/**
 * Initialize the game.
 */
document.addEventListener("DOMContentLoaded", () => {
    initializeBoard();
    renderPieces();
});

const handleDrop = async (event, cell) => {
    if (!hoveredPiece || !hoveredPieceDiv) {
        console.warn("⚠️ No hovered piece detected. Cannot place.");
        return;
    }

    const startX = parseInt(cell.dataset.row);
    const startY = parseInt(cell.dataset.col);
    const pieceName = hoveredPieceDiv.dataset.piece;
    const pieceShape = JSON.parse(hoveredPieceDiv.dataset.shape);

    console.log(`📡 Sending place request for ${pieceName} at (${startX}, ${startY})`);

    try {
        const response = await fetch(`${API_BASE_URL}/place_piece`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                piece: pieceName,
                shape: pieceShape,
                x: startX,
                y: startY,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("❌ Error placing piece:", errorData);
            alert(`Invalid move: ${errorData.error}`);
            return;
        }

        const result = await response.json();
        console.log("📌 [Backend Response] ->", result);

        if (result.success) {
            console.log(`📌 DEBUG: ${pieceName} successfully placed.`);

            const pieceElement = document.querySelector(`[data-piece="${pieceName}"]`);
            if (pieceElement) {
                pieceElement.remove();
            } else {
                console.warn("⚠️ Tried to remove piece, but it was already missing.");
            }

            await updateBoardState();
            await renderPieces();

            hoveredPiece = null;
            hoveredPieceDiv = null;
            clearHover();
        }
    } catch (error) {
        console.error("❌ Network error placing piece:", error);
    }
};



/**
 * Render the board UI after placing a piece.
 */
 const renderBoard = (grid) => {
    console.log("🎨 Updating board UI...");
    for (let i = 0; i < grid.length; i++) {
        for (let j = 0; j < grid[i].length; j++) {
            const cell = document.querySelector(`.cell[data-row="${i}"][data-col="${j}"]`);
            if (cell) {
                if (grid[i][j] !== 0) {
                    cell.style.backgroundImage = `url(${API_BASE_URL}/static/player_${grid[i][j]}.png)`;
                    cell.style.backgroundSize = "cover";
                } else {
                    cell.style.backgroundImage = "";
                }
            }
        }
    }
};

/**
 * End the current player's turn.
 */
const endTurn = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/end_turn`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ current_player: currentPlayer }),
        });

        if (!response.ok) throw new Error(`Failed to end turn: ${response.statusText}`);

        const data = await response.json();
        console.log("✅ Turn ended:", data);

        currentPlayer = data.next_player;
        currentTurnDisplay.textContent = `Current Turn: Player ${currentPlayer}`;
        renderBoard(data.board);
        renderPieces(data.pieces);
    } catch (error) {
        console.error("❌ Error ending turn:", error);
    }
};

document.getElementById("end-turn-button").addEventListener("click", endTurn);