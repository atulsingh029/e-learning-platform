const csrftoken = $("[name=csrfmiddlewaretoken]").val();

function all_c(){
    let c = $.ajax({
    type : 'GET',
            url : '/api/listallcourses/',
            dataType : 'json',
            success  : function (data) {
                handleData1(data);
            }
    });
    return c;
}
all_c();
let allcourses;
function handleData1(data){
     allcourses= data;
}


function all_t(){
    let c = $.ajax({
    type : 'GET',
            url : '/api/listallteachers/',
            dataType : 'json',
            success  : function (data) {
                handleData2(data);
            }
    });
    return c;
}

let allteachers;
function handleData2(data){
     allteachers= data;
}

/*completed*/
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
                 document.getElementById("canvas").innerHTML= val;

            }
        }
    );
}

function listallcourses() {
    $.ajax(
        {
            type : 'GET',
            url : '/api/listallcourses/',
            dataType : 'json',
            success  : function (data) {
                let val = `
                <div class="row row-cols-1 row-cols-md-3">
                ${data.map(function(obj) {
                    var url='';
                    let btn_status;
                    let btn_view='';
                    let label = "disabled";
                    if(obj.c_status !== true){
                        btn_status = "btn-success";
                        label="active";
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
                 document.getElementById("canvas").innerHTML= val;

            }
        }
    );
}

function opencourse(c_id){
    $.ajax({
        type: 'GET',
            url: '/api/opencourse/'+c_id,
            contentType: 'application/json',
            success : function (data) {
            console.log(data);
            /*
            * Abhishek
            * data is the variable that contains two arrays as shown in picture on github, i.e. first array contains all the lectures and second contains all the resources
            * on the DOM you have a div with id "canvas"
            * in that div you have to show all the data both lectures and resources
            * first resources below it lectures
            * */

            }
    });
}

/*completed*/
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

/*completed*/
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
function openroom(room_id,o_id,reference) {   /*Teacher name feature pending*/
    all_t();
    let element = document.getElementById('canvas');
    let trigers = ` <div>
                    <button onclick='addcourseform(${room_id})' class='btn btn-sm btn-success d-inline mr-1'>Add Course</button>
                    <button onclick='deleteroom(${room_id})' class="btn btn-sm  btn-danger mr-1 d-inline">Delete Room</button>
                    </div> `;
                element.innerHTML = trigers+
                    "<div id='subcan1'></div>" +
                    "<div id='subcan2'></div>" +
                    "<div id='subcan3'></div>";
    editroom(room_id,o_id,reference);
    $.ajax(
        {
            type : 'GET',
            url : '/api/viewroom/'+room_id,
            contentType :'application/json',
            success : function (data) {
                let val = `
                <div class="row row-cols-1 row-cols-md-3">
                ${data.data.map(function(obj) {
                    if (obj.c_status === false){
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
                    `;}
                }).join('')}
                </div><h5>Students In This Room</h5>`;
                let elemen = document.getElementById('subcan2');
                elemen.innerHTML = val;
                roomstudents(room_id,o_id,reference);
            }

        }
    );
}

function editroom(room_id,o_id,reference) {
    $.ajax(
        {
            type:"GET",
            url: "/api/editroom/"+room_id,
            contentType:"application/json",
            success : function (data) {
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
function acceptapplication(reference){
    $.ajax(
        {
            type : 'POST',
            url : '/api/acceptapplications/',
            contentType :'application/json',
            data : JSON.stringify({"reference":reference}),
            headers: { "X-CSRFToken": csrftoken },
            success:function (data) {
                listapplications();
            }
        }
    );
}

/*completed*/
function rejectapplication(reference){
    $.ajax(
        {
            type : 'POST',
            url : '/api/rejectapplications/',
            contentType :'application/json',
            data : JSON.stringify({"reference":reference}),
            headers: { "X-CSRFToken": csrftoken },
            success:function (data) {
                listapplications();
            }
        }
    );
}

/*completed*/
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

/*completed*/
function roomstudents(id,o_id,reference) {
    $.ajax(
        {
            type: 'GET',
            url: '/api/listroomstudents/'+id,
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
                
            ${data.map(function(obj) {
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
    if(teacher.options[teacher.selectedIndex].value === "Choose Instructor For This Course" || data[0].value==="" || data[1].value===""){
        alert("Invalid Input : Some Fields Missing");
    }
    else {
        var teacher_id = teacher.options[teacher.selectedIndex].value;
    $.ajax(
        {
            type : 'POST',
            url : '/api/addcourse/new/',
            contentType :'application/json',
            data : JSON.stringify({"room_id":id,"title":data[0].value,"description":data[1].value,"teacher_id":teacher_id}),
            headers: { "X-CSRFToken": csrftoken },
            success:function (data) {
                alert("Course Added");
                all_c();
                openroom(id,data.o_id,data.reference)
            }
        }
    );
    }
}

function addexistingcourse(id) {
    let form = document.getElementById("select_data").value;
    let d = JSON.stringify({"room_id":id,"c_id":form});
    $.ajax({
        type : 'POST',
        url : '/api/addcourse/existing/',
        contentType :'application/json',
        data : d,
        headers: { "X-CSRFToken": csrftoken },
        success:function (data) {
                openroom(id,data.o_id,data.reference);
            }
    });

}



function addcourseform(id){
    let existing_c = allcourses;
    if (existing_c === undefined){
        alert("Some Error Occurred While Loading The Page, Please Refresh!");
    }
    let instructors = allteachers;
    $.ajax(
        {
            type : 'GET',
            url : '/api/viewroom/'+id,
            contentType :'application/json',
            success: function(data){
                let view = document.getElementById('canvas');
                view.innerHTML=`
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
                    ${instructors.map(function (obj){
                        return`
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
                    ${existing_c.map(function (obj){
                        return`
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
function updateroom(id){
    let fdata = $("#editroomform").serializeArray();
    let title = fdata[0].value;
    let description = fdata[1].value;
    let data = $("#id_picture");
    var file = data[0].files[0];
    let formData = new FormData();
    formData.append("image",file);
    formData.append("title",title);
    formData.append("description",description);
    document.getElementById("editroomform").reset();
     $.ajax(
        {
            type : 'POST',
            url : '/api/editroom/'+id,
            contentType :false,
            processData : false,
            data :formData,
            headers : {"x-csrftoken" : csrftoken},
            success : function (data) {
                editroom(id,data.o_id,data.reference);
            },
            error : function (error) {
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
            success : function (data) {
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
                        <th>username</th>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Email</th>
                        <th>Room</th>
                        <th>Change Room</th>
                    </tr>
                </thead>
                <tbody>
            ${data.map(function(obj) {
                    return `
            <tr class="text-center row1">
                <td>${obj.username}</td>
                <td>${obj.first_name} ${obj.last_name}</td>
                <td>${obj.phone}</td>
                <td>${obj.email}</td>
                <td>${obj.room}</td>
                <td>action</td>
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
function removestudent(id,o_id,reference) {
    $.ajax(
        {
            type: 'GET',
            url: '/api/removestudentfromcurrentroom/'+id,
            contentType: 'application/json',
            success : function (data) {
                roomstudents(data.room_id,o_id,reference);
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
            success : function (data) {
                console.log(data)
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
                        <th >Username</th>
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