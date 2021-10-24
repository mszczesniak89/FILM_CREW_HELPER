
const ot_prompt = document.querySelector("#ot_prompt")
const start_hour = document.querySelector("#start_hour");
const end_hour = document.querySelector("#end_hour");
let start = 0;
let end = 0;

console.log("sup?");

start_hour.addEventListener('blur', function (event) {
      start = start_hour.value
});


end_hour.addEventListener('blur', function (event) {
      end = end_hour.value;
      let t1 = new Date(start);
      let t2 = new Date(end);
      let diff = t2 - t1;
      if (Math.floor(diff/3600e3) >= 12) {
            console.log(diff/3600e3);
            ot_prompt.style.display = "block";
      } else {
            console.log(diff/3600e3);
            ot_prompt.style.display = "none";
      }
});





