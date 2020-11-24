const csrftoken = $("[name=csrfmiddlewaretoken]").val();
let can = document.getElementById("canvas");
can.innerHTML="<div class=\"col-xs-12 col-sm-12 col-md-12 col-lg-12 col-xl-3 input-group mb-2 mt-2 mt-sm-2 mt-md-2\">\n" +
    "                      <input type=\"text\" class=\"form-control border-dark btn-sm\" placeholder=\"@username/email/phone/name\" id=\"search_key\" required>\n" +
    "                      <div class=\"input-group-append\">\n" +
    "                        <button class=\"btn btn-sm btn-outline-dark\" type=\"button\" onclick=\"search()\">Search</button>\n" +
    "                      </div>\n" +
    "            </div>" +
    "<div id=\"search_result\"></div>"+
    "<div id='can1'></div>" +
    "<div id = 'can2'></div>";
let courses = [];
$.ajax({
    type:'GET',
    url:"/dashboard/tls/",
    contentType:'json',
    success:function (data){
        let va = `
<h5>Today's Live Class TimeTable</h5>
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
                        <th>Course</th>
                        <th>Time</th>
                        <th>Agenda</th>
                        <th>Join</th
                        
                    </tr>
                </thead>
                <tbody>
                
            ${data.map(function (obj) {
                    return `
            <tr class="text-center row1">
                <td>${obj.course.c_name}</td>
                <td>${obj.start_time}</td>
                <td>${obj.agenda}</td>
                <td><a href="${obj.session_id}" target="_blank" class="btn btn-sm btn-info">Join</a> </td>
               
            </tr>`;
                }).join('')}
            </tbody>`;
        document.getElementById("can1").innerHTML=va;
    }

});


$.ajax({
    type:'GET',
    url:"/api/getteacherscourse",
    contentType:'json',
    success:function (data){
        courses = data;
        let temp = `
<h5>Your Courses</h5>
            <div class="row row-cols-1 row-cols-md-3">
                ${data.map(function (obj) {
            if (obj.c_status === false) {
                return `
                    <div class="card m-2 border-dark rounded" style='max-width: 20em;min-width: 20em;max-height: 16em;min-height: 16em;'>
                        <div class="card-body">
                            <h4 class="card-title">${obj.c_name}</h4>
                            <p class="card-text">${obj.c_description}</p>
                            
                        </div>    
                        <div class="card-footer text-center">
                              <a href="#" onclick="opencourse(${obj.c_id})" class="btn btn-sm btn-primary">View Course</a>
                        </div>
                        
                    </div>
                    `;
            }
        }).join('')}`;
        can2.innerHTML=temp;
    }
});



function roomstudentsIni() {
    $.ajax(
        {
            type: 'GET',
            url: '/dashboard/getstudentsteacher/',
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
            <table class="table table-striped">
                <thead class="text-light">
                    <tr class="text-center">
                        <th>Username</th>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Email</th>
                        <th>Room</th>
                        
                    </tr>
                </thead>
                <tbody>
                
            ${data.map(function (obj) {
                    return `
            <tr class="text-center row1">
                <td>${obj.user.username}</td>
                <td>${obj.user.first_name} ${obj.user.last_name}</td>
                <td>${obj.user.phone}</td>
                <td>${obj.user.email}</td>
               <td>${obj.from_room.title}</td>
            </tr>`;
                }).join('')}
            </tbody>`;
                let element = document.getElementById('canvas');
                element.innerHTML = val;
            }


        }
    );
}


function assignments(){
    $.ajax(
        {
            type: 'GET',
            url: '/dashboard/assignments',
            dataType: 'json',
            success: function (data) {
                let val = `
                <h5>Assignments</h5>
                <div class="row row-cols-1 row-cols-md-3">
                ${data.map(function (obj) {
                    
                    return `
                    
                    <div class="card m-2 border-dark rounded" style='max-width: 20em;min-width: 20em;max-height: 12em;min-height: 12em;'>
                        <div class="card-body" style="overflow: hidden">
                            <h4 class="card-title">${obj.name}</h4>
                            
                            <p class="card-text" >${obj.description}</p>
                            
                        </div>    
                        <div class="card-footer text-center">
                              <button class="btn btn-sm btn-info">${obj.max_marks}</button>
                              <a href="#" onclick="openassignment('${obj.id}','${obj.description}','${obj.problem}')" class="btn btn-sm btn-primary">Check Assignment</a>
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

function openassignment(id,description,problem){
    $.ajax(
        {
            type: 'GET',
            url: '/dashboard/solutions/'+id,
            dataType: 'json',
            success: function (data) {
                let val = `
                <a href="${problem}" class="btn btn-sm btn-primary">View Problem</a>
                <h5 class="mt-1">Description : ${description}</h5>
                <div class="row row-cols-1 row-cols-md-3">
                ${data.map(function (obj) {
                    
                    return `
                    
                    <div class="card m-2 border-dark rounded" style='max-width: 20em;min-width: 20em;max-height: 10em;min-height: 10em;'>
                        <div class="card-body" style="overflow: hidden">
                            <h4 class="card-title">${obj.uploader.first_name} ${obj.uploader.last_name}</h4>
                            <h4>@ ${obj.uploader.username}</h4>
                        </div>    
                        <div class="card-footer text-center">
                              
                              <a href="${obj.solution}" class="btn btn-sm btn-primary">View Solution</a>
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

function scheduleclass(){
    let sch_window = document.getElementById("canvas");
    let sch_template = `
    <h5>Schedule Online Class</h5>
    <p>Note:Time should be entered in HOURS only, minute entry will not be considered.</p>
    <div class="col-5 ml-1">
    <form id="class_schedule" method="POST">
        <div class="form-group">
        <label class="my-1" for="agenda"> Agenda</label>
        <input id="agenda" type="text"  required maxlength="256" name="agenda">
        </div>
        <div class="form-group">
        <label class="my-1" for="date"> Date</label>
        <input id="date" type="date" required name="date">
        </div>
        <div class="form-group">
        <label class="my-1" for="stime"> Start Time</label>
        <input id="stime" type="time" required name="stime">
        </div>
        
        <div class="form-group">
        <label for="session_id" class="my-1 mr-2">Session URL</label>
        <input type="text" id="session_id" required name="url">
        </div>
        <div class="form-group">
        <label class="my-1" for="clist"> Select Course</label>
          <select class="my-1" id="clist" name="course">
            <option selected>Choose</option>
            ${courses.map(function (c){
                return `<option value = "${c.c_id}">${c.c_name}</option>`;
    }).join('')}
          </select></div>
          <button class="btn btn-sm btn-success" type="button" onclick="scheduler()">Schedule</button>
    </form>
    </div>
    `;
    sch_window.innerHTML=sch_template;
}

function scheduler(){
    let s_data = $("#class_schedule").serializeArray();
    let obj = JSON.stringify(s_data);
    $.ajax(
        {
            type: 'POST',
            url: '/dashboard/schedule/',
            contentType: 'application/json',
            data: obj,
            headers: { "X-CSRFToken": csrftoken },
            success:function (data){
            alert(data);
            if (data ==='added'){
                let a = document.getElementById("class_schedule").reset();
            }
            }
        });
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
