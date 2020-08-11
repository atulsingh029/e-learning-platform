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
                    return `
                     
                    <div class="card m-2 " style='max-width: 20em;min-width: 20em;max-height: 16em;min-height: 16em;'>
                        <div class="card-body" style='background-image:url(${url});background-size: cover'>
                            <div class="card-body">
                              <h1 class=" card-title">${obj.title}</h1>
                              <p class="card-text">${obj.description}</p>
                              <a href="#" class="btn btn-secondary mt-5 disabled">${obj.room_stream_details}</a>
                              <a href="#" onclick="openroom(${room_id})" class="btn btn-primary mt-5">Go To Room</a>
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
                let element = document.getElementById('canvas');
                element.innerHTML = "pending";  /* write your template here */
            }

        }
    );
}