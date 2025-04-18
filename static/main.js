const crop_data = [
    { 
        date: "2025-02-25", crop: "Tomato", cropType: "common", model: "1200", price: "₹30" 
    },
    { 
        date: "2025-02-26", crop: "Tomato", cropType: "common",model: "1600", price: "₹40" 
    },
    {
         date: "2025-02-27", crop: "Tomato", cropType: "common", model: "1800", price: "₹45" 
    }
];
const iot_data = [
    {
        date:"2025-02-25", time:"00:00 - 4:00", temperature:"25", humidity:"70",co2:"60"
    },
    {
        date:"2025-02-25", time:"00:00 - 4:00", temperature:"25", humidity:"70",co2:"60"
    },
    {
        date:"2025-02-25", time:"40:00 - 24:00", temperature:"25", humidity:"90",co2:"80"
    },
    {
        date:"2025-02-26", time:"00:00 - 10:00", temperature:"25", humidity:"30",co2:"60"
    }
]
const tableprice = document.getElementById("table-price");
const tableiot=document.getElementById("table-iot");
const predict=document.getElementById('predict');
const getdata=document.getElementById('getdata');
const plantationDate=document.getElementById('plantationDate');
const crop=document.getElementById('crop');
const harvestDate=document.getElementById('harvestDate');

predict.addEventListener("click",populate_price);
getdata.addEventListener("click",populate_iot);
function populate_price(){
    if(!plantationDate.value || crop.value==="SELECT"){
        alert("please enter valid Plantation Date and Crop");
        return;
    }
    const plantationDateInput=plantationDate.value;
    const cropInput=crop.value;
    const payload = {
        features:[plantationDateInput,cropInput]
    }
    fetch('/predictTrend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    }).then(
        response=>response.json()
    ).then(response=>{
        console.log(response.message);
    }
    )
    // crop_data.forEach(item => {
    //     let row = `<tr>
    //         <td>${item.date}</td>
    //         <td>${item.crop}</td>
    //         <td>${item.cropType}</td>
    //         <td>${item.model}</td>
    //         <td>${item.price}</td>
    //     </tr>`;
    //     tableprice.innerHTML += row;  
    // });
}

function populate_iot(){
    if(!plantationDate.value || crop.value==="SELECT"){
        alert("please enter valid Plantation Date and Crop");
        return;
    }
    if(!harvestDate.value){
        alert("please enter valid Harvest Date");
        return;
    }
    const harvestDateInput = harvestDate.value;
    const plantationDateInput=plantationDate.value;
    const cropInput=crop.value;
    const payload ={
        features:[plantationDateInput,cropInput,harvestDateInput]
    }
    fetch('/predictIOT', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(
        response=>response.json()
    ).then(response=>{
        console.log(response.message);
    }
    )
    // iot_data.forEach(item => {
    //     let row = `<tr>
    //         <td>${item.date}</td>
    //         <td>${item.time}</td> <!-- Added 'time' field -->
    //         <td>${item.temperature}</td>
    //         <td>${item.humidity}</td>
    //         <td>${item.co2}</td>
    //     </tr>`;
    //     tableiot.innerHTML += row;  
    // });
}