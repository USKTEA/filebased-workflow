class Board(val rows: Int = 9, val cols: Int = 9, val mineCount: Int = 10) {
    val cells: Array<Array<Cell>> = Array(rows) { Array(cols) { Cell() } }
    private var minesPlaced = false

    fun initialize() {
        placeMines()
        calculateAdjacentMines()
    }

    private fun placeMines() {
        var placed = 0
        val random = java.util.Random()
        while (placed < mineCount) {
            val r = random.nextInt(rows)
            val c = random.nextInt(cols)
            if (!cells[r][c].hasMine) {
                cells[r][c].hasMine = true
                placed++
            }
        }
        minesPlaced = true
    }

    fun calculateAdjacentMines() {
        for (r in 0 until rows) {
            for (c in 0 until cols) {
                if (!cells[r][c].hasMine) {
                    cells[r][c].adjacentMines = countAdjacentMines(r, c)
                }
            }
        }
    }

    private fun countAdjacentMines(row: Int, col: Int): Int {
        var count = 0
        for (dr in -1..1) {
            for (dc in -1..1) {
                if (dr == 0 && dc == 0) continue
                val nr = row + dr
                val nc = col + dc
                if (nr in 0 until rows && nc in 0 until cols && cells[nr][nc].hasMine) {
                    count++
                }
            }
        }
        return count
    }

    fun relocateMine(row: Int, col: Int) {
        if (!cells[row][col].hasMine) return
        cells[row][col].hasMine = false
        val random = java.util.Random()
        while (true) {
            val r = random.nextInt(rows)
            val c = random.nextInt(cols)
            if (!cells[r][c].hasMine && !(r == row && c == col)) {
                cells[r][c].hasMine = true
                break
            }
        }
        calculateAdjacentMines()
    }

    fun isInBounds(row: Int, col: Int): Boolean = row in 0 until rows && col in 0 until cols

    // Rendering responsibility (intentionally merged here instead of separate Renderer.kt)
    fun render(revealAll: Boolean = false) {
        print("   ")
        for (c in 0 until cols) print(" $c")
        println()
        print("   ")
        for (c in 0 until cols) print("--")
        println()

        for (r in 0 until rows) {
            print("$r |")
            for (c in 0 until cols) {
                val cell = cells[r][c]
                val display = when {
                    revealAll && cell.hasMine -> " *"
                    cell.state == CellState.REVEALED -> {
                        if (cell.hasMine) " *"
                        else if (cell.adjacentMines == 0) " ."
                        else " ${cell.adjacentMines}"
                    }
                    cell.state == CellState.FLAGGED -> " F"
                    else -> " #"
                }
                print(display)
            }
            println()
        }
    }
}
