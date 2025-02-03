const board = document.getElementById("board");
const currentTurnDisplay = document.getElementById("current-turn");
const pieceSelector = document.getElementById("piece-selector");
let currentPlayer = 1; // Start with Player 1

// Backend API endpoints
const API_GET_BOARD = "http://127.0.0.1:5000/get_board";
const API_PLACE_PIECE = "http://127.0.0.1:5000/place_piece";

// Initialize a 20x20 grid
const initializeBoard = () => {
  console.log("Initializing board...");
  board.innerHTML = ""; // Clear board if reinitializing
  for (let i = 0; i < 20; i++) {
    for (let j = 0; j < 20; j++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.dataset.row = i;
      cell.dataset.col = j;

      // Make each cell droppable
      cell.addEventListener("dragover", (e) => e.preventDefault());
      cell.addEventListener("drop", (e) => handleDrop(e, cell));

      board.appendChild(cell);
    }
  }
  console.log("Board initialized.");
};

// Fetch the board state from the backend
const fetchBoard = async () => {
  try {
    const response = await fetch(API_GET_BOARD);
    const data = await response.json();
    renderBoard(data.board);
    updateCurrentTurn(data.current_player); // Map backend player to frontend player
  } catch (error) {
    console.error("Error fetching board state:", error);
  }
};

// Render the board state on the grid
const renderBoard = (boardState) => {
  const cells = document.querySelectorAll(".cell");
  cells.forEach((cell) => {
    const row = parseInt(cell.dataset.row);
    const col = parseInt(cell.dataset.col);
    const player = boardState[row][col];
    cell.className = "cell"; // Reset cell
    if (player === "A") cell.classList.add("player-1");
    else if (player === "B") cell.classList.add("player-2");
    else if (player === "C") cell.classList.add("player-3");
    else if (player === "D") cell.classList.add("player-4");
  });
};

// Handle drop event for placing a piece
const handleDrop = async (e, cell) => {
  const pieceType = e.dataTransfer.getData("pieceType");
  const row = parseInt(cell.dataset.row);
  const col = parseInt(cell.dataset.col);

  console.log(`Dropped piece: ${pieceType} at Row: ${row}, Col: ${col}`);

  // Send placement to backend
  try {
    const response = await fetch(API_PLACE_PIECE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ piece: pieceType, x: row, y: col }),
    });
    const data = await response.json();

    if (data.success) {
      renderBoard(data.board); // Update board
      endTurn(); // Switch players
    } else {
      alert(data.error || "Invalid move!");
    }
  } catch (error) {
    console.error("Error during piece placement:", error);
  }
};

// End the turn and switch players
const endTurn = () => {
  currentPlayer = currentPlayer === 4 ? 1 : currentPlayer + 1; // Cycle between 1-4
  updateCurrentTurn(currentPlayer);
};

const updateCurrentTurn = (player) => {
  currentPlayer = player; // Update player state
  currentTurnDisplay.textContent = `Current Turn: Player ${currentPlayer}`;
};

// Add event listeners to draggable pieces
const initializePieces = () => {
  const pieces = document.querySelectorAll(".piece");
  pieces.forEach((piece) => {
    piece.setAttribute("draggable", true);
    piece.addEventListener("dragstart", (e) => {
      e.dataTransfer.setData("pieceType", piece.dataset.piece);
      console.log(`Dragging piece: ${piece.dataset.piece}`);
    });
  });
};

// Initialize everything on page load
initializeBoard();
initializePieces();
fetchBoard();
