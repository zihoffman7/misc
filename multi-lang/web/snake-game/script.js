var canvas = document.getElementById("game");
var ctx = canvas.getContext("2d");
var dir = "d", pressed = [], opposites = {"u" : "d", "d": "u", "l": "r", "r": "l"}, game = {active: false};

var Snake = function(dims, colors) {
  this.speed = 100;
  this.maxSpeed = 80;
  this.occupied = [Math.floor(dims*dims / 2), Math.floor(dims*dims / 2) + 1];
  this.colors = colors;
};

var Food = function(level, dims, pos, colors) {
  this.color = colors[Math.floor(Math.random() * colors.length)];
  this.scoreBoost = 1;
  this.pos = pos;
};

var Board = function(dims, boardColors, snakeColors, foodColors) {
  this.boardColors = boardColors;
  this.foodColors = foodColors;
  this.active = true;
  this.dims = dims;
  this.score = 0;
  this.squareX = Math.floor(canvas.height / dims);
  this.squareY = Math.floor(canvas.width / dims);
  this.snake = new Snake(dims, snakeColors);
  this.food = [];
  this.genFood();
  this.game();
  canvas.width -= canvas.width - this.squareX * dims;
  canvas.height -= canvas.height - this.squareY * dims;
};

Board.prototype.flash = function(text) {
  ctx.fillStyle = this.boardColors[2];
  ctx.font = "24px Arial";
  var textString = text, textWidth = ctx.measureText(textString ).width;
  ctx.fillText(textString , (canvas.width / 2) - (textWidth / 2), canvas.height / 2);
};

Board.prototype.game = function() {
  var update = function() {
    var movement;
    var offScreen = false;
    if (pressed.length) {
      dir = (dir == opposites[pressed[pressed.length - 1]]) ? pressed[pressed.length - 2] || dir : pressed[pressed.length - 1];
      pressed = [];
    }
    if (dir == "u") {
      movement = -1 * this.dims;
    }
    else if (dir == "d") {
      movement = this.dims;
      offScreen = ((this.snake.occupied[0] + movement) > this.dims * this.dims - 1);
    }
    else if (dir == "r") {
      movement = 1;
      offScreen = ((this.snake.occupied[0] + movement) % this.dims == 0);
    }
    else if (dir == "l") {
      movement = -1;
      offScreen = ((this.snake.occupied[0] + movement) % this.dims == this.dims - 1);
    }
    if ((this.snake.occupied[0] + movement) < 0) {
      offScreen = true;
    }
    this.snake.occupied.unshift(this.snake.occupied[0] + movement);
    this.snake.occupied.pop(this.snake.occupied.length - 1);
    var duplicates = arr => arr.filter((item, index) => arr.indexOf(item) != index);
    if (duplicates(this.snake.occupied).length || offScreen || this.snake.length == this.dims * this.dims - 1) {
      this.active = false; // game over
      this.flash("Click to play again");
    }
    else {
      this.refresh();
      setTimeout(update.bind(this), this.snake.speed); // Dynamic timeout updating
    }
  }
  setTimeout(update.bind(this), this.snake.speed);
};

Board.prototype.genFood = function() {
  var pos = this.pos = Math.floor(Math.random() * this.dims * this.dims);

  var retry = false;
  for (var i = 0; i < this.snake.occupied.length; i++) {
    if (this.snake.occupied[i] == this.pos) {
      retry = true;
    }
  }
  if (retry) {
    this.genFood();
  }
  else {
    this.food.push(new Food((this.score % 5 == 0 && this.score != 0) ? (this.score % 10 == 0) ? (this.score % 15 == 0) ? 3 : 2 : 1 : 0, this.dims, pos, this.foodColors));
  }
};

