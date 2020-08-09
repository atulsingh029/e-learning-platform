const btn_listallrooms = document.getElementById('listallrooms');
const btn_addroom = document.getElementById('addroom');


function listallrooms() {
    $.ajax(
        {
            type : 'GET',
            url : '/api/listallrooms/',
            dataType : 'json',
            success : function (data) {
                let val = `
                <button type="button" class="btn btn-primary btn-sm p-1" data-toggle="modal" data-target="#exampleModal">Add Room</button>
                <div class="row row-cols-1 row-cols-md-3">
                ${data.map(function(obj) {
                    return `
                    <div class="card m-3" style="max-width: 20em;min-width: 20em;max-height: 20em;min-height: 20em;">
                        <img src="${obj.profile_pic}" class="card-img-top" alt="...">
                        <div class="card-body">
                            <h5 class="card-title">${obj.title}</h5>
                            <p class="card-text text-muted">${obj.room_stream_details}</p>
                            <p class="card-text ">${obj.description}</p>
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

function addroom(input,token) {
    $.ajax(
        {
            type : 'POST',
            url : '/api/addroom/',
            contentType :'application/json',
            data : input,
            headers: { "X-CSRFToken": token },
            success:function () {
                alert("success");
            }
        }
    );
}


// this is helper function, it collects form input and passes it as addroom method argument
function input(){
    let x = $("#roomform").serializeArray(); // This line collects data inputted by user in form
    document.getElementById("roomform").reset(); //This line resets the form that was filled by user after collecting data from it.
    let a = x[1].value;
    let b = x[2].value;
    var token = x[0].value;
    addroom(JSON.stringify({"title":a,"description":b}),token);

}


btn_listallrooms.addEventListener('click',listallrooms);
btn_addroom.addEventListener('click',input);