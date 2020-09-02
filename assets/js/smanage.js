$.ajax(
        {
            type : 'GET',
            url : '/api/viewstudentroom/',
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
                }).join('')}`;
                let elemen = document.getElementById('canvas');
                elemen.innerHTML = val;
            }

        }
    );