package recfun

object Main {
  def main(args: Array[String]) {
    println("Pascal's Triangle")
    for (row <- 0 to 10) {
      for (col <- 0 to row)
        print(pascal(col, row) + " ")
      println()
    }
  }

  /**
   * Exercise 1
    * the edge of the triangle will always be 1.
   */
    def pascal(c: Int, r: Int): Int = {
      if (c == 0 || c == r) 1
      else pascal(c - 1, r - 1) + pascal(c, r - 1)
  }
  
  /**
   * Exercise 2
    * Recursive function inFunction is used to pass on openBraces that keeps the count of open braces.
   */
    def balance(chars: List[Char]): Boolean = {
      def inFunction(chars: List[Char], openBraces: Int): Boolean = {
        if (chars.isEmpty) { openBraces == 0 }
        else {
          val firstLetter = chars.head
          val count =
            if (firstLetter == '(') openBraces + 1
            else if (firstLetter == ')') openBraces - 1
            else openBraces
          if (count >= 0) inFunction(chars.tail, count)
          else false
        }
      }

      inFunction(chars, 0)
    }
  /**
   * Exercise 3
   */

    def countChange(money: Int, coins: List[Int]): Int = {
      def inFunction(money: Int, coins: List[Int]) : Int = {
        if (coins.isEmpty) 0
        else if (money - coins.head == 0) 1
        else if (money - coins.head < 0) 0
        else countChange(money - coins.head, coins) + countChange(money, coins.tail)
      }
      inFunction(money, coins.sorted)
    }
  }
