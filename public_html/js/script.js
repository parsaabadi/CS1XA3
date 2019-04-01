
$(document).ready(

    function () {
        $(document).keydown(function(press){   // for supporting keyboard and taking the keystroke values everytime user input
            var keypressed = press.which;
            if(keypressed == "38" && direction != "down") direction = "up";
            else if(keypressed == "40" && direction != "up") direction = "down";
            else if(keypressed == "37" && direction != "right") direction = "left";
            else if(keypressed == "39" && direction != "left") direction = "right";
        });
        // checking snake strike itself
        function self_collision(snakeArray, xcord, ycord) {
            for(var i=0; i < snakeArray.length; i++) {
                if(snakeArray[i].xcord == xcord && snakeArray[i].ycord == ycord)
                    return true;
            }
            return false;
        }
        // creating snake in the canvas
        function paintSnaketarget(xcord, ycord, color) {
            gContext.fillStyle = color;
            gContext.fillRect(xcord*widthpercell, ycord*widthpercell, widthpercell, widthpercell);
            gContext.strokeStyle = "white";
            gContext.strokeRect(xcord*widthpercell, ycord*widthpercell, widthpercell, widthpercell);
        }

        var gameCanvas_id = $('#game-id')[0];
        var width_game_screen = 480, height_game_screen = 600;
        var total_points, direction;
        var target;
        var widthpercell = 12;
        var run_game;
        var snakes;
        var gContext = gameCanvas_id.getContext("2d");
        // load_game into the canvas with all initial values
        function load_game() {
            total_points = 0;
            direction = "right";
            snakes = [];
            for (var i = 4; i>=0;i--) {
                snakes.push({xcord:i, ycord:0});
            }
            target = {
                xcord: Math.floor(Math.random()*(width_game_screen-widthpercell)/widthpercell),
                ycord: Math.floor(Math.random()*(height_game_screen-widthpercell)/widthpercell)
            };

            if (run_game != "undefined") clearInterval(run_game);
            run_game = setInterval(canvasGame, 120);
        }
        load_game();    // calling load_game function

        // canvas games method for controlling the game and play rules
        function canvasGame() {
            gContext.fillStyle = "white";
            gContext.fillRect(0,0, width_game_screen, height_game_screen);
            var nxcord = snakes[0].xcord;
            var nycord = snakes[0].ycord;

            // getting next value in the canvas
            if(direction == "right") nxcord++;
            else if(direction == "left") nxcord--;
            else if(direction == "up") nycord--;
            else if(direction == "down") nycord++;

            // checking the value of the coordinate of snake it is inside the canvas or strike itself
            if(nxcord == -1 || nxcord == width_game_screen/widthpercell || nycord == -1 || nycord == height_game_screen/widthpercell || self_collision(snakes, nxcord, nycord))
            {
                //restart game
                load_game();
                //Lets organize the code a bit now.
                return;
            }
            // if snake reaches the target
            if(nxcord == target.xcord && nycord == target.ycord)
            {
                var tail = {xcord: nxcord, ycord: nycord};
                total_points++;

                target = {
                    xcord: Math.floor(Math.random()*(width_game_screen-widthpercell)/widthpercell),
                    ycord: Math.floor(Math.random()*(height_game_screen-widthpercell)/widthpercell)
                };
            }
            else    // just moving the snake in the next direction
            {
                var tail = snakes.pop(); //pops out the last cell
                tail.xcord = nxcord; tail.ycord = nycord;
            }
            snakes.unshift(tail);
            for(var i = 0; i < snakes.length; i++)
            {
                var c = snakes[i];
                //Lets paint 10px wide cells
                paintSnaketarget(c.xcord, c.ycord, "green");
            }

            paintSnaketarget(target.xcord, target.ycord, "red");
            gContext.fillStyle = "black";
            var score_text = "Points: " + total_points;
            gContext.fillText(score_text, 5, height_game_screen-5);
        }
    }
);