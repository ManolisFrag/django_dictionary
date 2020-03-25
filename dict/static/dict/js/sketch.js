let video;
let poseNet;
let pose;
let skeleton;
let recordd;
let toggle;

let json = {}; // new  JSON Object

json.id = 0;
json.name = 1;
let i = 0;

var data = {};

let wrists_array = [];
let all_coordinates = [];
var ww = 640;
var hh = 360;


function setup() {
  createCanvas(ww, hh);
  // canvas.parent('jumbo-canvas');
  // canvas.position(width/3, height/2);
  video = createCapture(VIDEO);
  video.size(ww,hh);
  video.hide();
  poseNet = ml5.poseNet(video, modelLoaded);
  poseNet.on('pose', gotPoses);
  button = createButton('Start recording');
  button.position(width/4, height+220);
  button.mousePressed(Record_sign);
  col = color("#007bff");
  button.style('font-size', '40px');
  button.style('color', 255);
  button.style('background-color', col);

  // button = createButton('STOP recording');
  // button.position(width/3, height+150);
  // button.style('font-size', '30px');
  // button.style('background-color', col);
  // button.mousePressed(stop_sign);
  recordd = false;
  toggle = false;
  var x = document.getElementById("id_pose_array");
  x.style.display = "none";
  var yy = document.getElementsByTagName("LABEL")[0];
  yy.style.display = "none";
}



function gotPoses(poses) {
  //console.log(poses);
  if (poses.length > 0) {
    pose = poses[0].pose;
    skeleton = poses[0].skeleton;
  }
}

function modelLoaded() {
  console.log('poseNet ready');
}

function draw() {
  background(200);
  
  image(video, 0, 0);

  recordd = false;
  if (pose) {
    let eyeR = pose.rightEye;
    let eyeL = pose.leftEye;
    let d = dist(eyeR.x, eyeR.y, eyeL.x, eyeL.y);
    // fill(255, 0, 0);
    // ellipse(pose.nose.x, pose.nose.y, d);
    // fill(0, 0, 255);
    ellipse(pose.rightWrist.x, pose.rightWrist.y, 32);
    ellipse(pose.leftWrist.x, pose.leftWrist.y, 32);

    for (let i = 0; i < pose.keypoints.length; i++) {
      let x = pose.keypoints[i].position.x;
      let y = pose.keypoints[i].position.y;
      fill(0, 255, 0);
      ellipse(x, y, 16, 16);
    }
    // if (keyCode === UP_ARROW) {
    //   json.location_x = pose.rightWrist.x;
    //   json.location_y = pose.rightWrist.y;
    //   console.log(pose.rightWrist.x, pose.rightWrist.y);
    //   saveJSON(json, i.toString()+'.json');
    //   i = i+1;
    // }


    for (let i = 0; i < skeleton.length; i++) {
      let a = skeleton[i][0];
      let b = skeleton[i][1];
      strokeWeight(2);
      stroke(255);
      line(a.position.x, a.position.y, b.position.x, b.position.y);
    }

    //scaling
    eucl_dist = Math.hypot(pose.rightShoulder.x-pose.leftShoulder.x, pose.rightShoulder.y-pose.leftShoulder.y)
    // console.log(eucl_dist);
    all_coordinates = new Array(new Array(pose.nose.x-pose.nose.x,pose.nose.y-pose.nose.y), 
    new Array((pose.rightShoulder.x-pose.nose.x)/eucl_dist,(pose.rightShoulder.y - pose.nose.y)/eucl_dist),
    new Array((pose.leftShoulder.x-pose.nose.x)/eucl_dist,(pose.leftShoulder.y - pose.nose.y)/eucl_dist),
    new Array((pose.rightWrist.x-pose.nose.x)/eucl_dist,(pose.rightWrist.y - pose.nose.y)/eucl_dist),   
    new Array((pose.leftWrist.x-pose.nose.x)/eucl_dist,(pose.leftWrist.y - pose.nose.y)/eucl_dist)
    );
    // console.log("all coordinates",all_coordinates);
    // console.log("only wrists", new Array(all_coordinates[3]));
    
    
    //saving wrist in array
    if (toggle){
      wrists_array.push(new Array(all_coordinates[3]));
    }

  }
}
function Record_sign() {
  if (!toggle) {
    console.log("Start Recording");
    wrists_array = [];
    toggle = true;
    button.html('Stop Recording');
    button.style('background-color', '#fc1303');
  } else {
    toggle = !toggle
    console.log("Stop putting in the array");
    document.getElementById("id_pose_array").value = (wrists_array);
    button.html('Start recording');
    button.style('background-color', col);
  }
  
  // console.log("Start putting in the array");
  // wrists_array = [];
  // toggle = true;
  // wrists_array.push(new Array(pose.rightWrist.x,pose.rightWrist.y));
}

function stop_sign() {
  toggle = false;
  console.log("Stop Recording");  
  document.getElementById("id_pose_array").value = (wrists_array);

}
function getCol(matrix, col){
  var column = [];
  for(var i=0; i<matrix.length; i++){
     column.push(matrix[i][col]);
  }
  return column;
}



  