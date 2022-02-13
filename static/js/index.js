var start;
var end;
var chain = [];

$(document).ready(function() {
    $("#submit").click(handleGuess);
    $("#undo").click(undoGuess);
    $("#forfeit").click(showPath);

    start = $("#start").html();
    end = $("#end").html();

    chain.push(start);
    displayChain(chain);
});

function handleGuess() {
    curr = $("#chain").children().last().html();
    next = $("#guess").val();
    $("#guess").val("");

    $.ajax({
        url : "/validate",
        type : "POST",
        data : JSON.stringify({
            curr : curr,
            next : next
        }),
        contentType: "application/json",
        success : function(response) {
            if (response.success) {
                chain.push(next);
                displayChain(chain);

                if (next == end) {
                    $("#form").html("You won!");
                    showPath();
                }
            } else {
                alert(response.message);
            }
        }, error : serverError
    });
}

function undoGuess() {
    if (chain.length > 1) {
        chain.pop();
    }

    displayChain(chain);
}

function showPath() {
    $.ajax({
        url : "/path",
        type : "POST",
        success : function(response) {
            path = response.path;
            content = "<p>The shortest path was ";

            for (var i = 0; i < path.length; i++) {
                content = content + path[i];
                if (i < path.length - 1) {
                    content = content + ", ";
                }
            }

            content = content + ". Refresh for a new game.</p>";
            $("#path").html(content);
        }, error: serverError
    });
}

function displayChain(chain) {
    content = "";
    for (var i = 0; i < chain.length; i++) {
        content = content + "<p>" + chain[i] + "</p>";
    }

    $("#chain").html(content);
}

function serverError() {
    alert("Internal server error.");
}
