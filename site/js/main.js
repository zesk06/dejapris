console.log("main.js is loading")
getData();

function populateTable(items) {
    const table = document.getElementById("testBody");
        items.forEach( item => {
          // console.log("add item", item);
          let row = table.insertRow();
          let isbn = row.insertCell(0);
          let title = row.insertCell(1);
          let note = row.insertCell(2);
          let dejapris = row.insertCell(3);
          let link = row.insertCell(4);
          isbn.innerHTML = item.isbn;
          title.innerHTML = item.title;
          note.innerHTML = item.note;
          dejapris.innerHTML = item.dejapris;
          link.innerHTML = '<a href="toto.html">toto<a>'

        });
}
async function getData() {
    const response = await fetch('/book/');
    // console.log(response);
    const data = await response.json();
    // console.log(data);
    populateTable(data);
}