Board.prototype.refresh = function() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  var skip = true;

  for (var i = 0; i < this.dims; i++) {
    for (var j = 0; j < this.dims; j++) {
      skip = !skip;
      ctx.fillStyle = (skip) ? this.boardColors[0] : this.boardColors[1];
      var snakes = [];
      if (this.snake.occupied.indexOf(i * this.dims + j) > -1) {
        snakes.push({
          i: i,
          j: j,
          color: this.snake.colors[this.snake.occupied.indexOf(i * this.dims + j) % this.snake.colors.length]
        });
      }
      var arcs = [];
      for (var k = 0; k < this.food.length; k++) {
        if (this.food[k].pos == i * this.dims + j) {
          if (this.snake.occupied.indexOf(i * this.dims + j) > -1) {
            this.score += this.food.pop(this.food.indexOf(this.food[k])).scoreBoost;
            this.genFood();
            if (this.snake.speed > this.snake.maxSpeed) {
              this.snake.speed -= 5;
            }
            this.snake.occupied.push(i * this.dims + j);
          }
          else {
            arcs.push({
              color: this.food[k].color,
              radius: this.squareX/2,
              x: j*this.squareY + this.squareY/2,
              y: i*this.squareX + this.squareX/2
            });
          }
        }
      }

      ctx.fillRect(j*this.squareY, i*this.squareX, j*this.squareY + this.squareY, i*this.squareX + this.squareX);

      for (var arc of arcs) {
        ctx.fillStyle = arc.color;
        ctx.arc(arc.x, arc.y, arc.radius-2, 0, 2 * Math.PI);
        ctx.fill();
      }
      for (var block of snakes) {
        ctx.fillStyle = block.color;
        ctx.fillRect(block.j*this.squareY, block.i*this.squareX, block.j*this.squareY + this.squareY, block.i*this.squareX + this.squareX);
      }
    }
  }
  ctx.fillStyle = this.boardColors[2];
  ctx.font = "12px Arial";
  ctx.fillText(this.score, 2, 12);
};

var colors = {
  board: {
    lawn: ["#ebfaeb", "#d8f0d8", "black"],
    black: ["#2b2b2b", "#1a1a1a", "gainsboro"],
    grayscale: ["#f7f7f7", "white", "darkslategray"],
    white: ["white", "black", "gray"]
  },
  snake: {
    rainbow: ["#db8c8c", "#dbc58c", "#cedb8c", "#97db8c", "#8cdbc1", "#8cc7db", "#8c8ddb", "#b98cdb", "#db8ccb"],
    blue: ["#afd2db", "#93bac4", "#74a0ab", "#6298a6", "#4d8391", "#6298a6", "#74a0ab", "#93bac4"],
    purple: ["#a39bd1", "#968ccf", "#887dc9", "#7a6ec2", "#6c60b5", "#7a6ec2", "#887dc9", "#968ccf"],
    grayscale: ["#adadad", "#a1a1a1", "#8c8c8c", "#707070", "#8c8c8c", "#808080"],
    yellow: ["#dbd872", "#d6d367", "#d1ce5e", "#cfcb55", "#d1ce5e", "#d6d367"],
    transparent: ["rgb(115, 115, 115, 0.3)", "rgb(110, 110, 110, 0.3)", "rgb(105, 105, 105, 0.3)", "rgb(110, 110, 110, 0.3)"]
  },
  food: {
    normal: ["purple", "blue", "green", "orange"],
    grayscale: ["gainsboro", "gray", "lightgray", "darkgray"],
    colorful: ["#30bf5b", "#bf3056", "#307fbf", "#a2bf30"],
    purple: ["#b37bd1", "#8f55ad", "#7a3d99", "#652387"]
  }
};

document.addEventListener("keydown", function(e) {
  if (e.key == "Right" || e.key == "ArrowRight") {
    pressed.push("r");
  }
  if (e.key == "Left" || e.key == "ArrowLeft") {
    pressed.push("l");
  }
  if (e.key == "Up" || e.key == "ArrowUp") {
    pressed.push("u");
  }
  if (e.key == "Down"  || e.key == "ArrowDown") {
    pressed.push("d");
  }
});

document.getElementById("game").addEventListener("mousedown", function() {
  if (!game.active) {
    game = new Board(19, colors.board.black, colors.snake.rainbow, colors.food.colorful);
  }
});
