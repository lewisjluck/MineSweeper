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
  return grid
}

function plantFlag(grid, revealed) {
  if (!revealed.includes($(this).attr("id"))) {
    $(this).toggleClass("flag");
  }
}

function revealTile(id, grid) {
  if ($("#" + id).hasClass("g")) {
    $("#" + id).addClass("l-b");
  } else {
    $("#" + id).addClass("d-b");
  }
  colour = "";
  text = grid[parseInt(id)].toString();
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
  $("#" + id).css("color", colour);
  $("#" + id).text(text);
}

function getGaps(grid, d) {
  masterGaps = [];
  for (i = 0; i < grid.length; i++) {
    already = undefined;
    for (j = 0; j< masterGaps.length; j++) {
      if (masterGaps[j].includes(i)) {
        already = true;
      } else {
        already = false;
      }
    }
    if (grid[i] == 0 && !already) {
      gaps = []
      masterGaps.push(DFS(grid, i, gaps, d));
    }
  }
  for (i = 0; i < d; i++) {
    for (j = 0; j < d; j++) {
      index = i * d + j
      if (grid[index] == 0) {
        gapsArray = undefined;
        for (y = 0; y < masterGaps.length; y++) {
          if (masterGaps[y].includes(index)) {
            gapsArray = y;
          }
        }
        if (grid[index + 1] != 0 && j != d - 1) {
          if (!masterGaps[gapsArray].includes(index + 1)){
            masterGaps[gapsArray].push(index + 1);
          }
        }
        if (i < d - 1 && j < d - 2) {
          if (grid[index + d + 1] == 0 && grid[index + 1] != 0) {
            if (!masterGaps[gapsArray].includes(index + 2)){
              masterGaps[gapsArray].push(index + 2);
            }
          }
        }
        if (i != 0 && j < d - 2) {
          if (grid[index - d + 1] == 0 && grid[index + 1] != 0) {
            if (!masterGaps[gapsArray].includes(index + 2)){
              masterGaps[gapsArray].push(index + 2);
            }
          }
        }
        if (grid[index - 1] != 0 && j != 0) {
          if (!masterGaps[gapsArray].includes(index - 1)){
            masterGaps[gapsArray].push(index - 1);
          }
        }
        if (i < d - 1 && j > 1) {
          if (grid[index + d - 1] == 0 && grid[index - 1] != 0) {
            if (!masterGaps[gapsArray].includes(index - 2)){
              masterGaps[gapsArray].push(index - 2);
            }
          }
        }
        if (i != 0 && j > 1) {
          if (grid[index - d - 1] == 0 && grid[index - 1] != 0) {
            if (!masterGaps[gapsArray].includes(index - 2)){
              masterGaps[gapsArray].push(index - 2);
            }
          }
        }
      } else {
        if (i != d - 1) {
          if (grid[index + d] == 0) {
            gapsArray = undefined;
            for (y = 0; y < masterGaps.length; y++) {
              if (masterGaps[y].includes(index + d)) {
                gapsArray = y;
              }
            }
            if (!masterGaps[gapsArray].includes(index)){
              masterGaps[gapsArray].push(index);
            }
          }
        }
        if (i != d - 1 && j != d-1) {
          if (grid[index + d + 1] == 0) {
            gapsArray = undefined;
            for (y = 0; y < masterGaps.length; y++) {
              if (masterGaps[y].includes(index + d + 1)) {
                gapsArray = y;
              }
            }
            if (!masterGaps[gapsArray].includes(index)){
              masterGaps[gapsArray].push(index);
            }
          }
        }
        if (i != d - 1 && j != 0) {
          if (grid[index + d - 1] == 0) {
            gapsArray = undefined;
            for (y = 0; y < masterGaps.length; y++) {
              if (masterGaps[y].includes(index + d - 1)) {
                gapsArray = y;
              }
            }
            if (!masterGaps[gapsArray].includes(index)){
              masterGaps[gapsArray].push(index);
            }
          }
        }
        if (i != 0) {
          if (grid[index - d] == 0) {
            gapsArray = undefined;
            for (y = 0; y < masterGaps.length; y++) {
              if (masterGaps[y].includes(index - d)) {
                gapsArray = y;
              }
            }
            if (!masterGaps[gapsArray].includes(index)){
              masterGaps[gapsArray].push(index);
            }
          }
        }
        if (i != 0 && j != d-1) {
          if (grid[index - d + 1] == 0) {
            gapsArray = undefined;
            for (y = 0; y < masterGaps.length; y++) {
              if (masterGaps[y].includes(index - d + 1)) {
                gapsArray = y;
              }
            }
            if (!masterGaps[gapsArray].includes(index)){
              masterGaps[gapsArray].push(index);
            }
          }
        }
        if (i != 0 && j != 0) {
          if (grid[index - d - 1] == 0) {
            gapsArray = undefined;
            for (y = 0; y < masterGaps.length; y++) {
              if (masterGaps[y].includes(index - d - 1)) {
                gapsArray = y;
              }
            }
            if (!masterGaps[gapsArray].includes(index)){
              masterGaps[gapsArray].push(index);
            }
          }
        }
      }
    }
  }
  return masterGaps;
}

function DFS(grid, i, gaps, d) {
  gaps.push(i);
  if (i % d != 0) {
    if (grid[i-1] == 0 && !gaps.includes(i-1)) {
      gaps = gaps.concat(DFS(grid, i-1, gaps, d).filter((item) => gaps.indexOf(item) < 0));
    }
  }
  if (i < Math.pow(d, 2) - d) {
    if (grid[i+d] == 0 && !gaps.includes(i+d)) {
      gaps = gaps.concat(DFS(grid, i+d, gaps, d).filter((item) => gaps.indexOf(item) < 0));
    }
    if (i % d != 0) {
      if (grid[i+d-1] == 0 && !gaps.includes(i+d-1)) {
        gaps = gaps.concat(DFS(grid, i+d-1, gaps, d).filter((item) => gaps.indexOf(item) < 0));
      }
    }
    if (i % d != d - 1) {
      if (grid[i+d+1] == 0 && !gaps.includes(i+d+1)) {
        gaps = gaps.concat(DFS(grid, i+d+1, gaps, d).filter((item) => gaps.indexOf(item) < 0));
      }
    }
  }
  if (i % d != d-1) {
    if (grid[i+1] == 0 && !gaps.includes(i+1)) {
      gaps = gaps.concat(DFS(grid, i+1, gaps, d).filter((item) => gaps.indexOf(item) < 0));
    }
  }
  if (i >= d) {
    if (grid[i-d] == 0 && !gaps.includes(i-d)) {
      gaps = gaps.concat(DFS(grid, i-d, gaps, d).filter((item) => gaps.indexOf(item) < 0));
    }
    if (i % d != 0) {
      if (grid[i-d-1] == 0 && !gaps.includes(i-d-1)) {
        gaps = gaps.concat(DFS(grid, i-d-1, gaps, d).filter((item) => gaps.indexOf(item) < 0));
      }
    }
    if (i % d != d - 1) {
      if (grid[i-d+1] == 0 && !gaps.includes(i-d+1)) {
        gaps = gaps.concat(DFS(grid, i-d+1, gaps, d).filter((item) => gaps.indexOf(item) < 0));
      }
    }
  }
  return gaps;
}
