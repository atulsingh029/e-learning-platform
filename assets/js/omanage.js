const csrftoken = $("[name=csrfmiddlewaretoken]").val();
let roomslist;
function update_room(){
    $.ajax({type:'GET',url:'/api/listallrooms/',contentType:'application/json',success:function (data){
                        roomslist=data;
                    }});
}
function all_c() {
    return $.ajax({
        type: 'GET',
        url: '/api/listallcourses/',
        dataType: 'json',
        success: function (data) {
            handleData1(data);
        }
    });
}
update_room();
all_c();
let allcourses;
function handleData1(data) {
    allcourses = data;
}


function all_t() {
    return $.ajax({
        type: 'GET',
        url: '/api/listallteachers/',
        dataType: 'json',
        success: function (data) {
            handleData2(data);
        }
    });
}

let allteachers;
function handleData2(data) {
    allteachers = data;
}

function search() {
    let data = document.getElementById("search_key");
    let area = document.getElementById("search_result");
    let key = data.value;
    data.value = "";
    if (key === '') {
        alert("Invalid Search");
    }
    else {
        $.ajax(
            {
                type: 'POST',
                url: '/api/search/',
                contentType: 'application/json',
                data: JSON.stringify({ "key": key }),
                headers: { "X-CSRFToken": csrftoken },
                success: function (data) {
                    let teacher = data.teacher;
                    let student = data.student;
                    let val = `
                <div class="row row-cols-1 row-cols-md-3">
                
                ${student.map(function (obj) {
                    return `
                    <style>
                        .card-img{
                            border-radius: 100%;
                            align-items: center;
                            background-repeat: no-repeat;
                            background-position: 50% 50%;
                            background-size: cover;
                            height: 100px;
                            width: 100px;
                        }
                        .name{
                            overflow: hidden;
                            text-overflow: ellipsis;
                            line-height: 16px;
                            max-height: 32px;
                        }
                    
                    </style>
                    <div class="card m-2 border-dark rounded" style='max-width: 20em;min-width: 20em;max-height: 16em;min-height: 16em;'>
                        <div class="row">
                            <div class="col-4">
                                 <img src="${obj.user.profile_pic}" alt="profile_pic" class="card-img p-1">
                            </div>
                        <div class="col-8 pt-2">
                            <h6 class="pr-2 name text-capitalize">${obj.user.first_name} ${obj.user.last_name}</h6>
                            <h6 class="text-info">@${obj.user.username}</h6>
                            <h6 class="text-info">Student</h6>
                        </div>
                        </div>
                        <div class="card-body">
                          <h6 class="text-center">${obj.from_room.title} <span style="color: #1e7e34"> : ${obj.from_room.room_stream_details}</span></h6>
                          <hr>
                          <h6 class=""><i class = "material-icons vertical-align-middle padding-bottom-3">call</i> ${obj.user.phone}</h6>
                          <h6 class="light name"><i class = "material-icons vertical-align-middle padding-bottom-3" >message</i> ${obj.user.email}</h6>
                        </div>    
                    </div>
                    `;
                }).join('')}
                </div>`;

                let val2 = `
                <div class="row row-cols-1 row-cols-md-3">
                
                ${teacher.map(function (obj) {
                    return `
                    <style>
                        .card-img{
                            border-radius: 100%;
                            align-items: center;
                            background-repeat: no-repeat;
                            background-position: 50% 50%;
                            background-size: cover;
                            height: 100px;
                            width: 100px;
                        }
                        .name{
                            overflow: hidden;
                            text-overflow: ellipsis;
                            line-height: 16px;
                            max-height: 32px;
                        }
                    
                    </style>
                    <div class="card m-2 border-dark rounded" style='max-width: 20em;min-width: 20em;max-height: 16em;min-height: 16em;'>
                        <div class="row">
                            <div class="col-4">
                                 <img src="${obj.user.profile_pic}" alt="profile_pic" class=" card-img p-1">
                            </div>
                        <div class="col-8 pt-2">
                            <h6 class="pr-2 name text-capitalize">${obj.user.first_name} ${obj.user.last_name}</h6>
                            <h6 class="text-info">@${obj.user.username}</h6>
                            <h6 class="text-info">Teacher</h6>
                        </div>
                        </div>
                        <div class="card-body">
                          <hr>
                          <h6 class=""><i class = "material-icons vertical-align-middle padding-bottom-3">call</i> ${obj.user.phone}</h6>
                          <h6 class="light name"><i class = "material-icons vertical-align-middle padding-bottom-3" >message</i> ${obj.user.email}</h6>
                        </div>    
                    </div>
                    `;
                }).join('')}
                </div>`;
                 val = val+val2;
                area.innerHTML=val;
                }
            }
        );
    }
}

