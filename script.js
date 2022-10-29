function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                allText = rawFile.responseText;
                content(allText);
            }
        }
    }
    rawFile.send(null);
}

// readTextFile("./result.txt");

var posList = [];

function content(lines){
    var groups = lines.split("@\r\n");
    // console.log(groups);
    for (let i = 0; i < groups.length; i++){
        var lines = groups[i].split('\r\n');
        
        // console.log(lines);
        posList.push([]);
        for (let l = 0; l < lines.length; l++){
            if (lines[l] == '') {
                continue;
            }
            let pos = lines[l].split(' ');
            let Y = parseFloat(pos[0])
            let X = parseFloat(pos[1]) 
            posList[i].push([Y, X]);
        }
        // console.log(posList[i]);
        // let center = [(posList[0][0] + posList.slice(-1)[0]) / 2, (posList[0][1] + posList.slice(-1)[1]) / 2];
        // postList.unshift(center);
    }
    // console.log((posList[0].slice(-1)[0][1]))
}