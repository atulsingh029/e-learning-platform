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
                        btn_status = "btn-danger";
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
                              <a href="#" onclick="editroomredirect(${room_id})" class="btn btn-sm  btn-primary mt-5">Edit Room</a>
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
            type : 'GET',
            url : '/api/listapplications/',
            contentType :'application/json',
            success : function (data) {
                let element = document.getElementById('canvas');
                element.innerHTML = "pending";  /* write your template here */
            }

        }
    );
}


function openroom(room_id) {
    $.ajax(
        {
            type : 'GET',
            url : '/api/viewroom/'+room_id,
            contentType :'application/json',
            success : function (data) {
                let label ="teacher"
                let val = `
                <button type="button" class="btn btn-primary btn-sm p-1" data-toggle="modal" data-target="#exampleModal">Add Room</button>
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
                </div>`;
                let element = document.getElementById('canvas');
                element.innerHTML = val;
            }

        }
    );
}

function editroomredirect(room_id) {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax(
        {
            type : 'GET',
            url : '/api/editroom/'+room_id,
            contentType :'text/plain',
            success : function (data) {
                let element = document.getElementById('canvas');
                element.innerHTML = `
                     <div class="container">
                        <div class="row m-1 p-1 mt-5">
                            <div class="col-xs-12 col-md-6 m-auto">
                                <div class="card mt-3">
                                  <div class="card-header">
                                    Edit Room
                                  </div>
                                  <div class="card-body">
                                      <form method="post" action="/dashboard/editroom/${room_id}/" enctype="multipart/form-data">
                                      <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                                      ${data}
                                      <button type="submit" class="btn btn-sm btn-info mt-1">submit</button>
                                    </form>
                                  </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

            }

        }
    );
}

