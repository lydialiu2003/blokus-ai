const board = document.getElementById("board");
const pieceContainer = document.getElementById("piece-container");
const currentTurnDisplay = document.getElementById("current-turn");

let currentPlayer = 1;
let hoveredPiece = null;
let hoveredPieceDiv = null;
let selectedPieceDiv = null;
let selectedPieceShape = null;
let selectedPieceName = null;
let offsetX = 0, offsetY = 0;

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

    clearHover();

    const startX = parseInt(cell.dataset.row);
    const startY = parseInt(cell.dataset.col);
    const pieceShape = JSON.parse(hoveredPieceDiv.dataset.shape);

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
        const response = await fetch(API_GET_BOARD);
        if (!response.ok) throw new Error(`Failed to fetch board: ${response.statusText}`);

        const data = await response.json();

        renderBoard(data.board);
        currentPlayer = data.current_player;
        currentTurnDisplay.textContent = `Current Turn: Player ${currentPlayer}`;
        await renderPieces(); // ✅ Load pieces AFTER board is loaded
    } catch (error) {
        console.error("❌ Error fetching board state:", error);
    }
};

/**
 * Render the board UI.
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
 * Fetch and render the pieces for the current player.
 */
const renderPieces = async () => {
    pieceContainer.innerHTML = "";
    try {
        const response = await fetch(API_GET_PIECES);
        if (!response.ok) throw new Error(`Failed to fetch pieces: ${response.statusText}`);

        const { pieces } = await response.json();

        pieces.forEach((piece) => {
            if (!document.querySelector(`[data-piece="${piece.name}"]`)) {
                const pieceDiv = createPieceDiv(piece);
                pieceContainer.appendChild(pieceDiv);
            }
        });
    } catch (error) {
        console.error("❌ Error fetching pieces:", error);
    }
};

document.addEventListener("DOMContentLoaded", () => {
    const board = document.getElementById("board");
    const pieceContainer = document.getElementById("piece-container");
    const currentTurnDisplay = document.getElementById("current-turn");

    if (!board || !pieceContainer || !currentTurnDisplay) {
        console.error("❌ Error: One or more elements (board, pieceContainer, currentTurnDisplay) not found.");
        return;
    }

    initializeBoard();
});



/**
 * Create a DOM element for a game piece.
 */
const createPieceDiv = (piece) => {
    const pieceDiv = document.createElement("div");
    pieceDiv.classList.add("piece");
    pieceDiv.dataset.piece = piece.name;
    pieceDiv.dataset.shape = JSON.stringify(piece.shape); // Store as string safely

    renderPieceVisual(piece.shape, pieceDiv);

    pieceDiv.addEventListener("mousedown", (e) => {
        selectPiece(pieceDiv, piece.shape, piece.name, e);
    });

    pieceDiv.addEventListener("mouseover", () => {
        hoveredPiece = piece.shape; // ✅ Directly assign instead of parsing dataset
        hoveredPieceDiv = pieceDiv;
    });

    pieceDiv.addEventListener("mouseleave", () => {
        hoveredPiece = null;
        hoveredPieceDiv = null;
    });

    return pieceDiv;
};

/**
 * Select a piece and attach it to the cursor.
 */
const selectPiece = (pieceDiv, pieceShape, pieceName, event) => {
    selectedPieceDiv = pieceDiv.cloneNode(true);
    selectedPieceShape = pieceShape;
    selectedPieceName = pieceName;

    const { x, y } = getPieceOffset(pieceShape);
    offsetX = x + 25;
    offsetY = y + 25;

    selectedPieceDiv.style.position = "absolute";
    selectedPieceDiv.style.pointerEvents = "none";
    selectedPieceDiv.style.opacity = "0.7";
    selectedPieceDiv.style.zIndex = "1000";
    document.body.appendChild(selectedPieceDiv);

    movePieceWithCursor(event);

    document.addEventListener("mousemove", movePieceWithCursor);
    document.addEventListener("mouseup", releasePiece);
};

/**
 * Move the selected piece with the cursor.
 */
const movePieceWithCursor = (event) => {
    if (!selectedPieceDiv) return;

    selectedPieceDiv.style.left = `${event.clientX - offsetX}px`;
    selectedPieceDiv.style.top = `${event.clientY - offsetY}px`;
};

/**
 * Release the piece when clicking on the board.
 */
