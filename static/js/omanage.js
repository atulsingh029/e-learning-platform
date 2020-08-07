const btn_listallrooms = document.getElementById('listallrooms');
const btn_addroom = document.getElementById('addroom');


function listallrooms() {
    $.ajax(
        {
            type : 'GET',
            url : '/api/listallrooms/',
            dataType : 'json',
            success : function (data) {
                 document.getElementById("canvas").innerHTML=
                `
                ${data.map(function(obj) {
                    return `
                        <div class="card" style="width: 18rem;">
                            <div class="card-body">
                                <h5 class="card-title">Room : ${obj.title}</h5>
                                 <h6 class="card-subtitle mb-2 text-muted">Status :  ${obj.room_stream_details}</h6>
                                 <p class="card-text">Description : ${obj.description}</p>
                            </div>
                        <div>
                    `;
                }).join('')}
                `
            }
        }
    );
}

function addroom(input,token) {
    let data = input;
    $.ajax(
        {
            type : 'POST',
            url : '/api/addroom/',
            contentType :'application/json',
            data : data,
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