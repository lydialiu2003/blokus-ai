// Select the board container and current turn display elements
const board = document.getElementById('board');
const currentTurnDisplay = document.getElementById('current-turn');
let currentPlayer = 1; // Start with Player 1

// Initialize a 20x20 grid
const initializeBoard = () => {
  console.log('Initializing board...');
  for (let i = 0; i < 20; i++) {
    for (let j = 0; j < 20; j++) {
      // Create a cell element for each grid position
      const cell = document.createElement('div');
      cell.classList.add('cell');
      cell.dataset.row = i; // Store the row index
      cell.dataset.col = j; // Store the column index

      // Append the cell to the board container
      board.appendChild(cell);
    }
  }
  console.log('Board initialized.');
};

// Handle cell clicks
const handleCellClick = (cell) => {
  console.log(`Cell clicked: Row ${cell.dataset.row}, Col ${cell.dataset.col}`);

  // Check if the cell is already occupied
  if (cell.classList.contains('player-1') || cell.classList.contains('player-2')) {
    alert('This cell is already occupied!');
    return;
  }

  // Mark the cell with the current player's color
  cell.classList.add(`player-${currentPlayer}`);
  console.log(`Cell marked for Player ${currentPlayer}`);
};

// End the turn and switch players
const endTurn = () => {
  console.log(`Player ${currentPlayer} ended their turn.`);
  // Switch to the other player
  currentPlayer = currentPlayer === 1 ? 2 : 1;
  // Update the turn display
  currentTurnDisplay.textContent = `Current Turn: Player ${currentPlayer}`;
  console.log(`Now it's Player ${currentPlayer}'s turn.`);
};

// Attach the End Turn button event listener
document.getElementById('end-turn').addEventListener('click', endTurn);

// Initialize the board when the page loads
initializeBoard();
