const csrftoken = $("[name=csrfmiddlewaretoken]").val();
function listallrooms() {
    $.ajax(
        {
            type : 'GET',
            url : '/api/listallrooms/',
            dataType : 'json',
            success  : function (data) {
                let val = `
                <button type="button" class="btn btn-primary btn-sm p-1" data-toggle="modal" data-target="#exampleModal">Add Room</button>
                <div class="row row-cols-1 row-cols-md-3">
                ${data.map(function(obj) {
                    let url = obj.display_pic;
                    let room_id = obj.id;
                    let btn_status;
                    let label = "free";
                    if(obj.room_stream_details !== "free"){
                        btn_status = "btn-success";
                        label="live";
                    }
                    else {
                        btn_status = "disabled";
                    }
                    return `
                     
                    <div class="card m-2 " style='max-width: 20em;min-width: 20em;max-height: 16em;min-height: 16em;'>
                        <div class="card-body" style='background-image:url(${url});background-size: cover'>
                            <div class="card-body">
                              <h1 class=" card-title">${obj.title}</h1>
                              <p class="card-text">${obj.description}</p>
                              <a href="${obj.room_stream_details}" target="_blank" class="btn btn-secondary btn-sm  mt-5 ${btn_status}">${label}</a>
                              <a href="#" onclick="openroom(${room_id})" class="btn btn-sm btn-primary mt-5">Go To Room</a>
                            </div>
                        </div>
                    </div>
                    `;
                }).join('')}
                </div>`;
                 document.getElementById("canvas").innerHTML= val;

            }
        }
    );
}

function addroom(form_id) {
    let id = `#${form_id}`;
    let form_data = $(id).serializeArray(); // This line collects data inputted by user in form
    document.getElementById("roomform").reset(); //This line resets the form that was filled by user after collecting data from it.
    let a = form_data[1].value;
    let b = form_data[2].value;
    var token = form_data[0].value;
    let input =JSON.stringify({"title":a,"description":b});
    $.ajax(
        {
            type : 'POST',
            url : '/api/addroom/',
            contentType :'application/json',
            data : input,
            headers: { "X-CSRFToken": token },
            success:function () {
                $("#close_modal").click();
                listallrooms();
            }
        }
    );
}


function listapplications(){
    $.ajax(
        {
            type: 'GET',
            url: '/api/listapplications/',
            contentType: 'application/json',
            success : function (data) {
                let label ="Accept"
                let val = `
            <style> 
                  table tr th{
                      padding: 2rem;
                  }
                  thead{
                   background-color: black;
                   background-size: cover;
               }
               .row1{
                   background-color: white;
                   background-size: cover;
               }
               
             </style>
             <h5 class="text-center text-sm-center">New Admission Requests</h5>
            <table class="table table-striped">
                <thead class="text-light">
                    <tr class="text-center">
                        <th >Ref_No.</th>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Email</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
            ${data.map(function(obj) {
                    return `
            <tr class="text-center row1">
                <td>${obj.reference}</td>
                <td>${obj.first_name} ${obj.last_name}</td>
                <td>${obj.phone}</td>
                <td>${obj.email}</td>
                <td><a class="btn btn-outline-success d-inline" onclick="acceptapplication(${obj.id})">${label}</a><a class="btn btn-outline-danger d-inline m-1" onclick="rejectapplication(${obj.id})">Reject</a></td>
            </tr>`;
                }).join('')}
            </tbody>`;
                let element = document.getElementById('canvas');
                element.innerHTML = val;
            }


        }
    );
}


function openroom(room_id) {   /*Teacher name feature pending*/

    let element = document.getElementById('canvas');
    let trigers = ` <div>
                    <button onclick='addcourse(${room_id})' class='btn btn-sm btn-success d-inline mr-1'>Add Course</button> 
                    <button onclick='addstudent(${room_id})' class="btn btn-sm  btn-success mr-1 d-inline">Add Student</button>
                    <button onclick='deleteroom(${room_id})' class="btn btn-sm  btn-danger mr-1 d-inline">Delete Room</button>
                    </div> `;
                element.innerHTML = trigers+
                    "<div id='subcan1'></div>" +
                    "<div id='subcan2'></div>" +
                    "<div id='subcan3'></div>";
    editroom(room_id);
    $.ajax(
        {
            type : 'GET',
            url : '/api/viewroom/'+room_id,
            contentType :'application/json',
            success : function (data) {
                let label ="teacher"
                let val = `
                <div class="row row-cols-1 row-cols-md-3">
                ${data.map(function(obj) {
                    return `
                    <div class="card m-2 " style='max-width: 20em;min-width: 20em;max-height: 16em;min-height: 16em;'>
                        <div class="card-body" >
                            <div class="card-body">
                              <h1 class=" card-title">${obj.c_name}</h1>
                              <p class="card-text">${obj.c_description}</p>
                              <a  class="btn btn-secondary btn-sm  mt-5 disabled">${label}</a> 
                            </div>
                        </div>
                    </div>
                    `;
                }).join('')}
                </div><h5>Students In This Room</h5>`;
                let elemen = document.getElementById('subcan2');
                elemen.innerHTML = val;
                roomstudents(room_id);
            }

        }
    );
}

function editroom(room_id) {
    $.ajax(
        {
            type : 'GET',
            url : '/api/editroom/'+room_id,
            contentType :'text/plain',
            success : function (data) {
                let eleme = document.getElementById('subcan1');
                eleme.innerHTML = `
                        <div class="row m-1 p-1 mt-5">
                            <div class="col-xs-12 col-md-6 ">
                                <form method="post" action="/dashboard/editroom/${room_id}/" enctype="multipart/form-data">
                                      <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                                      ${data}
                                      <button type="submit" class="btn btn-sm btn-info mt-1">submit</button>
                                 </form>
                            </div>
                        </div><h5>Courses In This Room</h5>`;
            }
        }
    );
}

function acceptapplication(id){
console.log("accept"+id);
}

function rejectapplication(id){
console.log("reject"+id);
}

function deleteroom(id){
     $.ajax(
        {
            type : 'POST',
            url : '/api/deleteroom/',
            contentType :'application/json',
            data : JSON.stringify({"id":id}),
            headers: { "X-CSRFToken": csrftoken },
            success:function () {
                listallrooms();
            }
        }
    );
}

function addstudent(id) {
console.log("add"+id);
}

function roomstudents(id) {
console.log("in room students list"+id);
}

function addcourse(id) {
console.log("add course"+id);
}