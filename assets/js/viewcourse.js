function opencourse(c_id) {
    $.ajax({
        type: 'GET',
        url: '/api/opencourse/' + c_id,
        contentType: 'application/json',
        success: function (data) {
            let lectures = data[0];
            let resourses = data[1];
            let firstlecture;

            if(data.response === "no data available"){
                lectures = [];
                resourses = [];
                firstlecture = [{"video":"/filestatic/videos/default.mp4","l_description":"", 'l_name':"NO LECTURE IS ADDED YET"},]
            }
            else if(lectures[0]===undefined){
                lectures = [];
                firstlecture = [{"video":"/filestatic/videos/default.mp4","l_description":"", 'l_name':"NO LECTURE IS ADDED YET"},]
            }
            else {
                firstlecture = [lectures[0],];
            }
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
                    <div class="col-12 col-xl-8">
                    <style>
                    .contain {
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
                    
                    
                    
                    
                    <div class="contain mt-2 mb-2">
                         <video id = "videoframe" class="responsive-iframe" controls autoplay> <source src="${firstlecture[0].video}" type="video/mp4"> </video>
                    </div>
                    <div class="p-0" id="lecturefooter">
                        <h5 class="ml-2">${firstlecture[0].l_name}</h5>
                        <h6 class="ml-2">${firstlecture[0].l_description}</h6>
                       </div> 
                    </div>
                    <div class="col-12 col-xl-4 mt-2">
                        <table class="table">
                            <thead class="text-dark">
                                <tr class="text-center">
                                    <th>Lectures</th>
                                    <th></th>
                                </tr>
                            </thead>
                            <tbody>
                                ${lectures.map(function (l) {
                let l_url = l.video;
                return `
                                    <tr>
                                        <td>
                                            <button class="btn btn-link border-0 btn-block text-left" onclick="loadlecture('${l_url}','${l.l_description}','${l.id}','${l.l_name}')"><span style="font-weight: bolder">L: ${l.l_number}</span>
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



function loadlecture(l, description, id, name) {
    let frame = document.getElementById("videoframe");
    frame.setAttribute("src", l);
    document.getElementById("lecturefooter").innerHTML = `
    <h5 class="ml-2">${name}</h5>
    <h6 class="ml-2">${description}</h6>
    `;
}