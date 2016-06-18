package funsets

/**
 * 2. Purely Functional Sets.
 */
object FunSets {
  /**
   * We represent a set by its characteristic function, i.e.
   * its `contains` predicate.
   */
  type Set = Int => Boolean

  def main(args: Array[String]) {
    println("Check Contains")
    if (contains(Set(1,2,3),2)) println("Very Good")
    else println("Very Bad")

    println("Check union")
    val x1 = union(Set(1,2), Set(3,4))
    if (x1(1)) println("Very Good")
    else println("Very Bad")

    println("Check intersect")
    val x2 = intersect(Set(1,2), Set(3,4))
    if (x2(1)) println("Very Bad")
    else println("Very Good")

    println("Check diff")
    val x3 = diff(Set(1,2), Set(3,4))
    if (x3(1)) println("Very Good")
    else println("Very Bad")
    if (x3(3)) println("Very Bad")
    else println("Very Good")

    println("Check forall")
    val p: Int => Boolean = i => i > 1
    if (forall(Set(1,2),p)) println("Very Bad")
    else println("Very Good")
    if (forall(Set(2,3,4),p)) println("Very Good")
    else println("Very Bad")

    println("Check exists")
    if (exists(Set(1,2,-2),p)) println("Very Good")
    else println("Very Bad")
    if (forall(Set(-2,-3),p)) println("Very Bad")
    else println("Very Good")

    println("Check map")
    def f: Int => Int = x => x * x

    val x4 = map(Set(1,2,3,4), f)
    if (x4(9)) println("Very Good")
    else println("Very Bad")
    if (!x4(2)) println("Very Good")
    else println("Very Bad")
  }

  /**
   * Indicates whether a set contains a given element.
   */
  def contains(s: Set, elem: Int): Boolean = s(elem)

  /**
   * Returns the set of the one given element.
   */
  def singletonSet(elem: Int): Set = Set(elem)
  
  /**
   * Returns the union of the two given sets,
   * the sets of all elements that are in either `s` or `t`.
   */
  def union(s: Set, t: Set): Set = {
    i => s(i) || t(i)
  }
  
  /**
   * Returns the intersection of the two given sets,
   * the set of all elements that are both in `s` and `t`.
   */
  def intersect(s: Set, t: Set): Set = {
    i => s(i) && t(i)
  }
  
  /**
   * Returns the difference of the two given sets,
   * the set of all elements of `s` that are not in `t`.
   */
  def diff(s: Set, t: Set): Set = {
    i => s(i) && !t(i)
  }
  
  /**
   * Returns the subset of `s` for which `p` holds.
   */
  def filter(s: Set, p: Int => Boolean): Set = {
    intersect(s,p)
  }
  

  /**
   * The bounds for `forall` and `exists` are +/- 1000.
   */
  val bound = 1000

  /**
   * Returns whether all bounded integers within `s` satisfy `p`.
   */
  def forall(s: Set, p: Int => Boolean): Boolean = {
    def iterSet(i: Int): Boolean = {
      if (s(i) && !p(i)) false
      else if (i > bound) true
      else iterSet(i+1)
    }
    iterSet(-bound)
  }
  
  /**
   * Returns whether there exists a bounded integer within `s`
   * that satisfies `p`.
   */
    //def exists(s: Set, p: Int => Boolean): Boolean = ???
/*
  def exists(s: Set, p: Int => Boolean): Boolean = {

    def iterSet(i: Int): Boolean = {
      if (s(i) && p(i)) true
      else if (i > bound) false
      else iterSet(i+1)
    }
    iterSet(-bound)
  }
*/
  def exists(s: Set, p: Int => Boolean): Boolean = forall(s, union(s,p))

  /**
   * Returns a set transformed by applying `f` to each element of `s`.
   */
    //def map(s: Set, f: Int => Int): Set = ???


  def map(s: Set, f: Int => Int): Set = {

    def iterSet(i: Int, tempSet: Set): Set = {
      if (i > bound) tempSet
      else if (s(i)) iterSet(i+1, union(singletonSet(f(i)), tempSet))
      else iterSet(i+1, tempSet)
    }
    iterSet(-bound, diff(s,s))
  }

  /**
   * Displays the contents of a set
   */
  def toString(s: Set): String = {
    val xs = for (i <- -bound to bound if contains(s, i)) yield i
    xs.mkString("{", ",", "}")
  }

  /**
   * Prints the contents of a set on the console.
   */
  def printSet(s: Set) {
    println(toString(s))
  }
}
