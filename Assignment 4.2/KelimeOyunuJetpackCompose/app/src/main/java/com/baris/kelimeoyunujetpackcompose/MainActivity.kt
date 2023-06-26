package com.baris.kelimeoyunujetpackcompose

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Delete
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.baris.kelimeoyunujetpackcompose.ui.theme.KelimeOyunuJetpackComposeTheme
import kotlin.random.Random
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.io.BufferedReader
import java.io.File
import java.io.InputStream
import java.io.InputStreamReader

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            KelimeOyunuJetpackComposeTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(), color = MaterialTheme.colors.background
                ) {
                    GameGrid(onCellClicked, onCellChanged)
                }
            }
        }
    }

    fun readTextFile(filename: String): List<String> {
        val inputStream: InputStream = assets.open(filename)
        val bufferedReader = BufferedReader(InputStreamReader(inputStream))
        val lines = mutableListOf<String>()
        var line: String?
        while (bufferedReader.readLine().also { line = it } != null) {
            lines.add(line!!)
        }
        bufferedReader.close()
        return lines
    }


    data class CharacterInfo(
        var character: Char? = null, val score: Int, val isVowel: Boolean
    )


    val turkcesesliHarfler = listOf('A', 'E', 'I', 'İ', 'O', 'Ö', 'U', 'Ü')

    val turkceSessizHarfler = listOf(
        'B',
        'C',
        'Ç',
        'D',
        'F',
        'G',
        'Ğ',
        'H',
        'J',
        'K',
        'L',
        'M',
        'N',
        'P',
        'R',
        'S',
        'Ş',
        'T',
        'V',
        'Y',
        'Z'
    )

    val scoreMap = mapOf(
        'A' to 1,
        'B' to 3,
        'C' to 4,
        'Ç' to 4,
        'D' to 3,
        'E' to 1,
        'F' to 7,
        'G' to 5,
        'Ğ' to 8,
        'H' to 5,
        'I' to 2,
        'İ' to 1,
        'J' to 10,
        'K' to 1,
        'L' to 1,
        'M' to 2,
        'N' to 1,
        'O' to 2,
        'Ö' to 7,
        'P' to 5,
        'R' to 1,
        'S' to 2,
        'Ş' to 4,
        'T' to 1,
        'U' to 2,
        'Ü' to 3,
        'V' to 7,
        'Y' to 3,
        'Z' to 4
    )

    val fileMap = mapOf(
        'A' to "a.txt",
        'B' to "b.txt",
        'C' to "c.txt",
        'Ç' to "c2.txt",
        'D' to "d.txt",
        'E' to "e.txt",
        'F' to "f.txt",
        'G' to "g.txt",
        'Ğ' to "g2.txt",
        'H' to "h.txt",
        'I' to "i.txt",
        'İ' to "i2.txt",
        'J' to "j.txt",
        'K' to "k.txt",
        'L' to "l.txt",
        'M' to "m.txt",
        'N' to "n.txt",
        'O' to "o.txt",
        'Ö' to "o2.txt",
        'P' to "p.txt",
        'R' to "r.txt",
        'S' to "s.txt",
        'Ş' to "s2.txt",
        'T' to "t.txt",
        'U' to "u.txt",
        'Ü' to "u2.txt",
        'V' to "v.txt",
        'Y' to "y.txt",
        'Z' to "z.txt"
    )

    data class CellInfo(
        val row: Int,
        val col: Int,
        var letter: Char? = null,
        var isClicked: Boolean = false,
        var isfreezing: Boolean = false,
        var isfreezeblock: Boolean = false,
        var freezeblockcount: Int = 0
//    var letter2: CharacterInfo
    )

    var currentWord = ""
    var currentScore = 0
    var failCount = 0
    var isGameRunning = false
    var isGameOver = false

    @Composable
    fun GameGrid(
        OnCellClicked: (row: Int, col: Int) -> Unit,
        OnCellChanged: (row: Int, col: Int, letter: Char) -> Unit
    ) {
        var cellState by remember { mutableStateOf(cells) }
        val delayInMillis by remember { mutableStateOf(50L) }
        LaunchedEffect(Unit) {
            while (true) {
                delay(delayInMillis)
                cellState = cells.copyOf()
            }
        }
        Box(
            modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center
        ) {
            Column {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Current Score: $currentScore",
                        modifier = Modifier.align(Alignment.CenterVertically)
                    )
                    Text(text = "Fails: $failCount/3")
                }
                for (i in 0..9) {
                    Row {
                        for (j in 0..7) {
                            val cell = cellState[i][j]
                            val backgroundColor = if (cell.isClicked) Color.Blue
                            else if (cell.isfreezeblock && cell.isfreezing) Color.Cyan
                            else if (cell.isfreezeblock) Color.Yellow
                            else if (cell.isfreezing) Color.Red
                            else if (cell.letter != null) Color.LightGray
                            else Color.Gray
                            Box(modifier = Modifier
                                .size(50.dp)
                                .background(backgroundColor)
                                .clickable {
                                    OnCellClicked(i, j)
                                    // update the ui
                                    cellState = cells.copyOf()
                                }) {
                                cell.letter?.let {
                                    Text(
                                        text = it.toString(),
                                        modifier = Modifier.align(Alignment.Center)
                                    )
                                }
                            }
                        }
                    }
                }
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Button(onClick = {
                        println("Clicked Delete")
                        onDeleteClicked()
                        cellState = cells.copyOf()
                    }) {
                        Icon(
                            imageVector = Icons.Default.Delete, contentDescription = "Delete"
                        )
                    }
                    Text(text = currentWord, textAlign = TextAlign.Center)
                    Button(onClick = {
                        println("Clicked Accept")
                        onAcceptClicked()
                        cellState = cells.copyOf()
                    }) {
                        Icon(
                            imageVector = Icons.Default.Check, contentDescription = "Check"
                        )
                    }

                }
            }
            Button(
                onClick = {
                    if (!isGameRunning) {
                        isGameRunning = true
//                        for (i in 0..9) {
//                            for (j in 0..7) {
//                                cells[i][j].letter = null
//                                cells[i][j].isClicked = false
//                            }
//                        }
                        gameLoop(OnCellChanged)
                    }
                }, modifier = Modifier.align(Alignment.BottomCenter)
            ) {
                if (!isGameRunning) {
                    Text(text = "Start Game")
                } else {
                    Text(text = "Game Status: $delayInMillis")
                }
            }
        }
        if (isGameOver) {
            val file = File(filesDir, "UserScores.txt")
            if (!file.exists()) {
                file.createNewFile()
            }
            val userScores = file.readText()
            AlertDialog(
                onDismissRequest = { isGameOver = false },
                title = { Text(text = "Game Over") },
                text = {
                    Text(
                        text = "Your score is $currentScore\n" +
                                "Your old scores are\n$userScores"
                    )
                },
                confirmButton = {
                    Button(onClick = {
                        isGameOver = false
                        isGameRunning = false
                        currentScore = 0
                        failCount = 0
                        currentWord = ""
                    }) {
                        Text(text = "Restart")
                    }
                }
            )
            // save user score only once
            if (!userScores.contains(currentScore.toString())) {
                saveNewScore()
            }
        }
    }

    val onCellClicked: (row: Int, col: Int) -> Unit = { row, col ->
        if (cells[row][col].letter != null && !cells[row][col].isClicked) {
            println("Clicked $row, $col")
            cells[row][col].isClicked = true
            currentWord += cells[row][col].letter
            clickedCellsOrder.add(cells[row][col])
            clickedCellsOrder[clickedCellsOrder.size - 1].letter = cells[row][col].letter
        } else if (cells[row][col].isClicked) {
            println("Clicked $row, $col")
            cells[row][col].isClicked = false
            // how many time the letter is in clickedCellsOrder
//            val count = clickedCellsOrder.count { it.letter == cells[row][col].letter }
            // if the letter is in clickedCellsOrder more than once
            currentWord = currentWord.find { it == cells[row][col].letter }?.let {
                currentWord.replace(
                    it.toString(),
                    ""
                )
            } ?: currentWord
        }
    }

    val onCellChanged: (row: Int, col: Int, letter: Char) -> Unit = { row, col, letter ->
        cells[row][col].letter = letter
    }

    val cells = Array(10) { row ->
        Array(8) { col ->
            CellInfo(row, col)
        }
    }
    val clickedCellsOrder = mutableListOf<CellInfo>()

    // Clicked Delete Button
    fun onDeleteClicked() {
        // Delete all the letters from the current word
        currentWord = ""
        // Set the isClicked to false for all the cells
        for (i in 0..9) for (j in 0..7) {
            cells[i][j].isClicked = false
        }
    }

    // Clicked Accept Button
    fun onAcceptClicked() {
        if (currentWord == "") return
        if (currentWord.length < 3) return
        // Check if the current word is in the resource file
        // If yes, then delete the word from the board
        // If no, then delete the current word
        val firstLetter = currentWord[0]
        val lowercasecurrentWord = currentWord.replace("I", "ı").replace("İ","i").lowercase()
        val fileName = fileMap[firstLetter]
        val dictionary = fileName?.let { readTextFile(it) }
        if (dictionary != null) {
            if (dictionary.contains(lowercasecurrentWord)) {
                for (i in 0..9) for (j in 0..7) {
                    if (cells[i][j].isClicked) {
                        if (cells[i][j].isfreezing) {
                            cells[i][j].isfreezing = false
                            cells[i][j].isClicked = false
//                            cells[i][j].isfreezeblock = false
                        }
                        else {
                            cells[i][j].letter = null
                            cells[i][j].isClicked = false
                            cells[i][j].isfreezing = false
                            cells[i][j].isfreezeblock= false
                            cells[i][j].freezeblockcount = 0
                        }
                    }
                }
                addPoints(currentWord)
                currentWord = ""
            } else {
                failCount++
                if (failCount == 3) {
                    // spawn letter blocks from the top row
                    for (i in 0..7) {
                        // if there is a block in a cell in the top row game is over
                        if (cells[0][i].letter != null) {
                            isGameOver = true
                            isGameRunning = false
                            break
                        }
                        // if there is no block in a cell in the top row
                        // spawn a block 40% vowel 60% consonant
                        else {
                            val random = Random.nextInt(0, 10)
                            if (random < 4) {
                                cells[0][i].letter = turkcesesliHarfler.random()
                            } else {
                                cells[0][i].letter = turkceSessizHarfler.random()
                            }
                        }
                    }
                    failCount = 0
                }
                onDeleteClicked()
            }
        }
    }

    fun addPoints(word: String) {
        // Add points to the score
        for (letter in word) {
            scoreMap[letter]?.let {
                currentScore += it
            }
        }
    }

    fun saveNewScore() {
        val userScores = openFileInput("UserScores.txt")
            .bufferedReader()
            .readLines()
        val newScore = currentScore.toString()
        val newScoreList = userScores.toMutableList()
        newScoreList.add(newScore)
        // cast new scorelist to int
        newScoreList.sortByDescending { it.toInt() }
        val newScoreListString = newScoreList.joinToString("\n")
        val fileOutputStream = openFileOutput("UserScores.txt", Context.MODE_PRIVATE)
        fileOutputStream.write(newScoreListString.toByteArray())
        fileOutputStream.close()
    }

    @Preview
    @Composable
    fun PreviewGameGrid() {
        GameGrid(onCellClicked, onCellChanged)
    }

    fun gameLoop(OnCellChanged: (row: Int, col: Int, letter: Char) -> Unit) {
        GlobalScope.launch {
            failCount = 0
            currentScore = 0
            isGameOver = false
            isGameRunning = true
            // clear all the cells
            for (i in 0..9) for (j in 0..7) {
                cells[i][j].letter = null
                cells[i][j].isClicked = false
                cells[i][j].isfreezing = false
                cells[i][j].isfreezeblock = false
                cells[i][j].freezeblockcount = 0
            }
            for (i in 7..9) for (j in 0..7) {
                cells[i][j].letter = if (Random.nextInt(0, 100) < 40) {
                    turkcesesliHarfler.random()
                } else {
                    turkceSessizHarfler.random()
                }
            }
            var startTime = System.currentTimeMillis()
            var currentDelay = 5000L
            while (isGameRunning) {
                if (currentScore < 100) currentDelay = 4000L
                else if (currentScore < 200) currentDelay = 3000L
                else if (currentScore < 300) currentDelay = 2000L
                else if (currentScore < 400) currentDelay = 1000L

                for (i in 8 downTo 0) {
                    for (j in 7 downTo 0) {
                        val currentCell = cells[i][j]
                        if (currentCell.letter != null) {
                            val cellBelow = cells[i + 1][j]
                            if (cellBelow.letter == null) {
                                cellBelow.letter = currentCell.letter
                                currentCell.letter = null
                                cellBelow.isClicked = currentCell.isClicked
                                currentCell.isClicked = false
                                cellBelow.isfreezeblock = currentCell.isfreezeblock
                                currentCell.isfreezeblock = false
                                cellBelow.isfreezing = currentCell.isfreezing
                                currentCell.isfreezing = false
                                cellBelow.freezeblockcount = currentCell.freezeblockcount
                                currentCell.freezeblockcount = 0
                                OnCellChanged(i + 1, j, cellBelow.letter!!)
                            }
                        }
                        // freeze the blocks near the freezeblock
                        if (currentCell.isfreezeblock) {
                            if (i > 0) {
                                if (cells[i - 1][j].letter != null) {
                                    if (!(cells[i - 1][j].isfreezing)) {
                                        cells[i - 1][j].isfreezing = true
                                        currentCell.freezeblockcount++
                                        if (currentCell.freezeblockcount == 4) {
                                            currentCell.isfreezeblock = false
                                            currentCell.freezeblockcount = 0
                                        }
                                    }

                                }
                            }
                            if (i < 9) {
                                if (cells[i + 1][j].letter != null) {
                                    if (!(cells[i + 1][j].isfreezing)) {
                                        cells[i + 1][j].isfreezing = true
                                        currentCell.freezeblockcount++
                                        if (currentCell.freezeblockcount == 4) {
                                            currentCell.isfreezeblock = false
                                            currentCell.freezeblockcount = 0
                                        }
                                    }
                                }
                            }
                            if (j > 0) {
                                if (cells[i][j - 1].letter != null) {
                                    if (!(cells[i][j - 1].isfreezing)) {
                                        cells[i][j - 1].isfreezing = true
                                        currentCell.freezeblockcount++
                                        if (currentCell.freezeblockcount == 4) {
                                            currentCell.isfreezeblock = false
                                            currentCell.freezeblockcount = 0
                                        }
                                    }
                                }
                            }
                            if (j < 7) {
                                if (cells[i][j + 1].letter != null) {
                                    if (!(cells[i][j + 1].isfreezing)) {
                                        cells[i][j + 1].isfreezing = true
                                        currentCell.freezeblockcount++
                                        if (currentCell.freezeblockcount == 4) {
                                            currentCell.isfreezeblock = false
                                            currentCell.freezeblockcount = 0
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                if (System.currentTimeMillis() - startTime > currentDelay) {
                    // spawn a letter block
                    println("Spawning a letter block")
                    val row = 0
                    val col = (0..7).random()
                    // calculate how much vowel and consonant letters are in the board
                    var vowelCount = 0
                    var letterCount = 0
                    for (i in 0..9) for (j in 0..7) {
                        if (cells[i][j].letter != null) {
                            letterCount++
                            if (cells[i][j].letter in turkcesesliHarfler) {
                                vowelCount++
                            }
                        }
                    }
                    // if there are more than 40% vowel letters, spawn a consonant letter
                    // if there are less than 40% vowel letters, spawn a vowel letter
                    val letter = if (vowelCount.toDouble() / letterCount.toDouble() > 0.4) {
                        turkceSessizHarfler.random()
                    } else {
                        turkcesesliHarfler.random()
                    }
                    // check if the letter block is colliding with any other letter block
                    if (cells[row][col].letter != null) {
                        // game over
                        println("Game Over")
                        isGameOver = true
                        isGameRunning = false
                        break
                    }
                    cells[row][col].letter = letter
                    // 10% chance of spawning a freeze block
                    if (Random.nextInt(0, 100) < 10) {
                        cells[row][col].isfreezeblock = true
                    }
                    OnCellChanged(row, col, letter)
                    // reset the timer
                    startTime = System.currentTimeMillis()
                }
                // print all the cells status
//                if (System.currentTimeMillis() - startTime > 1000) {
//                    for (i in 0..9) {
//                        for (j in 0..7) {
//                            print("${i} ${j} ")
//                            print("${if (cells[i][j].isClicked) "X" else " "} ")
//                            print("${cells[i][j].letter ?: " "} ")
//                            print("${if (cells[i][j].isfreezeblock) "F" else " "} ")
//                            print("${if (cells[i][j].isfreezing) "P" else " "} ")
//                            print("${cells[i][j].freezeblockcount} |")
//                        }
//                        println()
//                    }
//                    print("------------------------------------------\n")
//                }
                delay(150)
            }
        }
    }
}