var canvas = document.getElementById("game");
var ctx = canvas.getContext("2d");
ctx.font = "14px Arial";

var entities = [];

var keysPressed = {
  right : false,
  left : false,
  up : false,
  down : false
};

class Entity {
  constructor(x, y) {
    entities.push(this);
    this.x = x;
    this.y = y;
  }
}

function genFood() {
  var radius, x, y, color;
  var probs = [0.4, 0.3, 0.2, 0.08, 0.02];
  var stats = [
    {
      probs: 0.4,
      color: "#eb4034",
      xp: 1
    },
    {
      probs: 0.3,
      color: "#2edb3c",
      xp: 2
    },
    {
      probs: 0.2,
      color: "#2b65d9",
      xp: 5
    },
    {
      probs: 0.08,
      color: "#d42ac6",
      xp: 10
    },
    {
      probs: 0.02,
      color: "#8d28d1",
      xp: 25
    }];
  do {
    radius = Math.floor(Math.random() * 8)
  } while (radius < 5);
  do {
    x = Math.floor(Math.random() * canvas.width + 1);
  } while (x >= canvas.width - radius || x <= radius);
  do {
    y = Math.floor(Math.random() * canvas.width + 1);
  } while (y >= canvas.height - radius || y <= radius);

  var goal = Math.random();
  var closest = stats[probs.indexOf(probs.reduce(function(prev, curr) {
    return (Math.abs(curr - goal) < Math.abs(prev - goal) ? curr : prev);
  }))];
  return {
    radius: radius,
    x: x,
    y: y,
    data: closest
  }
}

class Food extends Entity {
  constructor(data) {
    super(data.x, data.y);
    this.radius = data.radius;
    this.xp = data.data.xp;
    this.color = data.data.color;
    this.draw();
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
    ctx.closePath();
  }
}
var food = [new Food(genFood()), new Food(genFood()), new Food(genFood())];

class Player extends Entity {
  constructor(name, x, y) {
    super(x, y);
    this.score = 0;
    this.radius = 10;
    this.speed = 1;
    this.upgrades = {
      size: [18, 22, 26, 30, 34, 37, 40, 50],
      speed: [1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 2.85, 3.15],
      foodCount: [1, 2, 2, 2, 2, 3, 3, 5],
      xp: [0, 1, 2, 3, 4, 5, 6, 7, 8]
    };
  }
  increaseSize() {
    if (this.upgrades.size.length) {
      this.radius = this.upgrades.size[0];
      this.upgrades.size.shift();
    }
  }
  increaseSpeed() {
    if (this.upgrades.speed.length) {
      this.speed = this.upgrades.speed[0];
      this.upgrades.speed.shift();
    }
  }
  increaseFoodCount() {
    if (this.upgrades.foodCount.length) {
      for (var i = 0; i < this.upgrades.foodCount[0]; i++) {
        food.push(new Food(genFood()))
      }
      this.upgrades.foodCount.shift();
    }
  }
  increaseXPGain() {
    if (this.upgrades.xp.length > 1) {
      this.upgrades.xp.shift();
    }
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = "lightgray";
    ctx.fill();
    ctx.closePath();
  }
  move(x=0, y=0) {
    if (!(this.x + x >= canvas.width - this.radius || this.x + x <= this.radius)) {
      this.x += x;
    }
    if (!(this.y + y >= canvas.height - this.radius || this.y + y <= this.radius)) {
      this.y += y;
    }
  }
  checkBoundary() {
    if (this.x >= canvas.width - this.radius || this.x <= this.radius) {
      this.x = canvas.width / 2;
    }
    if (this.y >= canvas.height - this.radius || this.y <= this.radius) {
      this.y = canvas.height / 2;
    }
  }
  moveFromKeys(keys) {
    var x = 0;
    var y = 0;
    if (keys.up) {
      y -= this.speed;
    }
    if (keys.down) {
      y += this.speed;
    }
    if (keys.left) {
      x -= this.speed;
    }
    if (keys.right) {
      x += this.speed;
    }
    this.move(x, y);
  }
}

var player = new Player("hi", canvas.width/2, canvas.height/2);

setInterval(function() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  entities.forEach(function(entity) {
    entity.draw();
  });
  player.moveFromKeys(keysPressed);
  player.checkBoundary();
  food.forEach(function(f, ind) {
    if (Math.abs(player.x - f.x) < player.radius + f.radius && Math.abs(player.y - f.y) < player.radius + f.radius) {
      player.score += f.xp + player.upgrades.xp[0];
      delete f.x;
      food.splice(ind, 1, new Food(genFood()))
    }
  });
  ctx.fillStyle = "white";
  ctx.fillText("Score: " + player.score, 8, 20);
}, 10);

document.addEventListener("keydown", function(e) {
  if (e.key == "Right" || e.key == "ArrowRight") {
    keysPressed.right = true;
  }
  if (e.key == "Left" || e.key == "ArrowLeft") {
    keysPressed.left = true;
  }
  if (e.key == "Up" || e.key == "ArrowUp") {
    keysPressed.up = true;
  }
  if (e.key == "Down" || e.key == "ArrowDown") {
    keysPressed.down = true;
  }
});

document.addEventListener("keyup", function(e) {
  if (e.key == "Right" || e.key == "ArrowRight") {
    keysPressed.right = false;
  }
  if (e.key == "Left" || e.key == "ArrowLeft") {
    keysPressed.left = false;
  }
  if (e.key == "Up" || e.key == "ArrowUp") {
    keysPressed.up = false;
  }
  if (e.key == "Down" || e.key == "ArrowDown") {
    keysPressed.down = false;
  }
});

var upgradeData = {
  cost: [20, 40, 80, 120, 200, 500, 1000, 2400, "Maxed"],
  size: 0,
  speed: 0,
  count: 0,
  xp: 0
}

function events(id, text, category, toCall) {
  document.getElementById(id).addEventListener("click", function() {
    if (category >= 8) {
      document.getElementById("message").innerHTML = "You are already at max level";
    }
    else if (upgradeData.cost[category] > player.score) {
      document.getElementById("message").innerHTML = "Not enough xp";
    }
    else {
      player.score -= upgradeData.cost[category];
      category++;
      toCall.call(player);
      document.getElementById(id).innerHTML = text + " level " + category + ": Upgrade cost: " + upgradeData.cost[category];
    }
  });
}

document.getElementById("game-size").innerHTML = "Size level " + upgradeData.size + ": Upgrade cost: " + upgradeData.cost[upgradeData.size];
document.getElementById("game-speed").innerHTML = "Speed level " + upgradeData.speed + ": Upgrade cost: " + upgradeData.cost[upgradeData.size];
document.getElementById("game-count").innerHTML = "XP Count level " + upgradeData.count + ": Upgrade cost: " + upgradeData.cost[upgradeData.size];
document.getElementById("game-xpGain").innerHTML = "XP Gain level " + upgradeData.xp + ": Upgrade cost: " + upgradeData.cost[upgradeData.size];

events("game-size", "Size", upgradeData.size, player.increaseSize);
events("game-count", "XP Count", upgradeData.count, player.increaseFoodCount);
events("game-xpGain", "XP Gain", upgradeData.xp, player.increaseXPGain);
events("game-speed", "Speed", upgradeData.speed, player.increaseSpeed);
