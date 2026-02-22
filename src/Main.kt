fun main() {
    val board = Board()
    board.initialize()
    val engine = GameEngine(board)

    println("=== 지뢰찾기 (Minesweeper) ===")
    println("명령어: open <행> <열>")
    println("예시: open 3 4")
    println()

    while (!engine.isGameOver()) {
        board.render()
        println()
        print("명령 입력: ")

        val input = readlnOrNull()?.trim() ?: continue
        val parts = input.split(" ")

        if (parts.size != 3 || parts[0] != "open") {
            println("올바른 명령어를 입력하세요: open <행> <열>")
            continue
        }

        val row = parts[1].toIntOrNull()
        val col = parts[2].toIntOrNull()

        if (row == null || col == null) {
            println("행과 열은 숫자여야 합니다.")
            continue
        }

        if (!board.isInBounds(row, col)) {
            println("유효한 범위의 좌표를 입력하세요 (0-${board.rows - 1})")
            continue
        }

        engine.revealCell(row, col)
    }

    board.render(revealAll = true)
    println()

    if (engine.hasWon()) {
        println("축하합니다! 모든 안전 셀을 열었습니다. 승리!")
    } else {
        println("지뢰를 밟았습니다. 패배!")
    }
}
