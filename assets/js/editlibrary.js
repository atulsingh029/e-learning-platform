function loadLibraryDashboard(){
    var library_view = document.getElementById("canvas");
    library_view.innerHTML = "<h> Please Wait, Loading Books!</h>";
    $.ajax(
        {
            type : 'GET',
            url : '/elibrary/lib/',
            contentType : "application/json",
            success : function (data){
                library_view.innerHTML = "<div id='academic_books'></div>" +
                    "<div id='non_academic_books'></div>";
                var academic = [];
                var nonacademic = [];
                data.map(function (book){
                    if (book.type === "academic"){
                        academic.push(book);
                    }
                    else {
                        nonacademic.push(book);
                    }
                });
                var acad_template = `
                <div><a href="/elibrary/add/" class="btn btn-sm btn-info">Add Book</a></div><br>
                <div><h5>ACADEMICS BOOK</h5></div>
                <div class="row row-cols-1 row-cols-md-3">
                
                ${academic.map(function (o){
                    if (o.description === null){
                        o.description='';
                    }
                    return`
                <div class="card border-dark m-3" style="max-width: 250px; height: 200px; background-image: url('${o.cover}')">
                    <div class="card-body">
                       
                    </div>
                    <div><a href="${o.file}"><span class="material-icons">get_app</span></a><a href="#" onclick="delete_book(${o.id})"><span class="material-icons">delete</span></a></div><h5 class="p-1">${o.title}</h5>
                </div>
                    `;
                }).join('')}
                </div>
                `;


                var non_acad_template = `
                <div><h5>NON-ACADEMICS BOOK</h5></div>
                <div class="row row-cols-1 row-cols-md-3">
                
                ${nonacademic.map(function (o){
                    if (o.description === null){
                        o.description='';
                    }
                    return`
                <div class="card border-dark m-3" style="max-width: 250px; height: 200px; background-image: url('${o.cover}')">
                    <div class="card-body text-center">
                       
                    </div>
                    <div><a href="${o.file}"><span class="material-icons">get_app</span></a><a href="#" onclick="delete_book(${o.id})"><span class="material-icons">delete</span></a></div><h5 class="p-1">${o.title}</h5>
                </div>
                    `;
                }).join('')}
                </div>
                `;

                document.getElementById("academic_books").innerHTML = acad_template;
                document.getElementById("non_academic_books").innerHTML = non_acad_template;
            }
        }
    );
}


function delete_book(id){
    $.ajax({
        type: "GET",
        url: "/elibrary/delete/"+id,
        contentType: "application/json",
        success:function (data){
            alert(data);
            loadLibraryDashboard();
        },
        error:function (){
            alert("Error : Try again!")
        }
    });
}