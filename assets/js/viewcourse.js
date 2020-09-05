function rm_opencourse(c_id) {
    $.ajax({
        type: 'GET',
        url: '/api/opencourse/' + c_id,
        contentType: 'application/json',
        success: function (data) {
            var lectures = data[0];
            var resourses = data[1];
            canvas.innerHTML = `
            <div>
                <style>
                    h1 {
                        font-size: 3rem;
                        font-weight: 50;
                        color: rgb(18, 18, 19);
                        font-family: 'Nunito', sans-serif;
                    }
                </style>
                <div class="accordion col text-center text-dark" id="accordionE">
                    <div class="card border-0 m-0 p-0">
                        <div class="card-header" id="headingTwo" style="background-color: white">
                            <h2 class="mb-0">
                                <button class="btn btn-link btn-block text-left collapsed text-center" type="button"
                                    data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false"
                                    aria-controls="collapseTwo">
                                    Courses Resources
                                </button>
                            </h2>
                        </div>
                        <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionE">
                            <div class="row">
                            ${resourses.map(function (r) {
                var url;
                if (r.cr_url === null) {
                    url = r.file;
                }
                else {
                    url = r.cr_url;
                }
                return `
                                <div class="card-body">
                                <div class="card" style="width: 18rem; height: 9rem;">
                                  <div class="card-body">
                                    <h5 class="card-title">${r.cr_name}</h5>
                                    <small class="card-text">${r.cr_description}</small><br>
                                       <a href="${url}" target="_blank"><i class="material-icons mb-0 mt-1">launch</i></a>
                                  </div>
                                </div>
                            </div>
                                `;
            }).join('')}
                        </div>
                        </div>
                    </div>
                </div>
            
                <div class="row align-items-center m-1">
                    <div class="col-12 col-xl-8 ">
                    <style>
                    .container {
                      position: relative;
                      width: 100%;
                      overflow: hidden;
                      padding-top: 56.25%; /* 16:9 Aspect Ratio */
                    }
                    
                    .responsive-iframe {
                      position: absolute;
                      top: 0;
                      left: 0;
                      bottom: 0;
                      right: 0;
                      width: 100%;
                      height: 100%;
                      border: none;
                    }
                    </style>
                    <div class="container mt-2 mb-2">
                         <iframe id = "videoframe" class="responsive-iframe" src="${lectures[0].l_url}"></iframe>
                    </div>
                    <div class="row p-0" id="lecturefooter">
                        <p>${lectures[0].l_description}</p>
                       </div> 
                    </div>
                    <div class="col-12 col-xl-4  mt-2">
                        <table class="table">
                            <thead class="text-dark">
                                <tr class="text-center">
                                    <th>Lectures</th>
                                    <th></th>
                                </tr>
                            </thead>
                            <tbody>
                                ${lectures.map(function (l) {
                var l_url = l.l_url;
                return `
                                    <tr>
                                        <td>
                                            <button class="btn btn-link border-0 btn-block text-left" onclick="loadlecture('${l_url}','${l.l_description}','${l.id}')"><span style="font-weight: bolder">Lecture ${l.l_number}</span>
                                            <p>${l.l_name}</p>
                                            </button>
                                        </td>
                                    </tr>
                                    `;
            }).join('')}
                              
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
`;

        }
    });
}

function loadlecture(l, description, id) {
    var frame = document.getElementById("videoframe");
    frame.setAttribute("src", l);
    document.getElementById("lecturefooter").innerHTML = `
    <p>${description}</p>
    `;
}