/*completed*/
function listallrooms() {
    $.ajax(
        {
            type: 'GET',
            url: '/api/listallrooms/',
            dataType: 'json',
            success: function (data) {
                let val = `
                <button type="button" class="btn btn-primary btn-sm p-1" data-toggle="modal" data-target="#exampleModal">Add Room</button>
                <div class="row row-cols-1 row-cols-md-3">
                ${data.map(function (obj) {
                    let url = obj.display_pic;
                    let room_id = obj.id;
                    let btn_status;
                    let label = "free";
                    if (obj.room_stream_details !== "free") {
                        btn_status = "btn-success";
                        label = "live";
                    }
                    else {
                        btn_status = "disabled";
                    }
                    return `
                     
                    <div class="card m-2 border-dark rounded" style='max-width: 20em;min-width: 20em;max-height: 16em;min-height: 16em;'>
                        <div class="card-body" style='background-image:url(${url});background-size: cover'>
                            <h4 class="card-title">${obj.title}</h4>
                            <p class="card-text">${obj.description}</p>
                        </div>    
                        <div class="card-footer text-center">
                              <a href="${obj.room_stream_details}" target="_blank" class="btn btn-secondary btn-sm   ${btn_status}">${label}</a>
                              <a href="#" onclick="openroom(${room_id},${obj.organization.account},'${obj.reference}')" class="btn btn-sm btn-primary ">Go To Room</a>
                        </div>
                        
                    </div>
                    `;
                }).join('')}
                </div>`;
                document.getElementById("canvas").innerHTML = val;

            }
        }
    );
}

function listallcourses() {
    all_t();
    $.ajax(
        {
            type: 'GET',
            url: '/api/listallcourses/',
            dataType: 'json',
            success: function (data) {
                let val = `
                <button type="button" class="btn btn-primary btn-sm p-1" onclick="addcoursewithoutroom()">Add Course</button>
                <div class="row row-cols-1 row-cols-md-3">
                ${data.map(function (obj) {
                    var url = '';
                    let btn_status;
                    let btn_view = '';
                    let label = "disabled";
                    if (obj.c_status !== true) {
                        btn_status = "btn-success";
                        label = "active";
                    }
                    else {
                        btn_status = "btn-danger";
                        btn_view = 'disabled';

                    }
                    return `
                    
                    <div class="card m-2 border-dark rounded" style='max-width: 20em;min-width: 20em;max-height: 16em;min-height: 16em;'>
                        <div class="card-body" style='background-image:url(${url});background-size: cover'>
                            <h4 class="card-title">${obj.c_name}</h4>
                            <p class="card-text">${obj.c_description}</p>
                            <h6 class="card-title">Instructor : ${obj.instructor.user.first_name}</h6>
                        </div>    
                        <div class="card-footer text-center">
                              <a target="_blank" class="btn btn-sm  ${btn_status}">${label}</a>
                              <a href="#" onclick="opencourse(${obj.c_id})" class="btn btn-sm btn-primary ${btn_view}">View Course</a>
                        </div>
                        
                    </div>
                    `;
                }).join('')}
                </div>`;
                document.getElementById("canvas").innerHTML = val;

            }
        }
    );
}

/*completed*/
function addroom(form_id) {
    let id = `#${form_id}`; // #formid
    let form_data = $(id).serializeArray(); // This line collects data inputted by user in form
    document.getElementById("roomform").reset(); //This line resets the form that was filled by user after collecting data from it.
    let a = form_data[1].value;
    let b = form_data[2].value;
    if(a===''){
        let out = prompt("Enter Room Name");
        while(out===''){
            out = prompt("Enter Room Name");
        }
        a=out;
    }
    var token = form_data[0].value;
    let input = JSON.stringify({ "title": a, "description": b });
    $.ajax(
        {
            type: 'POST',
            url: '/api/addroom/',
            contentType: 'application/json',
            data: input,
            headers: { "X-CSRFToken": token },
            success: function () {
                $("#close_modal").click();
                listallrooms();
                update_room();
            }
        }
    );
}

