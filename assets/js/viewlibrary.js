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
                <div><h5>ACADEMICS BOOK</h5></div>
                <div class="row row-cols-1 row-cols-md-3">
                
                ${academic.map(function (o){
                    if (o.description === null){
                        o.description='';
                    }
                    return`
                <div class="card border-none m-3" style="max-width: 150px; height: 250px;">
                    <div class="card-body" onclick="showdetail('${o.title}','${o.author}','${o.edition}')" style="background-image: url('${o.cover}'); background-size: cover">
                       
                    </div>
                    <div class="card-footer">
                        <div class="text-center"><a href="${o.file}"><span class="material-icons">get_app</span></a></div>
                    </div>
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
                <div class="card border-none m-3" style="max-width: 150px; height: 250px;">
                    <div class="card-body" onclick="showdetail('${o.title}','${o.author}','${o.edition}')" style="background-image: url('${o.cover}'); background-size: cover">
                       
                    </div>
                    <div class="card-footer">
                        <div class="text-center"><a href="${o.file}"><span class="material-icons">get_app</span></a></div>
                    </div>
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

function showdetail(name,author,edition){
    alert(name+"\nBy "+author+"\nEdition : "+edition);
}