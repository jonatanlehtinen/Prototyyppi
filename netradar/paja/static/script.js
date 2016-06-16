"use strict";

var cnvs = document.getElementById("pongCanvas");
var cntx = cnvs.getContext("2d");

var ballRad = 10;
var x = cnvs.width / 2;
var y = cnvs.height - 30;
var dx = 2;
var dy = -2;

var score = 0;
var lives = 3;

var paddleWidth = 100;
var paddleHeight = 10;
var paddleX = (cnvs.width - paddleWidth) / 2;

var rightButtonPressed = false;
var leftButtonPressed = false;

var brickRowCount = 4;
var brickColumnCount = 8;
var brickWidth = 75;
var brickHeight = 20;
var brickPadding = 10;
var brickOffsetTop = 30;
var brickOffsetLeft = 30;

var bricks = [];
for(var c=0; c<brickColumnCount; c++) {
    bricks[c] = [];
    for(var r=0; r<brickRowCount; r++) {
        bricks[c][r] = { x: 0, y: 0, status: 1 };
    }
}

function collisionDetection() {
    for(var c=0; c<brickColumnCount; c++) {
        for(var r=0; r<brickRowCount; r++) {
            var b = bricks[c][r];
            if(b.status == 1) {
                if(x > b.x && x < b.x+brickWidth && y > b.y && y < b.y+brickHeight) {
                    dy = -dy;
                    b.status = 0;
                    score++;
                    if(score == brickRowCount*brickColumnCount) {
                        alert("You won, congratulations!");
                        document.location.reload();
                    }
                }
            }
        }
    }
}

function drawScore() {
    cntx.font = "16px Arial";
    cntx.fillStyle = "#0095DD";
    cntx.fillText("Score: "+score, 8, 20);
}

function drawLives() {
    cntx.font = "16px Arial";
    cntx.fillStyle = "#0095dd";
    cntx.fillText("Lives: "+lives, cnvs.width-65, 20);
}

function keyDownHandler(e) {
    if(e.keyCode === 39) {
        rightButtonPressed = true;
    }
    else if(e.keyCode === 37) {
        leftButtonPressed = true;
    }
}

function keyUpHandler(e) {
    if(e.keyCode === 39) {
        rightButtonPressed = false;
    }
    else if(e.keyCode === 37) {
        leftButtonPressed = false;
    }
}

function drawPaddle() {
    cntx.beginPath();
    cntx.rect(paddleX, cnvs.height - paddleHeight, paddleWidth, paddleHeight);
    cntx.fillStyle = "0095dd";
    cntx.fill();
    cntx.closePath();
}


function drawBall() {
    cntx.beginPath();
    cntx.arc(x, y, ballRad, 0, Math.PI * 2);
    cntx.fillStyle = "#0c6";
    cntx.fill();
    cntx.closePath();
}

function drawBricks() {
    for(var c=0; c<brickColumnCount; c++) {
        for(var r=0; r<brickRowCount; r++) {
            if(bricks[c][r].status == 1) {
                var brickX = (c*(brickWidth+brickPadding))+brickOffsetLeft;
                var brickY = (r*(brickHeight+brickPadding))+brickOffsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                cntx.beginPath();
                cntx.rect(brickX, brickY, brickWidth, brickHeight);
                cntx.fillStyle = "#ff4d4d";
                cntx.fill();
                cntx.closePath();
            }
        }
    }
}

function draw() {
    cntx.clearRect(0, 0, cnvs.width, cnvs.height);
    drawBall();
    drawPaddle();
    drawScore();
    drawLives();
    collisionDetection();
    drawBricks();

    if(x + dx > cnvs.width-ballRad || x + dx < ballRad) {
        dx = -dx;
    }

    if(y + dy < ballRad) {
    dy = -dy;
    } else if(y + dy > cnvs.height-ballRad) {
        if(x>paddleX && x < paddleX + paddleWidth) {
            dy = -dy;
        }
        else {
        lives--;
if(!lives) {
    alert("GAME OVER");
    document.location.reload();
}
else {
    x = cnvs.width/2;
    y = cnvs.height-30;
    dx = 2;
    dy = -2;
    paddleX = (cnvs.width-paddleWidth)/2;
}
        }
    }

    if (rightButtonPressed && paddleX < cnvs.width - paddleWidth) {
        paddleX += 7;
    }
    else if (leftButtonPressed && paddleX > 0) {
        paddleX -= 7;
    }

    x += dx;
    y += dy;

    requestAnimationFrame(draw);
}

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

draw();