/*completed*/
function listapplications() {
    $.ajax(
        {
            type: 'GET',
            url: '/api/listapplications/',
            contentType: 'application/json',
            success: function (data) {
                let label = "Accept"
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
                        <th>Ref_No.</th>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Email</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
            ${data.map(function (obj) {
                    return `
            <tr class="text-center row1">
                <td>${obj.reference}</td>
                <td>${obj.first_name} ${obj.last_name}</td>
                <td>${obj.phone}</td>
                <td>${obj.email}</td>
                <td><a class="btn btn-outline-success d-inline" onclick="acceptapplication('${obj.reference}')">${label}</a><a class="btn btn-outline-danger d-inline m-1" onclick="rejectapplication('${obj.reference}')">Reject</a></td>
            </tr>`;
                }).join('')}
            </tbody>`;
                let element = document.getElementById('canvas');
                element.innerHTML = val;
            }


        }
    );
}

/*completed*/
function openroom(room_id, o_id, reference) {   /*Teacher name feature pending*/
    all_t();
    let element = document.getElementById('canvas');
    let trigers = ` <div>
                    <button onclick='addcourseform(${room_id})' class='btn btn-sm btn-success d-inline mr-1'>Add Course</button>
                    <button onclick='deleteroom(${room_id})' class="btn btn-sm  btn-danger mr-1 d-inline">Delete Room</button>
                    </div> `;
    element.innerHTML = trigers +
        "<div id='subcan1'></div>" +
        "<div id='subcan2'></div>" +
        "<div id='subcan3'></div>";
    editroom(room_id, o_id, reference);
    $.ajax(
        {
            type: 'GET',
            url: '/api/viewroom/' + room_id,
            contentType: 'application/json',
            success: function (data) {
                let val = `
                <div class="row row-cols-1 row-cols-md-3">
                ${data.data.map(function (obj) {
                    if (obj.c_status === false) {
                        return `
                    <div class="card m-2 border-dark rounded" style='max-width: 20em;min-width: 20em;max-height: 16em;min-height: 16em;'>
                        <div class="card-body">
                            <h4 class="card-title">${obj.c_name}</h4>
                            <p class="card-text">${obj.c_description}</p>
                            <h6 class="card-title">Instructor : ${obj.instructor.user.first_name}</h6>
                        </div>    
                        <div class="card-footer text-center">
                              <a href="#" onclick="opencourse(${obj.c_id})" class="btn btn-sm btn-primary">View Course</a>
                        </div>
                        
                    </div>
                    `;
                    }
                }).join('')}
                </div><h5>Students In This Room</h5>`;
                let elemen = document.getElementById('subcan2');
                elemen.innerHTML = val;
                roomstudents(room_id, o_id, reference);
            }

        }
    );
}

function editroom(room_id, o_id, reference) {
    $.ajax(
        {
            type: "GET",
            url: "/api/editroom/" + room_id,
            contentType: "application/json",
            success: function (data) {
                let eleme = document.getElementById('subcan1');
                eleme.innerHTML = `
    <style>
        input{
            background-color:ghostwhite;
            border-top:0px; 
            border-left: 0px; 
            border-right: 0px; 
            width: 100%;
        }
        .abc:focus{
            outline: 0;
        }
       .A{
            width: auto;
        }
    
        table{
            width: 100%;
        }
    </style>
          <div class="row mt-5">
                <div class="col-xs-12 col-md-6 ">
                       <form method="post"  id="editroomform" enctype="multipart/form-data">
                            <table>   
                                <tr>
                                <td class="A"><label class="my-1" for="">Room Name</label></td>
                                <td class="B">:</td>
                                <td class="C"><input class="abc"  type="text" name="title" value="${data.title}" maxlength=20" required="" id="id_title"></td>
                                </tr>
                                <tr>
                                <td class="A"><label class=" my-1" for="">Description</label></td>
                                <td class="B">:</td>
                                <td class="C"><input type="text" class="abc" maxlength="150" required="" id="id_description" name="description" value="${data.description}"></td>
                                </tr>
                                <tr>
                                <td class="A"><label class=" my-1" for="">Picture</label></td>
                                <td class="B">:</td>
                                <td class="C"><input type="file" name="picture" accept="image/*" id="id_picture"></td> 
                                </tr>
                                <tr>
                                <td class="A"></td>
                                <td class="B"></td>
                                <td class="text-right"><a class="btn btn-info btn-sm " type="button" onclick="updateroom(${data.id})">Update</a></td>
                                </tr>
                            </table>
                       </form>
                </div>
                <div class="col-xs-12 col-md-6 ">
                    <div class="jumbotron jumbotron-fluid">
                        <div class="container">
                            <h3 class="display-5">Get your students onboard!</h3>
                            <p class="lead">Share this link with your students, once they signup using this link they will be automatically added to this room after your accept their application request.</p>
                            <h5>http://127.0.0.1:8000/r/${o_id}/${reference}</h5>
                        </div>
                    </div>
                </div>
          </div><h5>Courses In This Room</h5>`;
            }
        }
    );
}

/*completed*/
function acceptapplication(reference) {
    $.ajax(
        {
            type: 'POST',
            url: '/api/acceptapplications/',
            contentType: 'application/json',
            data: JSON.stringify({ "reference": reference }),
            headers: { "X-CSRFToken": csrftoken },
            success: function (data) {
                listapplications();
            }
        }
    );
}

/*completed*/
function rejectapplication(reference) {
    $.ajax(
        {
            type: 'POST',
            url: '/api/rejectapplications/',
            contentType: 'application/json',
            data: JSON.stringify({ "reference": reference }),
            headers: { "X-CSRFToken": csrftoken },
            success: function (data) {
                listapplications();
            }
        }
    );
}

/*completed*/
function deleteroom(id) {
    $.ajax(
        {
            type: 'POST',
            url: '/api/deleteroom/',
            contentType: 'application/json',
            data: JSON.stringify({ "id": id }),
            headers: { "X-CSRFToken": csrftoken },
            success: function () {
                listallrooms();
            }
        }
    );
}

/*completed*/
function roomstudents(id, o_id, reference) {
    $.ajax(
        {
            type: 'GET',
            url: '/api/listroomstudents/' + id,
            contentType: 'application/json',
            success: function (data) {
                let label = "Accept"
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
            <table class="table table-striped">
                <thead class="text-light">
                    <tr class="text-center">
                        <th >Username</th>
                        <th>Name</th>
                        
                        <th>Email</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                
            ${data.map(function (obj) {
                    return `
            <tr class="text-center row1">
                <td>${obj.username}</td>
                <td>${obj.first_name} ${obj.last_name}</td>
                <td>${obj.email}</td>
                <td><a class="btn btn-outline-danger btn-sm d-inline" onclick="removestudent('${obj.id}','${o_id}','${reference}')">Remove Student</a></td>
            </tr>`;
                }).join('')}
            </tbody>`;
                let element = document.getElementById('subcan3');
                element.innerHTML = val;
            }


        }
    );


}

