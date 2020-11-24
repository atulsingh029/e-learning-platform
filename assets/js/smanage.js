document.getElementById("canvas").innerHTML="<div id='can1'></div>" +
    "<div id = 'can2'></div>";


$.ajax({
    type:'GET',
    url:"/dashboard/sls/",
    contentType:'json',
    success:function (data) {
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
    }});

$.ajax(
        {
            type : 'GET',
            url : '/api/viewstudentroom/',
            contentType :'application/json',
            success : function (data) {
                let val = `
<h5>Your courses, keep learning</h5>
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
                }).join('')}`;
                let elemen = document.getElementById('can2');
                elemen.innerHTML = val;
            }

        }
    );

const csrftoken = $("[name=csrfmiddlewaretoken]").val();
function view_assignments(){
    let can = document.getElementById("canvas");
    $.ajax({
        type: 'GET',
        url:'/dashboard/listassignments/',
        contentType: 'json',
        success: function (data){
             let assign=`
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
             <h5 class="text-center text-sm-center">Assignments</h5>
            <table class="table table-striped">
                <thead class="text-light">
                    <tr class="text-center">
                        <th>Ref_No.</th>
                        <th>Name</th>
                        <th>Problem</th>
                        <th>Max_Marks</th>
                        <th>Upload</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
            ${data.map(function (obj) {
                 return `
            <tr class="text-center row1">
                <td>${obj.id}</td>
                <td>${obj.name}</td>
                <td><a class="btn btn-outline-success d-inline" href="${obj.problem}">Download</a></td>
                <td>${obj.max_marks}</td>
                <td><input type="file" id="${obj.id}"></input></td>
                <td><button type="button" class="btn btn-sm btn-success" onclick="upload('${obj.id}')">Upload</button></td>
            </tr>`;
             }).join('')}
            </tbody>
        `;
        can.innerHTML=assign;
        }
    });

}

function upload(id){
    var i = "#"+id;
    let data = $(i);
    var file = data[0].files[0];
    let formData = new FormData();
    formData.append("solution", file);
    formData.append("id", id);
    $.ajax(
        {
            type: 'POST',
            url: '/dashboard/send_sol/',
            contentType: false,
            processData: false,
            data: formData,
            headers: { "x-csrftoken": csrftoken },
            success: function (data) {
                view_assignments();
            },
            error: function (error) {
                console.log(error);
            }
        }
    );

}