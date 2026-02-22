class GameEngine(private val board: Board) {
    private var gameOver = false
    private var won = false
    private var firstClick = true

    fun isGameOver(): Boolean = gameOver
    fun hasWon(): Boolean = won

    fun revealCell(row: Int, col: Int): Boolean {
        if (gameOver) return false
        if (!board.isInBounds(row, col)) return false

        val cell = board.cells[row][col]
        if (cell.state == CellState.REVEALED) return false

        // First click safety (FR-6)
        if (firstClick) {
            handleFirstClick(row, col)
            firstClick = false
        }

        if (cell.hasMine) {
            cell.state = CellState.REVEALED
            gameOver = true
            won = false
            return true
        }

        revealRecursive(row, col)
        checkWin()
        return true
    }

    private fun handleFirstClick(row: Int, col: Int) {
        if (board.cells[row][col].hasMine) {
            board.relocateMine(row, col)
        }
    }

    private fun revealRecursive(row: Int, col: Int) {
        if (!board.isInBounds(row, col)) return
        val cell = board.cells[row][col]
        if (cell.state == CellState.REVEALED || cell.hasMine) return

        cell.state = CellState.REVEALED

        if (cell.adjacentMines == 0) {
            for (dr in -1..1) {
                for (dc in -1..1) {
                    if (dr == 0 && dc == 0) continue
                    revealRecursive(row + dr, col + dc)
                }
            }
        }
    }

    private fun checkWin() {
        for (r in 0 until board.rows) {
            for (c in 0 until board.cols) {
                val cell = board.cells[r][c]
                if (!cell.hasMine && cell.state != CellState.REVEALED) {
                    return
                }
            }
        }
        gameOver = true
        won = true
    }
}