function addnewcourse(id) {
    let data = $("#addcoursef").serializeArray();
    let teacher = document.getElementById("select_teacher");
    if (teacher.options[teacher.selectedIndex].value === "Choose Instructor For This Course" || data[0].value === "" || data[1].value === "") {
        alert("Invalid Input : Some Fields Missing");
    }
    else {
        var teacher_id = teacher.options[teacher.selectedIndex].value;
        $.ajax(
            {
                type: 'POST',
                url: '/api/addcourse/new/',
                contentType: 'application/json',
                data: JSON.stringify({ "room_id": id, "title": data[0].value, "description": data[1].value, "teacher_id": teacher_id }),
                headers: { "X-CSRFToken": csrftoken },
                success: function (data) {
                    alert("Course Added");
                    all_c();
                    if (data.take_to === 'listallcourses') {
                        listallcourses();
                    }
                    else {
                        openroom(id, data.o_id, data.reference);
                    }

                }
            }
        );
    }
}

function addexistingcourse(id) {
    let form = document.getElementById("select_data").value;
    let d = JSON.stringify({ "room_id": id, "c_id": form });
    $.ajax({
        type: 'POST',
        url: '/api/addcourse/existing/',
        contentType: 'application/json',
        data: d,
        headers: { "X-CSRFToken": csrftoken },
        success: function (data) {
            openroom(id, data.o_id, data.reference);
        }
    });

}