const releasePiece = (event) => {
    if (!selectedPieceDiv) return;

    const boardCell = document.elementFromPoint(event.clientX, event.clientY);
    if (boardCell && boardCell.classList.contains("cell")) {
        handleDrop(event, boardCell);
    }

    document.body.removeChild(selectedPieceDiv);
    selectedPieceDiv = null;
    selectedPieceShape = null;

    document.removeEventListener("mousemove", movePieceWithCursor);
    document.removeEventListener("mouseup", releasePiece);
};

/**
 * Get the offset of the top-left occupied cell (0,0) in the piece.
 */
const getPieceOffset = (pieceShape) => {
    let topLeftX = Infinity, topLeftY = Infinity;

    pieceShape.forEach((row, i) => {
        row.forEach((cell, j) => {
            if (cell === 1) {
                topLeftX = Math.min(topLeftX, i);
                topLeftY = Math.min(topLeftY, j);
            }
        });
    });

    const cellSize = 30;
    return { x: topLeftY * cellSize, y: topLeftX * cellSize };
};

/**
 * Handle rotation ('r') and flip ('f') on keypress when a piece is hovered.
 */
document.addEventListener("keydown", async (e) => {
    if (!hoveredPiece || !hoveredPieceDiv) return;

    const pieceName = hoveredPieceDiv.dataset.piece;
    const action = e.key.toLowerCase() === "r" ? "rotate" : e.key.toLowerCase() === "f" ? "flip" : null;

    if (!action) return;

    try {
        const transformedPiece = await rotateOrFlipPiece(pieceName, action);
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
 * Render a piece's shape visually inside a div.
 */
const renderPieceVisual = (pieceShape, pieceDiv) => {
    pieceDiv.innerHTML = ""; // Clear previous visual representation

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
        return data.shape; // Return the new shape after transformation
    } catch (error) {
        console.error(`❌ Error ${action}ing piece:`, error);
        return null;
    }
};


/**
 * Handle dropping a piece onto the board.
 */
const handleDrop = async (event, cell) => {
    if (!selectedPieceShape || !selectedPieceDiv) {
        console.warn("⚠️ No piece selected. Cannot place.");
        return;
    }

    const startX = parseInt(cell.dataset.row);
    const startY = parseInt(cell.dataset.col);
    const pieceName = selectedPieceName;
    const pieceShape = selectedPieceShape;

    console.log(`📡 Sending place request for ${pieceName} at (${startX}, ${startY})`);

    try {
        const response = await fetch(API_PLACE_PIECE, {
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

            // Remove placed piece from UI
            const pieceElement = document.querySelector(`[data-piece="${pieceName}"]`);
            if (pieceElement) {
                pieceElement.remove();
            } else {
                console.warn("⚠️ Tried to remove piece, but it was already missing.");
            }

            await updateBoardState();
            await renderPieces();

            selectedPieceDiv = null;
            selectedPieceShape = null;
            selectedPieceName = null;
            clearHover();
        }
    } catch (error) {
        console.error("❌ Network error placing piece:", error);
    }
};

/**
 * End the current player's turn and check for valid moves.
 */
const endTurn = async () => {
    try {
        console.log("📡 Calling /end_turn endpoint...");
        const response = await fetch(`${API_BASE_URL}/end_turn`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ current_player: currentPlayer }),
        });

        if (!response.ok) throw new Error(`Failed to end turn: ${response.statusText}`);

        const data = await response.json();
        console.log("✅ Turn ended:", data);

        // Update the current player
        currentPlayer = data.next_player;
        currentTurnDisplay.textContent = `Current Turn: Player ${currentPlayer}`;

        await updateBoardState();
        await renderPieces();

        // ✅ Automatically skip players if they have 0 valid moves
        if (data.valid_moves === 0) {
            console.log(`🚫 Player ${currentPlayer} has 0 valid moves! Skipping turn...`);
            setTimeout(endTurn, 1000); // Auto-skip after 1 second
        }
    } catch (error) {
        console.error("❌ Error ending turn:", error);
    }
};

/**
 * Ensure the End Turn button is set up correctly.
 */
document.addEventListener("DOMContentLoaded", () => {
    const endTurnButton = document.getElementById("end-turn-button");
    if (endTurnButton) {
        endTurnButton.addEventListener("click", () => {
            console.log("🎯 End Turn button clicked!");
            endTurn();
        });
    } else {
        console.error("❌ End Turn button not found in the DOM!");
    }

    initializeBoard();
});
