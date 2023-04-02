
var isbn_set_note = function(isbn,note){
    console.log("isbn_set_note("+isbn+","+note+")");
    fetch('/book/'+isbn+'/note', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'note': note})
    })
    .then(response => response.json())
    .then(response => console.log(JSON.stringify(response)))
    const note_element = document.getElementById("note_"+isbn);
    note_element.innerText = note;
};

// function thumbdown
var thumbdown = function(isbn){
    isbn_set_note(isbn, 1);
};

// function thumbup
var thumbup = function(isbn){
    isbn_set_note(isbn, 4);
};

function populateTable(items) {
    const table = document.getElementById("testBody");
        items.forEach( item => {
          // console.log("add item", item);
          let row = table.insertRow();
          let author = row.insertCell(0);
          let title = row.insertCell(1);
          let note = row.insertCell(2);
          // let dejapris = row.insertCell(3);
          let isbn = row.insertCell(3);
          isbn.innerHTML = item.isbn;
          title.innerHTML = item.title;
          author.innerHTML = item.author;
          note.innerHTML = item.note;
          note.innerHTML =  '<i class="pbutton" onclick="thumbdown('+item.isbn+')">👎</i>'
                          + '<span id="note_'+ item.isbn + '">' + note.innerHTML + '</span>' 
                          + '<i class="pbutton" onclick="thumbup('+item.isbn+')">👍</i>';
          // dejapris.innerHTML = item.dejapris;
          isbn.innerHTML = '<a href="https://www.abebooks.fr/servlet/SearchResults?kn='+item.isbn+'">'+item.isbn+'<a>'
        });
}

async function getData() {
    const response = await fetch('/book/');
    // console.log(response);
    const data = await response.json();
    // console.log(data);
    populateTable(data);
}


function filterTable(){
    console.log("filterTable()");
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
        tds = tr[i].getElementsByTagName("td");
        let concatStr = "";
        // for (j = 0; j < tds.length; j++) {
        // search only look for first three columns (author title note)
        for (j = 0; j < 3; j++) {
            txtValue = tds[j].textContent || tds[j].innerText;
            concatStr = concatStr + ":" + txtValue;
        }       
        // Manage row display
        if (concatStr.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}

getData();
