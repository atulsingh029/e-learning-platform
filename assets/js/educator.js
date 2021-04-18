let ice_candidates = [];
let localConnection;
function initiate_live_class(id) {
    let canvas = document.getElementById("canvas");
    canvas.innerHTML = `
        <div id="wait"><h5>Please Wait While Class Is Being Setup</h5></div>
        <video autoplay id="live_player"></video>
        <video autoplay id="r-player"></video>
    `
    const ice_configurations = {
        iceServers: [{ urls: 'stun:stun.l.google.com:19302' },

        ]
    };
    localConnection = new RTCPeerConnection(ice_configurations);

    localConnection.onicecandidate = e => {
        console.log("new candidate added")
        ice_candidates.push(localConnection.localDescription)
    }

    const sendChannel = localConnection.createDataChannel("sendChannel");
        sendChannel.onmessage = e => console.log("messsage received!" + e.data)
        sendChannel.onopen = e => console.log("open!");
        sendChannel.onclose = e => console.log("closed!");

        navigator.mediaDevices.getUserMedia({
            video: true,
            audio:true,
        }).then(stream => {
            localConnection.addStream(stream)
            localConnection.createOffer().then(o => localConnection.setLocalDescription(o))
            document.getElementById("live_player").srcObject = stream;
        });

        localConnection.ontrack = e => {
        console.log(e.streams);
        document.getElementById("r-player").srcObject = e.streams[0];
    }

        document.getElementById("wait").innerHTML = `
        <button class="btn btn-success btn-sm" onclick="send_offer_to_students(${id})">Start Class</button>
        <button class="btn btn-success btn-sm" onclick="add_student_to_stream(${id})">Refresh If Student Not Visible</button>
        `
}


function send_offer_to_students(id){

    let input = JSON.stringify({ "offer": ice_candidates[ice_candidates.length-1]});
    console.log(input)
    $.ajax(
        {
            type: 'POST',
            url: '/api/liveclass/offer/'+id,
            contentType: 'application/json',
            data: input,
            headers: { "X-CSRFToken": csrftoken },
            success: function () {
                alert("class began")
                add_student_to_stream(id);
            },
            error : function (er){
                alert("Error Occurred... Try Again")
            }
        }
    );
}


function add_student_to_stream(id){
    $.ajax(
        {
            type:'GET',
            url:'/api/live_class_get_answer/'+id,
            contentType:'application/json',
            success: function (data){
                let ans = {'type':'answer', 'sdp':data.toString()}
                 localConnection.setRemoteDescription (ans).then(a=>console.log("done"))
            }
        }
    );
}


function get_all_live_session_requests(){
    document.getElementById("canvas").innerHTML="<div id='can1'></div>" +
    "<div id = 'can2'></div>";


$.ajax({
    type:'GET',
    url:"/api/get_live_session_requests/",
    contentType:'json',
    success:function (data) {
        let va = `
<h5>Live Session Requests</h5>
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
                        <th>Student</th>
                        <th>Message</th>
                        <th>Schedule</th>
                        
                        
                    </tr>
                </thead>
                <tbody>
                
            ${data.map(function (obj) {
            return `
            <tr class="text-center row1">
                <td>${obj.for_course.c_name}</td>
                <td>${obj.requester.user.first_name} ${obj.requester.user.last_name}</td>
                <td>${obj.message}</td>
                <td><form id="date_time_${obj.id}" method="post"><input type="hidden" name="id" value="${obj.id}"><input type="time" id="up_time_${obj.id}" value="" name="time"><input name="date" type="date" id="up_date_${obj.id}"><button type="button" class="btn btn-sm btn-outline-info" onclick="live_session_scheduler(${obj.id})">Save</button></form> </td>
                
               
            </tr>`;
        }).join('')}
            </tbody>`;
        document.getElementById("can1").innerHTML=va;
    }});
}

function live_session_scheduler(id){
    let input = $("#date_time_"+id).serializeArray();
    console.log(input)
    $.ajax(
        {
            type: 'POST',
            url: '/api/live_session_scheduler/',
            contentType: 'application/json',
            data: JSON.stringify(input),
            headers: { "X-CSRFToken": csrftoken },
            success: function (data) {
                alert(data.status)
                get_all_live_session_requests()
            },
            error : function (er){
                alert("Error Occurred... Try Again")
            }
        }
    );
}