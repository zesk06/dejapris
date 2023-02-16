getData();

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
