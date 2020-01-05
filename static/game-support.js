function getGrid(d, p) {
  var no = [p, p - 1, p + 1, p - d, p - d - 1, p - d + 1, p + d + 1, p + d, p + d - 1]
  var grid = []
  for (i = 0; i < Math.pow(d, 2); i++) {
    if (Math.round(Math.random()*2) == 0 && !no.includes(i)) {
      grid.push('*');
    } else {
      grid.push(0);
    }
  }
  for (i = 0; i < Math.pow(d, 2); i++) {
    if (grid[i] != '*') {
      var tally = 0;
      if (i % d != 0) {
        if (grid[i-1] == '*') {
          tally ++;
        }
      }
      if (i % d != d-1) {
        if (grid[i+1] == '*') {
          tally ++;
        }
      }
      if (i >= d) {
        if (grid[i-d] == '*') {
          tally ++;
        }
        if (i % d != 0) {
          if (grid[i-d-1] == '*') {
            tally ++;
          }
        }
        if (i % d != d - 1) {
          if (grid[i-d+1] == '*') {
            tally ++;
          }
        }
      }
      if (i < Math.pow(d, 2) - d) {
        if (grid[i+d] == '*') {
          tally ++;
        }
        if (i % d != 0) {
          if (grid[i+d-1] == '*') {
            tally ++;
          }
        }
        if (i % d != d - 1) {
          if (grid[i+d+1] == '*') {
            tally ++;
          }
        }
      }
      grid[i] = tally
    }
  }
  var temp = "";
  for (y = 0; y < grid.length; y++) {
    if (y % d == d - 1) {
      console.log(temp + (grid[y].toString()));
      temp = "";
    } else {
      temp += grid[y].toString();
    }
  }
  var zeroes = [];
  for (y = 0; y < grid.length; y++) {
    if (grid[y] == 0) {
      zeroes.push(y);
    }
  }
  console.log(zeroes);
  return grid
}

function plantFlag(grid, revealed) {
  if (!revealed.includes($(this).attr("id"))) {
    $(this).toggleClass("flag");
  }
}

function revealTile(grid) {
  if ($(this).hasClass("g")) {
    $(this).addClass("l-b");
  } else {
    $(this).addClass("d-b");
  }
  colour = "";
  text = grid[$(this).attr("id")].toString();
  switch (text) {
    case '0':
      text = "";
      break;
    case '1':
      colour = "blue";
      break;
    case '2':
      colour = "green";
      break;
    case '3':
      colour = "red"
      break;
    case '4':
      colour = "purple";
      break;
    case '5':
      colour = "orange";
      break;
    case '6':
      colour = "yellow";
      break;
    case '7':
      colour = "pink";
      break;
    case '8':
      colour = "silver";
      break;
    case '*':
      //game over bro!
      break;
    default:
      break;
  }
  $(this).css("color", colour);
  $(this).text(text);
}
