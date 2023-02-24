
// function inc
// increments the isbn
var inc = function(isbn){
    // see https://reqbin.com/code/javascript/wzp2hxwh/javascript-post-request-example
    console.log("inc("+isbn+")");
    fetch('/book/'+isbn+'/note/inc', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(response => console.log(JSON.stringify(response)))
    window.location.reload();
};


// function dec
// decrements the isbn
var dec = function(isbn){
    // see https://reqbin.com/code/javascript/wzp2hxwh/javascript-post-request-example
    console.log("inc("+isbn+")");
    fetch('/book/'+isbn+'/note/dec', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(response => console.log(JSON.stringify(response)))
    window.location.reload();
};

function populateTable(items) {
    const table = document.getElementById("testBody");
        items.forEach( item => {
          // console.log("add item", item);
          let row = table.insertRow();
          let isbn = row.insertCell(0);
          let author = row.insertCell(1);
          let title = row.insertCell(2);
          let note = row.insertCell(3);
          let dejapris = row.insertCell(4);
          let link = row.insertCell(5);
          isbn.innerHTML = item.isbn;
          title.innerHTML = item.title;
          author.innerHTML = item.author;
          note.innerHTML = item.note;
          note.innerHTML = '<i class="pbutton_less" onclick="dec('+item.isbn+')">-</i>' + note.innerHTML + '<i class="pbutton_plus" onclick="inc('+item.isbn+')">+</i>';
          dejapris.innerHTML = item.dejapris;
          link.innerHTML = '<a href="https://www.abebooks.fr/servlet/SearchResults?kn='+item.isbn+'">lien<a>'
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
        for (j = 0; j < tds.length; j++) {
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
