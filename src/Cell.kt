enum class CellState {
    HIDDEN,
    REVEALED,
    FLAGGED
}

data class Cell(
    var state: CellState = CellState.HIDDEN,
    var hasMine: Boolean = false,
    var adjacentMines: Int = 0
)
