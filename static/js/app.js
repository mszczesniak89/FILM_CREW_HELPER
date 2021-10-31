/*jshint esversion: 6 */
/*global console*/
'use strict';

const ot_prompt = document.querySelector("#ot_prompt");
const date = document.querySelector("#id_date");
const start_hour = document.querySelector("#start_hour");
const end_hour = document.querySelector("#end_hour");
let date_value = 0;
let start = 0;
let end = 0;
const working_hours_context = document.querySelector("#working_hours").value;
let working_hours = 0;


if (working_hours_context === '1') {
      working_hours = 10;
} else if (working_hours_context === '2') {
      working_hours = 11;
} else if (working_hours_context === '3') {
      working_hours = 12;
}

date.addEventListener('blur', function (event) {
      date_value = date.value;
      let temp_start = new Date(date_value);
      let temp_end = new Date (date_value);
      temp_start.setHours(8);
      temp_end.setHours(20);
      start_hour.value = temp_start.toISOString().substring(0, 16);
      end_hour.value = temp_end.toISOString().substring(0, 16);
});





start_hour.addEventListener('blur', function (event) {
      start = start_hour.value;
});


end_hour.addEventListener('blur', function (event) {
      end = end_hour.value;
      let t1 = new Date(start);
      let t2 = new Date(end);
      let diff = t2 - t1;
      if (Math.floor(diff/3600e3) >= working_hours) {
            console.log(diff/3600e3);
            ot_prompt.style.display = "block";
      } else {
            console.log(diff/3600e3);
            ot_prompt.style.display = "none";
      }
});
