package chars

import (
	"strings"
)

type Point struct {
	X	int
	Y	int
}

var raw_chars = map[string]string{

"MISSING": `

******
******
******
******
******
******
******

`, "A": `

 ****
*    *
*    *
******
*    *
*    *
*    *

`, "B": `

*****
*    *
*    *
*****
*    *
*    *
*****

`, "C": `

  ****
 *
*
*
*
 *
  ****

`, "D": `

*****
*    *
*    *
*    *
*    *
*    *
*****

`, "E": `

******
*
*
******
*
*
******

`, "F": `

******
*
*
******
*
*
*

`, "G": `

  ****
 *
*
*  ***
*    *
 *   *
  ****

`, "H": `

*    *
*    *
*    *
******
*    *
*    *
*    *

`, "I": `

*****
  *
  *
  *
  *
  *
*****

`, "J": `

*****
  *
  *
  *
  *
  *
**

`, "K": `

*    *
*   *
*  *
***
*  *
*   *
*    *

`, "L": `

*
*
*
*
*
*
******

`, "M": `

 ** **
*  *  *
*  *  *
*  *  *
*  *  *
*  *  *
*  *  *

`, "N": `

*     *
**    *
* *   *
*  *  *
*   * *
*    **
*     *

`, "O": `

 ****
*    *
*    *
*    *
*    *
*    *
 ****

`, "P": `

*****
*    *
*    *
*****
*
*
*

`, "Q": `

 ****
*    *
*    *
*    *
*    *
*    *
 ****
     **

`, "R": `

*****
*    *
*    *
*****
*  *
*   *
*    *

`, "S": `

 ****
*
*
 ****
     *
     *
 ****

`, "T": `

*****
  *
  *
  *
  *
  *
  *

`, "U": `

*    *
*    *
*    *
*    *
*    *
*    *
 ****

`, "V": `

*     *
*     *
 *   *
 *   *
  * *
  * *
   *

`, "W": `

*  *  *
*  *  *
*  *  *
*  *  *
*  *  *
*  *  *
 ** **

`, "X": `

*     *
 *   *
  * *
   *
  * *
 *   *
*     *

`, "Y": `

*   *
*   *
*   *
*****
  *
  *
  *

`, "Z": `

*******
     *
    *
   *
  *
 *
*******

`, "1": `

 *
**
 *
 *
 *
 *
***

`, "2": `

 **
*  *
   *
  *
 *
*
****

`, "3": `

 **
*  *
   *
 **
   *
*  *
 **

`, "4": `

*  *
*  *
*  *
****
   *
   *
   *

`, "5": `

****
*
*
***
   *
   *
***

`, "6": `

 **
*
*
***
*  *
*  *
 **

`, "7": `

****
   *
  *
  *
 *
 *
 *

`, "8": `

 **
*  *
*  *
 **
*  *
*  *
 **

`, "9": `

 **
*  *
*  *
 ***
   *
   *
 **

`, "0": `

 **
*  *
*  *
*  *
*  *
*  *
 **

`}

func Points(c string) []Point {

	var ret []Point

	width := 0

	for i := 0; i < len(c); i++ {

		raw, ok := raw_chars[string([]byte{c[i]})]
		if ok == false {
			raw = raw_chars["MISSING"]
		}

		widest_line := 0

		lines := strings.Split(raw, "\n")

		for y, line := range lines {

			if len(line) > widest_line { widest_line = len(line) }

			for x := 0; x < len(line); x++ {
				if line[x] != ' ' {
					ret = append(ret, Point{x + width, y})
				}
			}
		}

		width += widest_line + 1
	}

	width -= 1

	for i := 0; i < len(ret); i++ {
		ret[i].X -= width / 2
		ret[i].Y -= 5					// Hardcoded based on the actual size of the chars
	}

	return ret
}