function addcoursewithoutroom() {
    if (allcourses === undefined) {
        alert("Some Error Occurred While Loading The Page, Please Refresh!");
    }
    let instructors = allteachers;
    let view = document.getElementById('canvas');
    view.innerHTML = `
                <style>
        input{
            background-color:ghostwhite;
            border-top:0px; 
            border-left: 0px; 
            border-right: 0px; 
            width: 100%;
        }
        select{
            background-color:ghostwhite;
            border-top:0px; 
            border-left: 0px; 
            border-right: 0px; 
            width: 75%;
        }
        .abc:focus{
            outline: 0;
        }
       .A{
            width: auto;
        }
    
        table{
            width: 100%;
        }
    </style>
    <div class="row">
    <div class="col col-md-6">
    <h5 class="display-5">Add A New Course</h5>
    <form method="post"  id="addcoursef">
         <table>   
             <tr>
                <td class="A"><label class="my-1" for="">Course Name</label></td>
                <td class="B">:</td>
                <td class="C"><input class="abc"  type="text" name="title" maxlength=20" required="" id="id_title"></td>
             </tr>
             <tr>
                <td class="A"><label class=" my-1" for="">Description</label></td>
                <td class="B">:</td>
                <td class="C"><input type="text" class="abc" maxlength="150" required="" id="id_description" name="description"></td>
             </tr>
             <tr>
                <td class="A"><label class="my-1" for="">Course Choose Instructor</label></td>
                <td class="B">:</td>
                <td class="C"><select class="abc" id="select_teacher">
                    <option selected>Choose Instructor For This Course</option>
                    ${instructors.map(function (obj) {
        return `
                        <option value="${obj.id}">${obj.first_name}${obj.last_name}</option>
                        `
    }).join('')}
                  </select></td>
             </tr>
             <tr>
                <td class="A"></td>
                <td class="B"></td>
                <td class="text-right"><a class="btn btn-info btn-sm " type="button" onclick="addnewcourse(-1)">Add</a></td>
             </tr>
         </table>
    </form>
</div>
    </div>`;
}


function addcourseform(id) {
    let existing_c = allcourses;
    if (existing_c === undefined) {
        alert("Some Error Occurred While Loading The Page, Please Refresh!");
    }
    let instructors = allteachers;
    $.ajax(
        {
            type: 'GET',
            url: '/api/viewroom/' + id,
            contentType: 'application/json',
            success: function (data) {
                let view = document.getElementById('canvas');
                view.innerHTML = `
                <h3 class='display-5 mb-3'>You Are Adding Course In ${data.title}</h3>
                <style>
        input{
            background-color:ghostwhite;
            border-top:0px; 
            border-left: 0px; 
            border-right: 0px; 
            width: 100%;
        }
        select{
            background-color:ghostwhite;
            border-top:0px; 
            border-left: 0px; 
            border-right: 0px; 
            width: 75%;
        }
        .abc:focus{
            outline: 0;
        }
       .A{
            width: auto;
        }
    
        table{
            width: 100%;
        }
    </style>
    <div class="row">
    <div class="col col-md-6">
    <h5 class="display-5">Add A New Course</h5>
    <form method="post"  id="addcoursef">
         <table>   
             <tr>
                <td class="A"><label class="my-1" for="">Course Name</label></td>
                <td class="B">:</td>
                <td class="C"><input class="abc"  type="text" name="title" maxlength=20" required="" id="id_title"></td>
             </tr>
             <tr>
                <td class="A"><label class=" my-1" for="">Description</label></td>
                <td class="B">:</td>
                <td class="C"><input type="text" class="abc" maxlength="150" required="" id="id_description" name="description"></td>
             </tr>
             <tr>
                <td class="A"><label class="my-1" for="">Course Choose Instructor</label></td>
                <td class="B">:</td>
                <td class="C"><select class="abc" id="select_teacher">
                    <option selected>Choose Instructor For This Course</option>
                    ${instructors.map(function (obj) {
                    return `
                        <option value="${obj.id}">${obj.first_name}${obj.last_name}</option>
                        `
                }).join('')}
                  </select></td>
             </tr>
             <tr>
                <td class="A"></td>
                <td class="B"></td>
                <td class="text-right"><a class="btn btn-info btn-sm " type="button" onclick="addnewcourse('${id}')">Add</a></td>
             </tr>
         </table>
    </form>
    
    <h5 class="display-5">Add An Existing Course To This Room Instead</h5>
    <form method="post"  id="addexistingf">
        <table>
            <tr>
                <td class="A"><label class="my-1" for="">Select A Course To Add</label></td>
                <td class="B">:</td>
                <td class="C"><select class="abc" id="select_data">
                    <option selected>Choose A Course </option>
                    ${existing_c.map(function (obj) {
                    return `
                        <option value="${obj.c_id}">${obj.c_name}</option>
                        `
                }).join('')}
                  </select></td>
             </tr>
             <tr>
                <td class="A"></td>
                <td class="B"></td>
                <td class="text-right"><a class="btn btn-info btn-sm " type="button" onclick="addexistingcourse(${id})">Add</a></td>
             </tr>
        </table>
        </div>
    </div>
    

                `;
            }
        });
}
/*completed*/
function updateroom(id) {
    let fdata = $("#editroomform").serializeArray();
    let title = fdata[0].value;
    let description = fdata[1].value;
    let data = $("#id_picture");
    var file = data[0].files[0];
    let formData = new FormData();
    formData.append("image", file);
    formData.append("title", title);
    formData.append("description", description);
    document.getElementById("editroomform").reset();
    $.ajax(
        {
            type: 'POST',
            url: '/api/editroom/' + id,
            contentType: false,
            processData: false,
            data: formData,
            headers: { "x-csrftoken": csrftoken },
            success: function (data) {
                editroom(id, data.o_id, data.reference);
            },
            error: function (error) {
                console.log(error);
            }
        }
    );
}


