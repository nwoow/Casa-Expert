
// -----------------------------------

const img1 = document.getElementsByClassName("img1")[0];
const img2 = document.getElementsByClassName("img2")[0];
const img3 = document.getElementsByClassName("img3")[0];
const img4 = document.getElementsByClassName("img4")[0];
const img5 = document.getElementsByClassName("img5")[0];
function checkFun() {
  if (document.getElementById("s1").checked) {
    img4.style.transform = "translate3d(-160%,40%,0)";
    img4.style.filter = "blur(1px)";
    img4.style.zIndex = "2";
    img5.style.transform = "translate3d(-80%,20%,0)";
    img5.style.zIndex = "2";
    img5.style.filter = "blur(0.5px)";
    img1.style.transform = "translate3d(0,0,0)";
    img1.style.filter = "blur(0px)";
    img1.style.zIndex = "3";
    img2.style.transform = "translate3d(80%,20%,0)";
    img2.style.zIndex = "2";
    img2.style.filter = "blur(0.5px)";
    img3.style.transform = "translate3d(160%,40%,0)";
    img3.style.zIndex = "1";
    img3.style.filter = "blur(1px)";
  } else if (document.getElementById("s2").checked) {
    img5.style.transform = "translate3d(-160%,40%,0)";
    img5.style.zIndex = "1";
    img5.style.filter = "blur(1px)";
    img1.style.transform = "translate3d(-80%,20%,0)";
    img1.style.zIndex = "2";
    img1.style.filter = "blur(0.5px)";
    img3.style.transform = "translate3d(80%,20%,0)";
    img3.style.zIndex = "2";
    img3.style.filter = "blur(0.5px)";
    img2.style.transform = "translate3d(0,0,0)";
    img2.style.zIndex = "3";
    img2.style.filter = "blur(0px)";
    img4.style.transform = "translate3d(160%,40%,0)";
    img4.style.zIndex = "1";
    img4.style.filter = "blur(1px)";
  } else if (document.getElementById("s3").checked) {
    img1.style.transform = "translate3d(-160%,40%,0)";
    img1.style.zIndex = "1";
    img1.style.filter = "blur(1px)";
    img2.style.transform = "translate3d(-80%,20%,0)";
    img2.style.zIndex = "2";
    img2.style.filter = "blur(0.5px)";
    img2.style.filter = "blur(0.5px)";
    img4.style.transform = "translate3d(80%,20%,0)";
    img4.style.zIndex = "2";
    img4.style.filter = "blur(0.5px)";
    img4.style.filter = "blur(0.5px)";
    img3.style.transform = "translate3d(0,0,0)";
    img3.style.zIndex = "3";
    img3.style.filter = "blur(0px)";
    img5.style.transform = "translate3d(160%,40%,0)";
    img5.style.zIndex = "1";
    img5.style.filter = "blur(1px)";
  } else if (document.getElementById("s4").checked) {
    img2.style.transform = "translate3d(-160%,40%,0)";
    img2.style.zIndex = "1";
    img2.style.filter = "blur(1px)";
    img3.style.transform = "translate3d(-80%,20%,0)";
    img3.style.zIndex = "2";
    img3.style.filter = "blur(0.5px)";
    img5.style.transform = "translate3d(80%,20%,0)";
    img5.style.zIndex = "2";
    img5.style.filter = "blur(0.5px)";
    img4.style.transform = "translate3d(0,0,0)";
    img4.style.zIndex = "3";
    img4.style.filter = "blur(0px)";
    img1.style.transform = "translate3d(160%,40%,0)";
    img1.style.zIndex = "1";
    img1.style.filter = "blur(1px)";
  } else if (document.getElementById("s5").checked) {
    img3.style.transform = "translate3d(-160%,40%,0)";
    img3.style.zIndex = "1";
    img3.style.filter = "blur(1px)";
    img4.style.transform = "translate3d(-80%,20%,0)";
    img4.style.zIndex = "2";
    img4.style.filter = "blur(0.5px)";
    img1.style.transform = "translate3d(80%,20%,0)";
    img1.style.zIndex = "2";
    img1.style.filter = "blur(0.5px)";

    img5.style.transform = "translate3d(0,0,0)";
    img5.style.zIndex = "3";
    img5.style.filter = "blur(0px)";
    img2.style.transform = "translate3d(160%,40%,0)";
    img2.style.zIndex = "1";
    img2.style.filter = "blur(1px)";
  } else {
  }
}
checkFun();
