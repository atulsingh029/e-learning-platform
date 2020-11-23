const csrftoken = $("[name=csrfmiddlewaretoken]").val();
let can = document.getElementById("canvas");
$.ajax({
    type:'GET',
    url:"/api/getteacherscourse",
    contentType:'json',
    success:function (data){
        let temp = `
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
        can.innerHTML=temp;
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

function scheduleonlineclass(){

}