function listallstudents() {
    $.ajax(
        {
            type: 'GET',
            url: '/api/listallstudents/',
            contentType: 'application/json',
            success: function (data) {
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
             <h5 class="text-center text-sm-center">Students</h5>
            <table class="table table-striped">
                <thead class="text-light">
                    <tr class="text-center">
                        <th>Username</th>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Email</th>
                        <th>Room</th>
                        <th>Change Room</th>
                    </tr>
                </thead>
                <tbody>
            ${data.map(function (obj) {
                    return `
            <tr class="text-center row1">
                <td>${obj.username}</td>
                <td>${obj.first_name} ${obj.last_name}</td>
                <td>${obj.phone}</td>
                <td>${obj.email}</td>
                <td>${obj.room}</td>
                <td><select name="rooms" id="rooms" onchange="change_room(this, '${obj.id}')">
                        <option>select to change</option>
                          ${roomslist.map(function (o){return `<option value="${o.id}">${o.title}</option>`})}
                        </select></td>
            </tr>`;
                }).join('')}
            </tbody>`;
                let element = document.getElementById('canvas');
                element.innerHTML = val;
            }


        }
    );

}

function change_room(selectObject,s_id){
    var value = selectObject.value;
    $.ajax({
        type : 'POST',
        url : '/api/changestudentroom/',
        contentType: 'application/json',
        data: JSON.stringify({'student_id':s_id, 'room_id':value}),
        headers: { "X-CSRFToken": csrftoken },
        success:function (data){
            listallstudents();
            alert('Room changed status : '+data.room_id);
        }
    })
}

/*completed*/
function removestudent(id, o_id, reference) {
    $.ajax(
        {
            type: 'GET',
            url: '/api/removestudentfromcurrentroom/' + id,
            contentType: 'application/json',
            success: function (data) {
                roomstudents(data.room_id, o_id, reference);
            }
        }
    );
}


function listallteachers() {
    $.ajax(
        {
            type: 'GET',
            url: '/api/listallteachers/',
            contentType: 'application/json',
            success: function (data) {
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
             <h5 class="text-center text-sm-center">Teachers</h5>
            <table class="table table-striped">
                <thead class="text-light">
                    <tr class="text-center">
                        <th>Username</th>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Email</th>
                       <th>Action</th> 
                    </tr>
                </thead>
                <tbody>
                
            ${data.map(function (obj) {
                    return `
            <tr class="text-center row1">
                <td>${obj.username}</td>
                <td>${obj.first_name} ${obj.last_name}</td>
                <td>${obj.phone}</td>
                <td>${obj.email}</td>
                <td><a class="btn btn-outline-danger btn-sm d-inline" onclick="fireinstructor()">Delete</a></td>
            </tr>`;
                }).join('')}
            </tbody>`;
                let element = document.getElementById('canvas');
                element.innerHTML = val;
            }
        }
    );


}


function timetablems(){
    var area = document.getElementById("canvas");
    let initial = `
    <h1>this is testing</h1>
    `;
    area.innerHTML=initial;
}