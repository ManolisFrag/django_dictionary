let playing = false;

let button;


let fingers = []; 

function setup() {
  // console.log(videoo);
  // specify multiple formats for different browsers
  createCanvas(5, 5);
  // fingers = createVideo(videoo);
  for (let i = 0; i < 10; i += 1) {
    fingers[i] = createVideo("/static/dict/videos/"+videoo[i]+".mp4");
    fingers[i].size(300,300);
    fingers[i].showControls();
    // fingers[i].hide();
    // fingers[i].loop();
  }
  console.log([fingers]);
  // fingers = createVideo("/static/dict/videos/ASIA.mp4")
  // console.log(videoo);
   // 
  
  // button = createButton('play');
  // button.mousePressed(toggleVid); // attach button listener
}

