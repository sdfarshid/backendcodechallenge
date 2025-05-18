let allAuthors = [];

window.onload = async function () {
  await loadAuthors(true);
  setupEvents();
};

document.getElementById("perPageSelect").onchange = function () {
  loadCommits();
};

function setupEvents() {
  document.getElementById("fetchBtn").onclick = async function () {
      const countValue = parseInt(document.getElementById("countBtn").value) || 10;

    try {
      await fetch("/api/v1/fetching/back-fetching", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ count: countValue })

      });
      await loadAuthors(true);
      alert("start New data fetched processing.");
    } catch (err) {
      console.log(" Failed to fetch new data.");
    }
  };

  document.getElementById("authorSelect").onchange = function () {
    loadCommits();
  };
}

async function loadAuthors(selectFirst = false) {
  try {

    const res = await fetch("/api/v1/author/list?limit=0");
    allAuthors = await res.json();
    const select = document.getElementById("authorSelect");
    let html = '<option value="">All Authors</option>';
    allAuthors.forEach(author => {
      html += `<option value="${author.id}">${author.name || author.id}</option>`;
    });
    select.innerHTML = html;

    if (selectFirst && allAuthors.length > 0) {
      select.value = allAuthors[0].id;
      await loadCommits();
    }

  } catch (err) {
    console.log("Error loading authors.");
  }
}

async function loadCommits() {
  try {
    const authorId = document.getElementById("authorSelect").value;
    const perPage = document.getElementById("perPageSelect").value;

    const url = new URL(window.location.origin + "/api/v1/commit/list");
    if (authorId) {
      url.searchParams.set("author_id", authorId);
    }
    url.searchParams.set("limit", perPage);

    const res = await fetch(url);
    const commits = await res.json();

    const tbody = document.querySelector("#commitTable tbody");
    let html = "";
    commits.forEach(commit => {
      const author = allAuthors.find(a => a.id === commit.author_id);
      const authorName = author ? author.name : "(Unknown Author)";
      const date = new Date(commit.created_at);
      const formattedDate = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")} ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;

      const staticLink = `https://github.com/nodejs/node/commit/${commit.hash}`;

      html += `
        <tr>
          <td>${commit.id}</td>
          <td><a href="${staticLink}" target="_blank">${commit.hash}</a> </td>
          <td>${authorName}</td>
          <td>${formattedDate}</td>
        </tr>`;
    });
    tbody.innerHTML = html;
  } catch (err) {
        console.log("Error loading commits.");
  }
}
