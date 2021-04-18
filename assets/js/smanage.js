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
                let link;
                let method;
                if (obj.session_id == null){
                    method = "join_call("+obj.web_rtc_request+")";
                    link = "#"
                }
                else {
                    link = obj.session_id;
                    method = ""
                }
            return `
            <tr class="text-center row1">
                <td>${obj.course.c_name}</td>
                <td>${obj.start_time}</td>
                <td>${obj.agenda}</td>
                <td><a href="${link}" onclick="${method}" class="btn btn-sm btn-info">Join</a> </td>
               
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

function live_session_request_status(){
    let can = document.getElementById("canvas");
    $.ajax(
        {
            type:'GET',
            url:'/api/live_session_request_status/',
            contentType:'application/json',
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
             <h5 class="text-center text-sm-center">Live Session Request Status</h5>
            <table class="table table-striped">
                <thead class="text-light">
                    <tr class="text-center">
                        <th>Course</th>
                        <th>Instructor</th>
                        <th>Schedule</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                ${data.requests.map(function (obj) {
                 return `
            <tr class="text-center row1">
                <td>${obj.for_course.c_name}</td>
                <td>${obj.for_course.instructor.user.first_name} ${obj.for_course.instructor.user.last_name}</td>
                <td>${obj.scheduled_time}</td>
                <td>${obj.status}</td>
                
            </tr>`;
             }).join('')}
            </tbody>
            
        `;
        can.innerHTML=assign;


            },

            error: function (data){
                alert("Error : Please Retry!")
            }
        }
    );
}

function join_call(id){
    $.ajax(
        {
            type:'GET',
            url:'/api/live_class_get_offer/'+id,
            contentType:'application/json',
            success: function (data){
                if (data === ''){
                    alert("Your Teacher Has Not Start The Session Yet!")
                }
                student_side_web_rtc_initiator(data);
            }
        }
    );
}
let test ;

function student_side_web_rtc_initiator(offer){
    let canvas = document.getElementById("canvas");
    canvas.innerHTML = `
        <div id="wait"><h5>Please Wait While Class Is Being Setup</h5></div>
        <video autoplay id="player"></video>
        <video autoplay id="live_player"></video>
    `
    const remoteConnection = new RTCPeerConnection()
    navigator.mediaDevices.getUserMedia({
            video: true,
            audio:true,
        }).then(stream => {
            remoteConnection.addStream(stream)
            document.getElementById("live_player").srcObject = stream;
        });
    let off = {'type':'offer', 'sdp':offer.toString()}
    remoteConnection.onicecandidate = e =>  {
    console.log(" NEW ice candidnate!! on localconnection reprinting SDP " )
    console.log(JSON.stringify(remoteConnection.localDescription) )
    }

    remoteConnection.ondatachannel = e => {

    const receiveChannel = e.channel;
    receiveChannel.onmessage = e => console.log("messsage received!!!" + e.data)
    receiveChannel.onopen = e => console.log("open!!!!");
    receiveChannel.onclose = e => console.log("closed!!!!");
    remoteConnection.channel = receiveChannel;

    }

    remoteConnection.ontrack = e => {
        console.log(e.streams);
        document.getElementById("player").srcObject = e.streams[0];
    }
    remoteConnection.setRemoteDescription(off).then(a=>console.log("done"))

    remoteConnection.createAnswer().then(a => remoteConnection.setLocalDescription(a)).then(a=>
    console.log(JSON.stringify(remoteConnection.localDescription)))

}
